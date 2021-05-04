import sqlite3
from prettytable import PrettyTable

base = sqlite3.connect('base.db')
cur = base.cursor()
cur.execute('SELECT * FROM users')
res = cur.fetchall()
x = PrettyTable()
x.field_names = ['id', 'Nickname', 'FName', 'LName', 'Dick','Dick Time']
for i in res:
    x.add_row(i)
print(x)