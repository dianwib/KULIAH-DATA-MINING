import xlwt,sys, time,operator,xlrd
import math
from random import randint
from PySide.QtGui import *
from PySide.QtCore import *
from xlutils.copy import copy
import random

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
        self.x1text=QLabel("Masukkan Jumlah Iterasi / Langkah")
        self.x2text = QLabel("Masukkan Jumlah Cluster")
        self.x3text = QLabel("Masukkan Jumlah Pangkat")
        self.x4text = QLabel("Masukkan Jumlah Error")

        self.banyakcluster = QLineEdit()
        self.banyakiterasi = QLineEdit()
        self.banyakerror = QLineEdit()
        self.banyakpangkat = QLineEdit()

        self.okbutton=QPushButton("Calculate")

        formLayout.addRow(self.x1text,self.banyakiterasi)
        formLayout.addRow(self.x2text,self.banyakcluster)
        formLayout.addRow(self.x3text, self.banyakpangkat)
        formLayout.addRow(self.x4text, self.banyakerror)

        formLayout.addRow(self.okbutton)

        self.connect(self.okbutton, SIGNAL("clicked()"), self.cek)
        self.setLayout(formLayout)




    def cek(self):
        self.total_cluster = int(self.banyakcluster.text())
        self.banyak_iterasi= int(self.banyakiterasi.text())
        self.banyak_error=float(self.banyakerror.text())
        x=float(self.banyakpangkat.text())
        self.pangkat= x/(x-1)
        print(self.pangkat)
        excel = xlrd.open_workbook("tribunnews_rabu.xlsx")
        self.data = excel.sheet_by_index(0)
        self.excel_baru = xlwt.Workbook()
        self.sheetcenteroid = self.excel_baru.add_sheet("centeroid")
        self.sheetdatatesting = self.excel_baru.add_sheet("datatesting_random")
        self.sheetdatatesting_C = self.excel_baru.add_sheet("datatesting_UPDATE")

        for i in range(self.total_cluster):
            self.sheetdatatesting.row(0).write(i + 1, "C"+str(i+1))
            self.sheetcenteroid.row(i+1).write(0, "Centroid ke " + str(i+1))
            self.sheetdatatesting_C.row(0).write(i + 1, "UPDATE C" + str(i + 1))

        for i in range(self.data.nrows-1):
            self.sheetdatatesting.row(i+1).write(0,str(i+1))
            self.sheetdatatesting_C.row(i + 1).write(0, str(i + 1))

        for i in range(self.data.ncols - 1):
            self.sheetcenteroid.row(0).write(i+1, "x" + str(i+1))

        self.sheetdatatesting.row(0).write(0, "objek")
        self.sheetdatatesting_C.row(0).write(0, "objek")

        self.excel_baru.save("tribunnews_cmean.xlsx")
        print(">>>>>>>>>>>>>>>>>>> langkah ke", self.total_langkah, " >>>>>>>>>>>>>>>>>>>")

        if self.total_langkah==1:
            self.isi_data_random()
        else:
            self.cari_pusat_norandom()

    def isi_data_random(self):

        for baris in range(1,self.data.nrows):
            for kolom in range (1,self.total_cluster+1):
                value_random=round(random.uniform(0.1,0.9),1)
                self.sheetdatatesting.row(baris).write(kolom, value_random)


                self.excel_baru.save("tribunnews_cmean.xlsx")

        self.cari_pusat()

    def cari_pusat(self):
        excel = xlrd.open_workbook("tribunnews_cmean.xlsx")
        sheetdatabaru = excel.sheet_by_index(1)

        self.cluster={}

        for kluster in range(1,self.total_cluster+1):
            atas=0
            bawah=0
            temp_kluster=[]

            a = []
            for j in range(self.data.ncols-1):##gaguna
                a.append(0)

            for data in range(1,self.data.nrows):

                for kolom in range(1,self.data.ncols):
                    temp_atas=(sheetdatabaru.cell_value(rowx=data, colx=kluster)**self.pangkat) * self.data.cell_value(rowx=data, colx=kolom)

                    a[kolom-1]=a[kolom-1]+temp_atas



                temp_bawah=sheetdatabaru.cell_value(rowx=data, colx=kluster)**self.pangkat
                bawah=bawah+temp_bawah

            for i in range (len(a)):
                a[i]=a[i]/bawah

            self.cluster[kluster]=a


        print(self.cluster)

        for kluster in self.cluster:
            print("kluster ke",kluster,"titik >>>>",self.cluster[kluster])
            for j in range(1,self.data.ncols):
                value = self.cluster[kluster][j-1]

                self.sheetcenteroid.row(kluster).write(j, value)


        self.excel_baru.save("tribunnews_cmean.xlsx")
        self.update_objek()

    def cari_pusat_norandom(self):

        self.cluster={}

        for kluster in range(1,self.total_cluster+1):
            atas=0
            bawah=0
            temp_kluster=[]

            a = []
            for j in range(self.data.ncols-1):##gaguna
                a.append(0)

            for data in range(1,self.data.nrows):

                for kolom in range(1,self.data.ncols):
                    temp_atas=(self.hasil_update[data][kluster-1]**self.pangkat) * self.data.cell_value(rowx=data, colx=kolom)

                    a[kolom-1]=a[kolom-1]+temp_atas



                temp_bawah=self.hasil_update[data][kluster-1]**self.pangkat
                bawah=bawah+temp_bawah

            for i in range (len(a)):
                a[i]=a[i]/bawah

            self.cluster[kluster]=a


        print(self.cluster)

        for kluster in self.cluster:
            print("kluster ke",kluster,"titik >>>>",self.cluster[kluster])
            for j in range(1,self.data.ncols):
                value = self.cluster[kluster][j-1]

                self.sheetcenteroid.row(kluster).write(j, value)


        self.excel_baru.save("tribunnews_cmean.xlsx")
        self.update_objek()


    def update_objek(self):
        self.hasil_update={}

        for baris in range(1,self.data.nrows):
            temp=0
            up=[]
            for kluster in range(1,self.total_cluster+1):
                hasil_i=0
                print("_________________")
                print("kluster",kluster)

                for i in range(1,self.total_cluster+1):

                    temp_i=((self.ED(baris,kluster))/(self.ED(baris,i)))**self.pangkat
                    hasil_i=hasil_i+temp_i
                    print(i,">>hsl i",hasil_i)


                hasil=1/hasil_i
                print("hsl",hasil)
                up.append(hasil)
                print("<<>>baris ke", baris, "kluster", kluster,"=", hasil)

                #cetak ke excel
                self.sheetdatatesting_C.row(baris).write(kluster,hasil)


            self.hasil_update[baris] = up

        for i in self.hasil_update:
            print("objek >> ",i,":",self.hasil_update[i])

        self.excel_baru.save("tribunnews_cmean.xlsx")
        self.cek_hasil()

    def ED(self,baris,kluster):
        self.buka_excel_baru = xlrd.open_workbook("tribunnews_cmean.xlsx")
        self.buka_sheet_centeroid = self.buka_excel_baru.sheet_by_index(0)
        self.buka_sheet_datatesting = self.buka_excel_baru.sheet_by_index(1)
        self.buka_sheet_datatesting_C = self.buka_excel_baru.sheet_by_index(2)


        tem=0
        for j in range (1,self.data.ncols):
            a=self.data.cell_value(rowx=baris, colx=j)
            print("(",a,"-",self.buka_sheet_centeroid.cell_value(rowx=kluster, colx=j),")^2")
            tem=((a- self.buka_sheet_centeroid.cell_value(rowx=kluster, colx=j)) **2 ) + tem
        hasil=math.sqrt(tem)
        return hasil
        print("nilai ED dari baris ke:",baris,"ke pusat:",i,"hasil=",hasil)


    def cek_hasil(self):

        if self.total_langkah==1:
            self.hasil_sebelumnya=self.hasil_update
            self.total_langkah += 1
            print(self.buka_sheet_datatesting_C.cell_value(rowx=1, colx=1),"SSS")
            return self.cek()
            print("mm")

        elif self.hasil_sebelumnya != self.hasil_update:
            print("nn")

            for baris in range(1,self.data.nrows):
                value_temp=0
                hasil=0
                for kolom in range(self.total_cluster):
                    temp=(self.hasil_sebelumnya[baris][kolom]-self.hasil_update[baris][kolom])
                    value_temp=value_temp+(temp**2)
                hasil=hasil+value_temp
                hasil=math.sqrt(hasil)

            if hasil < self.banyak_error  or self.total_langkah >= self.banyak_iterasi:
                print("selesai, total langkah=",self.total_langkah,">=",self.banyak_iterasi,"OR error=",hasil,"<",self.banyak_error)
                self.cek_kluster()
                exit()

            else:
                self.total_langkah+=1
                self.hasil_sebelumnya = self.hasil_update
                return self.cek()




    def cek_kluster(self):
        self.cek={}
        excel_baru = xlrd.open_workbook("tribunnews_cmean.xlsx")
        sheet=excel_baru.sheet_by_index(2)
        for baris in range(1, self.buka_sheet_datatesting_C.nrows):
            temp = []
            for kolom in range(1, self.buka_sheet_datatesting_C.ncols):
                value = sheet.cell_value(rowx=baris, colx=kolom)
                temp.append(value)

            # cek besar
            besar_data_index = max(temp)
            tipe_kluster = temp.index(besar_data_index) + 1
            self.sheetdatatesting_C.row(baris).write(sheet.ncols, tipe_kluster)



        self.excel_baru.save("tribunnews_cmean.xlsx")



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
