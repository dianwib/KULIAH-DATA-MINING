import xlsxwriter
import re
import beutiful_liatdb


import xlwt,sys, time,operator,xlrd
import math
from random import randint
from xlutils.copy import copy





'''
data.name = nama sheet
data.nrows = jumah baris
data.ncols = jumlah kolom
'''


from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

data=[]
kumpulan_katadasar=""
for kalimat in beutiful_liatdb.data:
    print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print (kalimat)
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    kalimat=kalimat.encode('utf-8').strip()
    katadasar = stemmer.stem(str(kalimat))


    factory = StopWordRemoverFactory()
    stopword = factory.create_stop_word_remover()
    stop = stopword.remove(katadasar)


    stop=re.sub(r'\b\w{1,3}\b', '', stop)
    print(stop)
    data.append(stop)
    kumpulan_katadasar=kumpulan_katadasar+stop


temp={}
kal=kumpulan_katadasar.split(" ")
for i in kal:
    if i not in temp:
        temp[i]=1
    else:
        hasil_sementara=temp[i]
        temp[i]=hasil_sementara+1

#print (temp)



def list_fitur():

    t={}
    semua_kata=""
    for i in  data:
        semua_kata=semua_kata+i+" "

    for j in semua_kata.split(" "):
        t[j]=0

    del t[""]
    return t

def coba1():
    tt=[]

    for kalimat in data:
        list_kata=kalimat.split(" ")

        a=list_fitur()
        for kata in list_kata:
            if kata not in list_fitur():
                a[kata]=0
            else:
                temp=a[kata]
                a[kata]=temp+1

        tt.append(a)

        #print (kalimat)

        #print (a)
    return tt

print coba1()
print len(list_fitur())
print list_fitur()
print (str(coba1()[2].values()[1]))



workbook=xlsxwriter.Workbook('databerita_gresik_full400fitur.xlsx')
worksheet1=workbook.add_worksheet()



for i in range(len(list_fitur())):
    #print i
    fitur=str (list_fitur().keys()[i])
    #print fitur
    worksheet1.write(0,i+1,str(fitur))

print (len(data))
for baris in range(len(data)):
    for kolom in range(len(list_fitur())):
        fitur=coba1()[baris].values()[kolom]
        print ("data ke > "+str(baris+1)+" kata "+str(coba1()[baris].keys()[kolom])+" sebanyak "+ str(coba1()[baris].values()[kolom]))
        worksheet1.write(baris+1, kolom+1, str(fitur))
workbook.close()

