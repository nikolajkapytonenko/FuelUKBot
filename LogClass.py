from datetime import datetime
import os

class UserLog():
	def __init__(self, user_id, name, 
				first = datetime.today().strftime("%H.%M.%S-%Y-%m-%d"), 
				last_date = datetime.today().strftime("%H.%M.%S-%Y-%m-%d"), 
				use_count = 1):
		self.id = user_id
		self.firstName = name
		self.last_date = last_date
		self.first_date = first
		self.use = int(use_count)
	
	def add_use(self):
		self.use += 1
	
	def __str__(self):
		return f"{self.id} | {self.firstName} | {self.first_date} | {self.last_date} | {self.use}"

class Logging():
	def __init__(self):
		self.file = os.path.join(os.getcwd(), 'FuelLog.csv')
		#self.file = "/home/ubuntu/FuelDir/FuelLog.csv"
	
	def write_file(self, text):
		try:
			ff = open(self.file, "a", encoding="cp1251")
			ff.write(text)
			ff.close()
			return True
		except ValueError:
			print("Не удалось записать файл")
			return False
	
	def rewrite(self, users):
		text = 'ID;Name;First Date; Last Use;Number\n'
		for user in users:
			text += f"{user.id};{user.firstName};{user.first_date};{user.last_date};{user.use};\n"
		try:
			ff = open(self.file, "w", encoding="cp1251")
			ff.write(text)
			ff.close()
			return True
		except ValueError:
			print("Не удалось записать файл")
			return False
	
	def read_file(self):
		f = open(self.file, "r", encoding="cp1251")
		text = f.read()
		text = text.split('\n')
		users = list()
		for line in text[1:-1]:
			user_line = line.split(";")
			users.append(UserLog(user_line[0], user_line[1], user_line[2], user_line[3], user_line[4]))
		return users
	
	def show_file(self):
		f = open(self.file, "r", encoding="cp1251")
		text = f.read()
		text = text.split('\n')
		users = list()
		for line in text[1:-1]:
			user_line = line.split(";")
			users.append(UserLog(user_line[0], user_line[1], user_line[2], user_line[3], user_line[4]))
		[print(u) for u in users]
	
	def exist(self, users, user_id):
		id_list = list()
		[id_list.append(user.id) for user in users]
		return user_id in id_list
	
	def add_user(self, user):
		if self.exist(self.read_file(), str(user.id)):
			print(f"User {user.id} alredy exist!")
		else:
			date = datetime.today().strftime("%H.%M.%S-%Y-%m-%d")
			text = f'{user.id};{user.firstName};{date};{date};{user.use}\n'
			return self.write_file(text)
	
	def update_user(self, user_id):
		users = self.read_file()
		if self.exist(users, user_id):
			for user in users:
				if user_id == user.id:
					user.add_use()
					user.last_date = datetime.today().strftime("%H.%M.%S-%Y-%m-%d")
			self.rewrite(users)
		else:
			print(f"User {user_id} doesn't exist")
		self.show_file()

if __name__ == "__main__":
	log = Logging()
	u = UserLog("3", "Kapiton")
	#log.add_user(u)
	log.update_user("2")

