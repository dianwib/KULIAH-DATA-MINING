import beautipul
import mysql.connector
import sqlite3
conn = sqlite3.connect('otomart.db')
c = conn.cursor()

# Create table
c.execute('DROP TABLE IF EXISTS mobil_bekas')
c.execute('''CREATE TABLE IF NOT EXISTS mobil_bekas
             (merk VARCHAR, model VARCHAR, tipe VARCHAR, harga INTEGER, kota VARCHAR, provinsi VARCHAR, showroom VARCHAR, transmisi VARCHAR, warna VARCHAR, deskripsi VARCHAR)''')


#for i in beautipul.product_dict:
#    print(beautipul.product_dict[i])
