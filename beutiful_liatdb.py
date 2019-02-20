import sqlite3
conn = sqlite3.connect('otomart.db')
c = conn.cursor()

c.execute('SELECT * FROM mobil_bekas')

meida = c.fetchall()

for i in meida:
    print (i)
