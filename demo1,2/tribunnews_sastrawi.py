
import re
import tribunnews_ambilfitur


from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

data = []
kumpulan_katadasar = ""
a=0
for kalimat in tribunnews_ambilfitur.data:
    a+=1
    print (a,">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print (kalimat)

    kalimat = kalimat.encode('utf-8').strip()

    factory = StopWordRemoverFactory()
    stopword = factory.create_stop_word_remover()
    stop = stopword.remove(kalimat)

    stop = re.sub(r'\b\w{1,2}\b', '', stop)

    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    katadasar = stemmer.stem(str(kalimat))
    katadasar = re.sub(r'\b\w{1,3}\b', '', katadasar).replace('-','')
    print(katadasar)
    data.append(katadasar)
    kumpulan_katadasar = kumpulan_katadasar + katadasar

temp = {}
kal = kumpulan_katadasar.split(" ")
for i in kal:
    if i not in temp:
        temp[i] = 1
    else:
        hasil_sementara = temp[i]
        temp[i] = hasil_sementara + 1


# print (temp)


def list_fitur():
    t = {}
    semua_kata = ""
    for i in data:
        semua_kata = semua_kata + i + " "

    for j in semua_kata.split(" "):
        t[j] = 0

    del t[""]
    return t


def coba1():
    tt = []

    for kalimat in data:
        list_kata = kalimat.split(" ")

        a = list_fitur()
        for kata in list_kata:
            if kata not in list_fitur():
                a[kata] = 0
            else:
                temp = a[kata]
                a[kata] = temp + 1

        tt.append(a)

        # print (kalimat)

        # print (a)
    return tt


print coba1()
print len(list_fitur())
print list_fitur()
print (str(coba1()[2].values()[1]))

