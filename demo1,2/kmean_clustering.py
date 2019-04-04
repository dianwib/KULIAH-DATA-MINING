import xlwt,sys, time,operator,xlrd
import math
from random import randint
from PySide.QtGui import *
from PySide.QtCore import *
from xlutils.copy import copy
'''
data.name = nama sheet
data.nrows = jumah baris
data.ncols = jumlah kolom
'''



class SampleWindow(QWidget):

    def __init__(self):
        super(SampleWindow, self).__init__()
        self.initGUI()

    def SetLayout(self):
        self.hasil_sebelumnya = {}
        self.total_langkah=1

        formLayout = QFormLayout(self)
        self.x1text=QLabel("")
        self.x2text = QLabel("Masukkan jumlah cluster")

        self.banyakcluster = QLineEdit()


        self.okbutton=QPushButton("Calculate")

        formLayout.addRow(self.x1text)
        formLayout.addRow(self.x2text,self.banyakcluster)
        formLayout.addRow(self.okbutton)
        self.connect(self.okbutton, SIGNAL("clicked()"), self.cek)
        self.setLayout(formLayout)




    def cek(self):
        self.total_cluster = int(self.banyakcluster.text())
        excel = xlrd.open_workbook("tribunnews_rabu.xlsx")
        self.data = excel.sheet_by_index(0)
        self.excel_baru = xlwt.Workbook()
        self.sheetcenteroid = self.excel_baru.add_sheet("centeroid")
        self.sheetdatatesting = self.excel_baru.add_sheet("datatesting")


        for i in range(self.total_cluster):
            self.sheetdatatesting.row(0).write(i + 1, "ED x"+str(i+1))
            #self.sheetcenteroid.row(0).write(i + 1, "x" + str(i+1))
            self.sheetcenteroid.row(i+1).write(0, "Centroid /rata M" + str(i+1))

        for i in range(self.data.nrows-1):
            self.sheetdatatesting.row(i+1).write(0,str(i+1))

        for i in range(self.data.ncols - 1):
            self.sheetcenteroid.row(0).write(i+1, "x" + str(i+1))

        self.sheetdatatesting.row(0).write(0, "objek")


        self.excel_baru.save("test.xlsx")
        print(">>>>>>>>>>>>>>>>>>> langkah ke", self.total_langkah, " >>>>>>>>>>>>>>>>>>>")
        if self.total_langkah==1:

            self.cari_random_cluster()
        else:
            self.cari_centeroid()



    def cari_random_cluster(self):
        self.cluster=[]

        while len(self.cluster) != self.total_cluster:
            temp=randint(1,self.data.nrows-1)
            if temp not in self.cluster:
                self.cluster.append(temp)
            else:
                continue
        print("===========================")
        print("langkah 1 objek random :",self.cluster)
        print("===========================")
        self.cari_centeroid()
        return self.cluster


    def cari_centeroid(self):
        excel = xlrd.open_workbook("test.xlsx")
        data = excel.sheet_by_index(1)

        if self.total_langkah==1:
            for i in range (1,self.total_cluster+1):
                #cetak ke file xlxs sheet centeroid
                row=self.sheetcenteroid.row(i)
                for j in range(1,self.data.ncols):
                    value_data=self.data.cell_value(rowx=self.cluster[i-1], colx=j)
                    row.write(j, value_data)

        else:

            for i in range(1,self.total_cluster+1):
                row = self.sheetcenteroid.row(i)
                for j in range(1, self.data.ncols):
                    temp=0
                    for objek in self.hasil_sebelumnya[i] :# hitung rata


                        value = self.data.cell_value(rowx=objek, colx=j)
                        temp=value+temp

                    print("rata=",temp,"/",len(self.hasil_sebelumnya[i]))
                    value_data = (temp / len(self.hasil_sebelumnya[i]))
                    row.write(j, value_data)
                    print("centeroid M",i, "x",j,"=",value_data)



        self.excel_baru.save("tribunnews_kmean.xlsx")
        self.calc_cluster(self.data)

    def ED(self,excelbarusheetcenteroid,baris,data):
        hasil_baris = []
        for i in range(1,self.total_cluster+1):
            baris_centeroid=i

            tem=0
            for j in range (1,self.data.ncols):
                a=excelbarusheetcenteroid.cell_value(rowx=baris_centeroid, colx=j)
                print("(",a,"-",data.cell_value(rowx=baris, colx=j),")^2")
                print (type(data.cell_value(rowx=baris, colx=j)))
                tem=((a- data.cell_value(rowx=baris, colx=j)) **2 ) + tem
            hasil=math.sqrt(tem)
            print("nilai ED dari baris ke:",baris,"ke pusat:",i,"hasil=",hasil)
            print("_______________________________________________________________________________")
            hasil_baris.append(hasil)

        return hasil_baris
#konversi dr dict ke excel
    def calc_cluster(self,data_sheet):
        self.list_ED={}
        for i in range(1,data_sheet.nrows):
            baris=i
            self.buka_excel_baru=xlrd.open_workbook("tribunnews_kmean.xlsx")
            self.buka_sheet_centeroid=self.buka_excel_baru.sheet_by_index(0)
            self.buka_sheet_datatesting = self.buka_excel_baru.sheet_by_index(1)
            self.list_ED[baris]=self.ED(self.buka_sheet_centeroid,baris,self.data)
            self.cetak_hasilED(self.list_ED,baris,self.sheetdatatesting)


        self.cek_pindah()

        for i in self.list_ED:
            print(i,self.list_ED[i])

    def cetak_hasilED(self,list_ED,baris,sheet):

        for i in range(self.total_cluster):
            value_data = list_ED[baris][i]
            sheet.row(baris).write(i+1, value_data)
        self.excel_baru.save("tribunnews_kmean.xlsx")

    def cek_pindah(self):#cek antar objek ke pusat
        excel = xlrd.open_workbook("tribunnews_kmean.xlsx")
        data = excel.sheet_by_index(1)

        hasil={}
        for i in range(1,self.total_cluster+1):
            tampung=[]
            for baris in range(1,data.nrows):
                temp = []
                for j in range(1, self.total_cluster+1):
                    tem_data = data.cell_value(rowx= baris,colx=j)
                    temp.append(tem_data)

                cek_kecil_antar_cluster = min(temp)
                index = temp.index(cek_kecil_antar_cluster)+1

                if i == 1:
                    print("baris",baris,temp,cek_kecil_antar_cluster, "pada index",index)

                # cetak ke kluster
                #data_sheet.row(baris).write(data_sheet.ncols, index)
                if index==i:
                    tampung.append(baris)

                hasil[i]=tampung

        print(hasil,"hasil")
        self.excel_baru.save("tribunnews_kmean.xlsx")

        print("hasil sebelumnya",self.hasil_sebelumnya," ||  hasilbaru",hasil)

        if hasil != self.hasil_sebelumnya:
            print("tidak")


            self.hasil_sebelumnya = hasil
            self.total_langkah+=1
            return self.cek()

        elif hasil == self.hasil_sebelumnya:
            print("sama dan sudah",self.total_langkah,"langkah")
            print("===========================")
            print("index random :", self.cluster)
            print("===========================")
            for i in self.hasil_sebelumnya:
                print("____________________________________________________________")
                print("cluster ke:",i,"total:",len(self.hasil_sebelumnya[i]),"objek")
                print(">>",self.hasil_sebelumnya[i])

            #cetak value klastre kolom terakhir ke excel
            excel = xlrd.open_workbook("tribunnews_kmean.xlsx")
            data = excel.sheet_by_index(1)
            for baris in range(1,data.nrows):
                value_data = []
                for i in range(1, data.ncols):
                    value_data.append(data.cell_value(rowx=baris, colx=i))
                min_data = min(value_data)
                value_data = value_data.index(min_data) + 1
                self.sheetdatatesting.row(baris).write(data.ncols, value_data)

                self.excel_baru.save("tribunnews_kmean.xlsx")
            exit()


        else:
            print("eror")
            exit()


    def initGUI(self):
        self.setWindowTitle("INI JUDUL")
        self.setGeometry(400, 400, 600, 200)  # ukuran layar

        self.SetLayout()
        self.show()


if __name__ == '__main__':
    try:
        myApp = QApplication(sys.argv)
        myWindow = SampleWindow()
        myWindow.show()
        myApp.exec_()
        sys.exit(0)
    except NameError:
        print("Name Error:", sys.exc_info()[1])
    except SystemExit:  # muncul print ketika di exit
        print("Closing Window")
    except Exception:
        print(sys.exc_info()[1])
