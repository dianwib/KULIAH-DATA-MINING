import url_2
from bs4 import BeautifulSoup

soup=BeautifulSoup(url_2.html,"lxml")

import sqlite3
conn = sqlite3.connect('berita.db')
c = conn.cursor()

# Create table
c.execute('DROP TABLE IF EXISTS berita_gresik')
c.execute('''CREATE TABLE IF NOT EXISTS berita_gresik
             (tanggal VARCHAR, judul VARCHAR, isi VARCHAR)''')
conn.commit()

# Insert a row of data







produk = soup.find_all("li","p2030") #class yang kan difilter pada inspect element #div=tag html / box car==classnya
a=0
for p in produk:
    a+=1
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",a)
    # print(p.find('h3','car-name-blue').get_text())#merk

    waktu = p.find('time', 'grey pt5').get_text()
    waktu=waktu.strip()
    print(waktu)

    berita = p.find('h3', 'f20 ln24 fbo').get_text()
    berita=berita.replace('\n', '').replace('\t\t', '').replace(',', '')
    berita=berita.strip()
    print(berita)
    isi = p.find('h4', 'black pt5').get_text()
    isi=isi.strip()
    print(isi)
    c.execute(
        "INSERT INTO berita_gresik (tanggal, judul,isi) values ( ?, ?,?)",
        (waktu,berita,isi))
    conn.commit()

conn.close()