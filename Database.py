import sqlite3
import hashlib
import time

class Database:
	def __init__(self, userId = 0):
		self.userId = userId

	def createTable(self):
		conn = sqlite3.connect("user.db")
		try:	
			conn.execute('''CREATE TABLE IF NOT EXISTS users \
			(user_id INT PRIMARY KEY NOT NULL, \
			name CHAR(50) NOT NULL, \
			key VARCHAR(100) NOT NULL);''')
		except Exception as e:
			print(e)
		else:
			print("Table created successfully")

	def getMaxId(self):
		conn = sqlite3.connect("user.db")
		try:
			cursor = conn.execute("SELECT MAX(user_id) AS id FROM users")
		except Exception as e:
			print(e)
		else:
			curr = list(cursor.fetchone())
			if str(curr[0]) == "None":
				return 0
			else:
				return curr[0]

	def createKey(self, key):
		_key = bytes(str(self.getMaxId()) + key + str(time.time()), encoding = 'utf-8')
		hash_object = hashlib.md5(_key)
		return hash_object.hexdigest()



	def insertUser(self, user_id, name, password):
		conn = sqlite3.connect("user.db")
		try:
			conn.execute("INSERT INTO users VALUES(?, ?, ?);", (user_id, name, self.createKey(password)))
			conn.commit()
		except Exception as e:
			print(e)
		else:
			print("SUCCEED")

	def setUserId(self, userId):
		self.userId = userId

	def getUserId(self):
		return self.userId

	def getKeyFromId(self):
		conn = sqlite3.connect("user.db")
		try:
			cursor = conn.execute("SELECT key FROM users WHERE user_id = ?", (str(self.getUserId())))
		except Exception as e:
			print(e)
		else:
			curr = list(cursor.fetchone())
			return curr[0]

	def getNameFromId(self):
		conn = sqlite3.connect("user.db")
		try:
			cursor = conn.execute("SELECT name FROM users WHERE user_id = ?", (str(self.getUserId())))
		except Exception as e:
			print(e)
		else:
			curr = list(cursor.fetchone())
			return curr[0]

	def showAll(self):
		conn = sqlite3.connect("user.db")
		cursor = conn.execute("SELECT user_id, name, password from users")
		for row in cursor:
			print("ID = ", row[0])
			print("NAME = ", row[1])
			print("PASS = ", row[2], "\n")


if __name__ == "__main__":
	db = Database()
	