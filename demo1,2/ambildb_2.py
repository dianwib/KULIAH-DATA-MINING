import sqlite3
conn = sqlite3.connect('tribunnews.db')
c = conn.cursor()

c.execute('SELECT * FROM berita_gresik')

meida = c.fetchall()

for i in meida:
    print (i)

