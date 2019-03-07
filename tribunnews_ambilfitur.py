import sqlite3
conn = sqlite3.connect('tribunnews.db')
c = conn.cursor()

c.execute('SELECT * FROM berita_gresik')

rows = c.fetchall()

data=[]
for row in rows:
    baris=""
    for j in row:
        j=j.replace(',', '')
        baris=baris+j+" "

    data.append(baris)



#for i in data:
#    print i