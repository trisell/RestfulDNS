import sqlite3
with sqlite3.connect('./storage.db') as conn:
	cursor = conn.cursor()

	sql = 'create table users(id INT PRIMARY KEY, username TEXT CHAR(32), password_hash TEXT CHAR(64))'
	cursor.execute(sql)
	conn.commit()