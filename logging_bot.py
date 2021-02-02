from datetime import datetime
import os
from user import User


class Logging:
	def __init__(self):
		self.file = os.path.join(os.getcwd(), 'FuelLog.csv')

	def write_user(self, client):
		if self.reside(self.get_users(), client):
			print(f"User {client.id} already exist!")
		else:
			date = datetime.today().strftime("%H.%M.%S-%Y-%m-%d")
			text = f'{client.id};{client.firstName};{date};{date};{client.use}\n'
			return self.write_log(text)

	def reside(self, users, client):
		id_list = list()
		[id_list.append(user.id) for user in users]
		return str(client.id) in id_list

	def write_log(self, text):
		try:
			f = open(self.file, "a", encoding="cp1251")
			f.write(text)
		except:
			print("Не удалось записать лог")
			return False
		finally:
			f.close()
			return True


	def update_user(self, client):
		users = self.get_users()
		if self.reside(users, client):
			for user in users:
				if client.id == user.id:
					user.increase_actions()
					user.last_date = datetime.today().strftime("%H.%M.%S-%Y-%m-%d")
			self.rewrite_users(users)
		else:
			print(f"User {client.id} doesn't exist")

	def get_users(self):
		text = self.read_file()
		users = list()
		for line in text:
			user_line = line.split(";")
			users.append(User(user_line[0], user_line[1], user_line[2], user_line[3], user_line[4]))
		return users

	def read_file(self):
		f = open(self.file, "r", encoding="cp1251")
		try:
			text = f.read()
		except:
			print("Не удалось считать файл!")
			return False
		finally:
			text = text.split('\n')
			return text[1:-1]
	
	def rewrite_users(self, users):
		text = 'ID;Name;First Date; Last Use;Number\n'
		for user in users:
			text += f"{user.id};{user.firstName};{user.first_date};{user.last_date};{user.use};\n"
		try:
			f = open(self.file, "w", encoding="cp1251")
			f.write(text)
		except:
			print("Не удалось записать файл")
			return False
		finally:
			f.close()
			return True



	def _show_file(self):
		text = self.read_file()
		users = list()
		for line in text:
			user_line = line.split(";")
			users.append(User(user_line[0], user_line[1], user_line[2], user_line[3], user_line[4]))
		[print(u) for u in users]
	

if __name__ == "__main__":
	log = Logging()
	u = User("474464039", "Kapiton")
	print(u)
	#log.write_user(u)
	log.update_user(u)

