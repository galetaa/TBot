import sqlite3
base = sqlite3.connect('base.db')
cur = base.cursor()
cur.execute('SELECT last_dick_request FROM users WHERE user_id =410718594')
print(cur.fetchall()[0][0])