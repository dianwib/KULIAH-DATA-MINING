import xlsxwriter
import math
import xlrd
excel = xlrd.open_workbook("tribunnews_vsmsatufitur.xlsx")
sheetdata = excel.sheet_by_index(0)
'''
data.name = nama sheet
data.nrows = jumah baris
data.ncols = jumlah kolom
'''



def banyak_kata():
    frekuensi_list = []
    for baris in range(1,3):
        dict_data={}
        for kolom in range(1,sheetdata.ncols):
            value = sheetdata.cell_value(rowx=baris, colx=kolom)
            #print ("value",value)
            value_fitur = sheetdata.cell_value(rowx=0, colx=kolom)
            #print ("fitur",value_fitur)
            dict_data[str(value_fitur)]=value
            #print (dict_data)

            temp={"doc_id":baris,"frekuensi":dict_data}

        frekuensi_list.append(temp)
    return frekuensi_list


print (banyak_kata())


def panjang_tiap_data(baris):
    excel_baru = xlrd.open_workbook("tribunnews_daftarsteaming.xlsx")
    sheetdata_baru = excel_baru.sheet_by_index(0)
    '''
    data.name = nama sheet
    data.nrows = jumah baris
    data.ncols = jumlah kolom
    '''
    value = sheetdata_baru.cell_value(rowx=baris, colx=2)
    kalimat=value.split(" ")
    return len(kalimat)


def hitung_tf():
    tf_number=[]

    for data in banyak_kata():
        id = data["doc_id"]
        #print (id)

        for i in data["frekuensi"]:
            temp={"doc_id":id, "TF score":data["frekuensi"][i]/panjang_tiap_data(id),"key":i}

            tf_number.append(temp)

    return tf_number

def hitung_idf():
    workbook = xlsxwriter.Workbook('tribunnews_idf.xlsx')
    worksheetidf = workbook.add_worksheet()
    idf_number=[]
    iterasi=1

    for data in banyak_kata():
        id = data["doc_id"]
        print (id)
        kolom = 1

        for i in data["frekuensi"].keys():
            count=sum([i in data["frekuensi"] for data in banyak_kata()])
            #print (data)
            #print (panjang_tiap_data(id))
            #print (count)
            fitur= float(math.log(panjang_tiap_data(id))/count)
            temp={"doc_id":iterasi,"IDF score": math.log(panjang_tiap_data(id))/count,"key":i}
            worksheetidf.write(iterasi, kolom, fitur)
            idf_number.append(temp)
            kolom+=1

        iterasi+=1
    workbook.close()
    return idf_number
print (hitung_idf())

def hitung_tfidf():
    tfidf_number=[]
    for data_j in hitung_idf():
        for data_i in hitung_tf():
            if data_j ["key"]==data_i["key"] and data_j["doc_id"]==data_i["doc_id"]:

                temp={"doc_id":data_j["doc_id"],"TFIDF score":data_j["IDF score"]*data_i["TF score"],"key":data_i["key"]}

        tfidf_number.append(temp)

    return tfidf_number





