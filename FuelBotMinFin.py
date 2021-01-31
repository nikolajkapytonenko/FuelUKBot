import requests
from bs4 import BeautifulSoup

import telebot
from telebot import types

from LogClass import Logging
from datetime import datetime

class FuelStation():
	def __init__(self, name, prises_list):
		self.name = name
		self.prises = dict()
		#self.prises["A98"] = prises_list[1]
		self.prises["A95+"] = prises_list[0]
		self.prises["A95"] = prises_list[1]
		self.prises["A92"] = prises_list[2]
		#self.prises["A80"] = prises_list[5]
		self.prises["ДТ"] = prises_list[3]
		#self.prises["ДТ+"] = prises_list[7]
		self.prises["ГАЗ"] = prises_list[4]
	
	def __str__(self):
		return self.name
	
	def get_stations(self):
		return self.name
	
	def get_fuel(self):
		keys = []
		[keys.append(key) for key in self.prises]
		return keys
		
	def get_data(self):
		text = "\n" + self.name + ":\n"
		i = 0
		for fuel in self.prises:
			if self.prises[fuel] != "-":
				text += f"{fuel}: {self.prises[fuel]};   "
				i += 1
			else:
				pass
		#text += "\n"# + "~"*50
		return text

'''
cites = {"Киев":"https://avtomaniya.com/benzin",
		"Одесса":"https://avtomaniya.com/site/fuel-odessa",
		"Днепр":"https://avtomaniya.com/site/fuel-dnepr",
		"Харьков":"https://avtomaniya.com/site/fuel-kharkov",
		"Львов":"https://avtomaniya.com/site/fuel-lviv"}
'''
class FuelUser():
	def __init__(self, bot, message,
				first_date = datetime.today().strftime("%H.%M.%S-%Y-%m-%d"),
				last_date = datetime.today().strftime("%H.%M.%S-%Y-%m-%d")):
		self.bot = bot
		self.message = message
		self.id = self.message.from_user.id
		self.firstName = self.message.from_user.first_name
		self.stations = dict()
		
		self.curent_city = ""
		self.curent_stations = list()
		
		self.use = 1
		self.last_date = last_date
		self.first_date = first_date
		
		'''
		self.cites = {"Киев":"https://avtomaniya.com/benzin",
			"Одесса":"https://avtomaniya.com/site/fuel-odessa",
			"Днепр":"https://avtomaniya.com/site/fuel-dnepr",
			"Харьков":"https://avtomaniya.com/site/fuel-kharkov",
			"Львов":"https://avtomaniya.com/site/fuel-lviv"}
		
		self.cites = {"Киев обл.":"https://index.minfin.com.ua/markets/fuel/reg/kievskaya/",
			"Одесса обл.":"https://index.minfin.com.ua/markets/fuel/reg/odesskaya/",
			"Днепр обл.":"https://index.minfin.com.ua/markets/fuel/reg/dnepropetrovskaya/",
			"Харьков обл.":"https://index.minfin.com.ua/markets/fuel/reg/harkovskaya/",
			"Львов обл.":"https://index.minfin.com.ua/markets/fuel/reg/lvovskaya/",
			"Запорожье обл.":"",
			"Винница обл.":"",
			"Полтава обл.":"",
			"Ивано-Франковск обл.":"",
			"Хмельницк обл.":"",
			"Ужгород обл.":"",
			"Житомир обл.":"",
			"Черкассы обл.":"",
			"Ровно обл.":"",
			"Николаев обл.":"",
			"Суммы обл.":"",
			"Тернополь обл.":"",
			"Херсон обл.":"",
			"Луцк обл.":"",
			"Чернигов обл.":"",
			"Кировоград обл.":"",
			"Черновцы обл.":""}
		'''
		
		self.cites = {"Киев":"https://index.minfin.com.ua/markets/fuel/reg/kievskaya/",
			"Одесса":"https://index.minfin.com.ua/markets/fuel/reg/odesskaya/",
			"Днепр":"https://index.minfin.com.ua/markets/fuel/reg/dnepropetrovskaya/",
			"Харьков":"https://index.minfin.com.ua/markets/fuel/reg/harkovskaya/",
			"Львов":"https://index.minfin.com.ua/markets/fuel/reg/lvovskaya/",
			"Запорожье":"https://index.minfin.com.ua/markets/fuel/reg/zaporozhskaya/",
			"Херсон":"https://index.minfin.com.ua/markets/fuel/reg/hersonskaya/",
			"Николаев":"https://index.minfin.com.ua/markets/fuel/reg/nikolaevskaya/",
			"Винница":"https://index.minfin.com.ua/markets/fuel/reg/vinnickaya/"}
			
	def echo(self, message):
		try:
			self.bot.reply_to(message, "Я не могу прочитать это собщение. Для того чтобы получить справку нажми '/help'", timeout=15)
		except ValueError:
				print("Не удалось отправить сообщение Telegram")
	
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
			self.bot.send_message(self.id, "Выбирите город:", 
				reply_markup=cites_markup, timeout=15)
			return True
		except ValueError:
			return False
	
	def send_msg(self, text):
		if len(text) > 0:
			try:
				self.bot.send_message(self.id, text, timeout=15)
				return True
			except ValueError:
				print("Не удалось отправить сообщение Telegram")
				return False
		else:
			return False
	
	def get_curent_stations_names(self):
		curent_stations_names = list()
		[curent_stations_names.append(stat.name) for stat in self.curent_stations]
		return curent_stations_names
	
	def create_stations(self, url):
		#self.stations = dict()
		page_text = ""
		try:
			r = requests.get(url)
			page_text = r.text
		except ValueError:
			self.sendMsg("Произошла ошибка при получении данных!")
			return False
		if len(page_text)>1:
			soup = BeautifulSoup(page_text, "html.parser")
			table = soup.find("table", {"class": "zebra"})
			rows = table.find_all("tr")
			Stations = dict()
			for row in rows[1:]:
				cols = row.find_all("td")
				cols = [e.text.strip() for e in cols]
				Stations[cols[0]] = FuelStation(cols[0], cols[2:])
			self.stations = Stations
			return True
		else:
			return False
	
	def city(self, city_name, drop_curent_stations=False):
		self.curent_city = city_name
		if drop_curent_stations:
			self.curent_stations = []
		
		self.create_stations(self.cites[city_name])
		
		text_msg = ""
		for station in self.stations:
			text_msg += self.stations[station].get_data()
		text_msg +="\n\nВыбирите заправку:"
		station_markup = types.InlineKeyboardMarkup()
		'''
		[station_markup.add(types.InlineKeyboardButton(station, callback_data=station)) 
			for station in self.stations]
		'''
		a = None
		b = None
		c = None
		stations_lst = list(self.stations.keys())
		for i in range(0, len(stations_lst)):
			if i%3 == 0:
				a = types.InlineKeyboardButton(stations_lst[i], callback_data=stations_lst[i])
				if i == len(stations_lst)-1:
					station_markup.row(a)
			elif i%3 == 1:
				b = types.InlineKeyboardButton(stations_lst[i], callback_data=stations_lst[i])
				if i == len(stations_lst )-1:
					station_markup.row(a, b)
			else:
				c = types.InlineKeyboardButton(stations_lst[i], callback_data=stations_lst[i])
				station_markup.row(a, b, c)
		update_btn = types.InlineKeyboardButton(f"Обновить данные за город {self.curent_city}", callback_data="update_city")
		station_markup.row(update_btn)
		try:
			self.bot.send_message(self.id, text_msg, 
				reply_markup=station_markup, timeout=15)
			return True
		except ValueError:
			return False
	
	def create_curent_stations(self, data):
		if len(self.curent_stations) > 0:
			stations_text = ", ".join(self.get_curent_stations_names())
			update_btn = types.InlineKeyboardButton(f"Получить данные за заправки: {stations_text}", callback_data=data)
			update_markup = types.InlineKeyboardMarkup()
			update_markup.add(update_btn)
			return update_markup
		else:
			return False
	
	def station(self, name):
		if len(self.stations) > 0:
			self.curent_stations.append(self.stations[name])
			text_msg = self.stations[name].get_data()
			#self.send_msg(text_msg)
			update_markup = self.create_curent_stations("curent_stations_update")
			if update_markup != False:
				try:
					self.bot.send_message(self.id, text_msg, 
						reply_markup=update_markup, timeout=15)
					return True
				except ValueError:
					return False
			else:
				self.send_msg(text_msg)
		else:
			return False
	
	def update_stations(self):
		self.create_stations(self.cites[self.curent_city])
		text_msg = ""
		for station in self.stations:
			if station in self.get_curent_stations_names():
				text_msg += self.stations[station].get_data()
			else:
				pass
		#print(text_msg)
		if len(text_msg) > 0:
			update_markup = self.create_curent_stations("curent_stations_update")
			if update_markup != False:
				try:
					self.bot.send_message(self.id, text_msg, 
						reply_markup=update_markup, timeout=15)
					return True
				except ValueError:
					return False
	
	def drop_stations(self):
		self.curent_stations = []
		text = "Список выбраных заправок сброшен"
		station_markup = types.InlineKeyboardMarkup()
		update_btn = types.InlineKeyboardButton(f"Обновить данные за город {self.curent_city}", callback_data="update_city")
		station_markup.row(update_btn)
		try:
			self.bot.send_message(self.id, text, 
				reply_markup=station_markup, timeout=15)
			return True
		except ValueError:
			return False
		
	
	def text_handler(self, message):
		'''
		Обработчик текстовых сообщений
		'''
		if message.text in self.cites:
			self.city(message.text, drop_curent_stations=True)
		# походу до этого дело не доходит
		elif message.text in self.stations:
			self.station(message.text)
		elif message.text == "drop":
			self.drop_stations()
		else:
			self.echo(message)
	
	def call_handler(self, call):
		'''
		Обработчик текстовых сообщений
		'''
		if call.data in self.stations:
			self.station(call.data)
		elif call.data == "update_city":
			self.city(self.curent_city)
		elif call.data == "curent_stations_update":
			self.update_stations()
		elif call.data == "drop_stations":
			self.drop_stations()
		else:
			pass#self.echo_call(call)
	
	def add_use(self):
		self.use += 1


Users = dict()
bot = telebot.TeleBot("914190330:AAFOnsItvftbwY2kyTiKPEA8D_ueGHvjNuE")
log = Logging()

@bot.message_handler(commands=['start'])
def send_start(message):
	if message.from_user.id in Users:
		Users[message.from_user.id].show_cites()
		log.update_user(str(message.from_user.id))
		print(f"Старый пользователь {Users[message.from_user.id].firstName} (start) !")
	else:
		Users[message.from_user.id] = FuelUser(bot, message)
		Users[message.from_user.id].show_cites()
		log.add_user(Users[message.from_user.id])
		print(f"ДОБАВЛЕН НОВЫЙ ПОЛЬЗОВАТЕЛЬ {Users[message.from_user.id].firstName} (start)")

@bot.message_handler(commands=['city'])
def send_city(message):
	if message.from_user.id in Users:
		Users[message.from_user.id].show_cites()
		log.update_user(str(message.from_user.id))
		print(f"Старый пользователь {Users[message.from_user.id].firstName} (city) !")
	else:
		Users[message.from_user.id] = FuelUser(bot, message)
		Users[message.from_user.id].show_cites()
		log.add_user(Users[message.from_user.id])
		print(f"ДОБАВЛЕН НОВЫЙ ПОЛЬЗОВАТЕЛЬ {Users[message.from_user.id].firstName} (city)")

@bot.message_handler(commands=['drop'])
def send_drop(message):
	if message.from_user.id in Users:
		Users[message.from_user.id].drop_stations()
		log.update_user(str(message.from_user.id))
		print(f"Старый пользователь {Users[message.from_user.id].firstName} (city) !")
	else:
		Users[message.from_user.id] = FuelUser(bot, message)
		Users[message.from_user.id].drop_stations()
		log.add_user(Users[message.from_user.id])
		print(f"ДОБАВЛЕН НОВЫЙ ПОЛЬЗОВАТЕЛЬ {Users[message.from_user.id].firstName} (city)")

@bot.message_handler(content_types=['text'])
def text_handler(message):
	'''
	Обработчик текстовых сообщений
	'''
	if message.from_user.id in Users:
		Users[message.from_user.id].text_handler(message)
		log.update_user(str(message.from_user.id))
		print(f"Старый пользователь {Users[message.from_user.id].firstName} (text) !")
	else:
		Users[message.from_user.id] = FuelUser(bot, message)
		Users[message.from_user.id].text_handler(message)
		log.add_user(Users[message.from_user.id])
		print(f"ДОБАВЛЕН НОВЫЙ ПОЛЬЗОВАТЕЛЬ {Users[message.from_user.id].firstName} (text)")

@bot.callback_query_handler(func=lambda call: True)
def call_handler(call):
	#bot.send_message(call.from_user.id, call.data)
	'''
	Обработчик 
	'''
	if call.from_user.id in Users:
		Users[call.from_user.id].call_handler(call)
		log.update_user(str(call.from_user.id))
		print(f"Старый пользователь {Users[call.from_user.id].firstName} (call) !")
	else:
		bot.send_message(call.from_user.id, "Пожалуйста, выберите город.", timeout=15)
		'''
		#Users[call.from_user.id].show_cites()
		Users[call.from_user.id] = FuelUser(bot)
		Users[call.from_user.id].call_handler(call)
		log.add_user(Users[message.from_user.id])
		print(f"ДОБАВЛЕН НОВЫЙ ПОЛЬЗОВАТЕЛЬ {Users[call.from_user.id].firstName} (call)")
		'''

bot.polling()
