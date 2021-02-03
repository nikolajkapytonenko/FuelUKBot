import requests
from bs4 import BeautifulSoup
import telebot
from telebot import types
from logging_bot import Logging
from datetime import datetime
from fuel_station import FuelStation


class FuelUser:
	def __init__(
			self,  tele_bot, message,
			first_date=datetime.today().strftime("%H.%M.%S-%Y-%m-%d"),
			last_date=datetime.today().strftime("%H.%M.%S-%Y-%m-%d")):
		self.bot = tele_bot
		self.message = message
		self.id = self.message.from_user.id
		self.firstName = self.message.from_user.first_name
		self.stations = dict()

		self.current_city = ""
		self.current_stations = list()
		
		self.use = 1
		self.last_date = last_date
		self.first_date = first_date

		self.cites = {
			"Киев": "https://index.minfin.com.ua/markets/fuel/reg/kievskaya/",
			"Одесса": "https://index.minfin.com.ua/markets/fuel/reg/odesskaya/",
			"Днепр": "https://index.minfin.com.ua/markets/fuel/reg/dnepropetrovskaya/",
			"Харьков": "https://index.minfin.com.ua/markets/fuel/reg/harkovskaya/",
			"Львов": "https://index.minfin.com.ua/markets/fuel/reg/lvovskaya/",
			"Запорожье": "https://index.minfin.com.ua/markets/fuel/reg/zaporozhskaya/",
			"Херсон": "https://index.minfin.com.ua/markets/fuel/reg/hersonskaya/",
			"Николаев": "https://index.minfin.com.ua/markets/fuel/reg/nikolaevskaya/",
			"Винница": "https://index.minfin.com.ua/markets/fuel/reg/vinnickaya/"
		}

	def text_handler(self, message):
		if message.text in self.cites:
			self.show_city_gas_stations(message.text, drop_current_stations=True)
		elif message.text in self.stations:
			self.show_station(message.text)
		elif message.text == "drop":
			self.drop_stations()
		else:
			self.send_msg(message)

	def show_city_gas_stations(self, city_name, drop_current_stations=False):
		self.current_city = city_name
		if drop_current_stations:
			self.current_stations = []

		self.create_stations(self.cites[city_name])

		text_msg = ""
		for station in self.stations:
			text_msg += self.stations[station].get_fuel_price()
		text_msg += "\n\nВыбирите заправку:"
		station_markup = self.create_gas_stations(city_name)
		try:
			self.bot.send_message(self.id, text_msg, reply_markup=station_markup, timeout=15)
			return True
		except:
			return False

	def create_stations(self, url):
		page_text = ""
		try:
			r = requests.get(url)
			page_text = r.text
		except:
			self.sendMsg("Произошла ошибка при получении данных!")
		else:
			if page_text:
				soup_data = BeautifulSoup(page_text, "html.parser")
				table = soup_data.find("table", {"class": "zebra"})
				rows = table.find_all("tr")
				stations = dict()
				for row in rows[1:]:
					cols = row.find_all("td")
					cols = [e.text.strip() for e in cols]
					stations[cols[0]] = FuelStation(cols[0], cols[2:])
				self.stations = stations
				return True
		finally:
			return page_text

	def create_gas_stations(self, city_name):
		column_a = None
		column_b = None
		column_c = None
		column_count = 3

		station_markup = types.InlineKeyboardMarkup()
		stations_lst = list(self.stations.keys())
		# позиционироване елементов по три в ряду
		for i in range(0, len(stations_lst)):
			if i % column_count == 0:
				column_a = types.InlineKeyboardButton(stations_lst[i], callback_data=stations_lst[i])
				if i == (len(stations_lst) - 1):
					station_markup.row(column_a)
			elif i % column_count == 1:
				column_b = types.InlineKeyboardButton(stations_lst[i], callback_data=stations_lst[i])
				if i == (len(stations_lst) - 1):
					station_markup.row(column_a, column_b)
			else:
				column_c = types.InlineKeyboardButton(stations_lst[i], callback_data=stations_lst[i])
				station_markup.row(column_a, column_b, column_c)
		update_btn = types.InlineKeyboardButton(
			f"Обновить данные за город {self.current_city}", callback_data="update_city"
		)
		station_markup.row(update_btn)
		return station_markup


	def show_station(self, name):
		if len(self.stations) > 0:
			self.current_stations.append(self.stations[name])
			text_msg = self.stations[name].get_fuel_price()
			updated_markup = self.create_current_stations("current_stations_update")
			if updated_markup:
				try:
					self.bot.send_message(self.id, text_msg, reply_markup=updated_markup, timeout=15)
					return True
				except ValueError:
					return False
			else:
				self.send_msg(text_msg)
		else:
			return False

	def create_current_stations(self, data):
		if len(self.current_stations) > 0:
			stations_text = ", ".join(self.get_current_stations_names())
			update_btn = types.InlineKeyboardButton(f"Получить данные за заправки: {stations_text}", callback_data=data)
			update_markup = types.InlineKeyboardMarkup()
			update_markup.add(update_btn)
			return update_markup
		else:
			return False

	def get_current_stations_names(self):
		current_stations_names = list()
		[current_stations_names.append(stat.name) for stat in self.current_stations]
		return current_stations_names


	def call_handler(self, call):
		if call.data in self.stations:
			self.show_station(call.data)
		elif call.data == "update_city":
			self.show_city_gas_stations(self.current_city)
		elif call.data == "current_stations_update":
			self.update_stations()
		elif call.data == "drop_stations":
			self.drop_stations()
		else:
			txt = "Я не могу прочитать это собщение. Для того чтобы получить справку нажми '/help'"
			self.echo(txt)

	def update_stations(self):
		self.create_stations(self.cites[self.current_city])
		text_msg = ""
		for station in self.stations:
			if station in self.get_current_stations_names():
				text_msg += self.stations[station].get_fuel_price()
			else:
				pass
		if len(text_msg) > 0:
			update_markup = self.create_current_stations("current_stations_update")
			if update_markup:
				try:
					self.bot.send_message(self.id, text_msg, reply_markup=update_markup, timeout=15)
					return True
				except:
					return False

	def show_cites(self):
		cites_markup = types.ReplyKeyboardMarkup()

		Kyev = types.KeyboardButton("Киев")
		Kharkov = types.KeyboardButton("Харьков")
		Odessa = types.KeyboardButton("Одесса")
		cites_markup.row(Kyev, Kharkov, Odessa)

		Dnepr = types.KeyboardButton("Днепр")
		Lvov = types.KeyboardButton("Львов")
		Zapor = types.KeyboardButton("Запорожье")
		cites_markup.row(Dnepr, Lvov, Zapor)

		Xerson = types.KeyboardButton("Херсон")
		Nick = types.KeyboardButton("Николаев")
		Vinnitza = types.KeyboardButton("Винница")
		cites_markup.row(Nick, Vinnitza, Xerson)

		try:
			self.bot.send_message(self.id, "Выбирите город:", reply_markup=cites_markup, timeout=15)
			return True
		except:
			return False

	def send_msg(self, text):
		if len(text) > 0:
			try:
				self.bot.send_message(self.id, text, timeout=15)
				return True
			except:
				print("Не удалось отправить сообщение Telegram")
				return False
		else:
			return False


	def drop_stations(self):
		self.current_stations = []
		text = "Список выбраных заправок сброшен.\nВаш текущий город {0}".format(self.current_city)
		station_markup = types.InlineKeyboardMarkup()
		update_btn = types.InlineKeyboardButton(f"Обновить данные за город {self.current_city}", callback_data="update_city")
		station_markup.row(update_btn)
		try:
			self.bot.send_message(self.id, text, reply_markup=station_markup, timeout=15)
			return True
		except:
			return False


	def echo(self, message):
		try:
			self.bot.reply_to(message, "Я не могу прочитать это собщение. Для того чтобы получить справку нажми '/help'", timeout=15)
		except ValueError:
			print("Не удалось отправить сообщение Telegram")
	

	def help_handler(self):
		text = """
		Доступные комманды:
		'/start' - начать
		'/city' - показать города
		'/drop' - сбросить заправки
		'/help' - помощь
		"""
		try:
			self.bot.send_message(self.id, text, timeout=15)
			return True
		except:
			return False


Users = dict()
bot = telebot.TeleBot("914190330:AAFOnsItvftbwY2kyTiKPEA8D_ueGHvjNuE")
log = Logging()


@bot.message_handler(commands=['start'])
def send_start(message):
	if message.from_user.id in Users:
		Users[message.from_user.id].show_cites()
		log.update_user(Users[message.from_user.id])
	else:
		Users[message.from_user.id] = FuelUser(bot, message)
		Users[message.from_user.id].show_cites()
		log.write_user(Users[message.from_user.id])


@bot.message_handler(commands=['help'])
def send_start(message):
	if message.from_user.id in Users:
		Users[message.from_user.id].help_handler()
		log.update_user(Users[message.from_user.id])
	else:
		Users[message.from_user.id] = FuelUser(bot, message)
		Users[message.from_user.id].help_handler()
		log.write_user(Users[message.from_user.id])


@bot.message_handler(commands=['city'])
def send_city(message):
	if message.from_user.id in Users:
		Users[message.from_user.id].show_cites()
		log.update_user(Users[message.from_user.id])
	else:
		Users[message.from_user.id] = FuelUser(bot, message)
		Users[message.from_user.id].show_cites()
		log.write_user(Users[message.from_user.id])


@bot.message_handler(commands=['drop'])
def send_drop(message):
	if message.from_user.id in Users:
		Users[message.from_user.id].drop_stations()
		log.update_user(Users[message.from_user.id])
	else:
		Users[message.from_user.id] = FuelUser(bot, message)
		Users[message.from_user.id].drop_stations()
		log.write_user(Users[message.from_user.id])


@bot.message_handler(content_types=['text'])
def text_handler(message):
	if message.from_user.id in Users:
		Users[message.from_user.id].text_handler(message)
		log.update_user(Users[message.from_user.id])
	else:
		Users[message.from_user.id] = FuelUser(bot, message)
		Users[message.from_user.id].text_handler(message)
		log.write_user(Users[message.from_user.id])


@bot.callback_query_handler(func=lambda call: True)
def call_handler(call):
	if call.from_user.id in Users:
		Users[call.from_user.id].call_handler(call)
		log.update_user(Users[call.from_user.id])
	else:
		bot.send_message(call.from_user.id, "Пожалуйста, выберите город.", timeout=15)


bot.polling()


