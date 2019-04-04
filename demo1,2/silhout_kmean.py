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

        formLayout = QFormLayout(self)
        self.x1text=QLabel("")
        self.x2text = QLabel("Massukkan banyak cluster tadi ketika proses k-mean")

        self.banyakcluster = QLineEdit()


        self.okbutton=QPushButton("Calculate cooficient")

        formLayout.addRow(self.x2text,self.banyakcluster)
        formLayout.addRow(self.okbutton)
        formLayout.addRow(self.x1text)
        self.connect(self.okbutton, SIGNAL("clicked()"), self.cek)
        self.setLayout(formLayout)




    def cek(self):
        self.temp_si = {}
        excel = xlrd.open_workbook("tribunnews_kmean.xlsx")
        self.data = excel.sheet_by_index(1)


        #disesuaikan dgn data asli yabg digunakan
        excel_asli = xlrd.open_workbook("tribunnews_rabu.xlsx")
        self.data_asli = excel_asli.sheet_by_index(0)

        self.excel_baru = xlwt.Workbook()


        self.total_cluster = int(self.banyakcluster.text())
        self.sheet_ai_bi_si = self.excel_baru.add_sheet("ai_bi_si")

        self.sheet_ai_bi_si.row(0).write(0, "objek")
        self.sheet_ai_bi_si.row(0).write(1, "ai")
        self.sheet_ai_bi_si.row(0).write(2, "bi")
        self.sheet_ai_bi_si.row(0).write(3, "si")

        for i in range(self.data.nrows-1):
            self.sheet_ai_bi_si.row(i+1).write(0,str(i+1))


        self.excel_baru.save("tribunnews_silhout_kmean.xlsx")

        self.baca_data(self.total_cluster)
        self.kesimpulan()

    def kesimpulan(self):
        temp=0
        for objek in self.temp_si:
            temp=temp+math.fabs(self.temp_si[objek]) #pakefabs / tdk

        hasil=(temp/(self.data.nrows-1))
        print(temp,"temp_si / ","banyak",self.data.nrows-1)
        self.x1text.setText("Tingkat Rata-Rata Koofisien hasil clustering menggunakan ECLUDIAN DISTANCE adalah: "+str(hasil))



    def baca_data(self,total_kluster):
        excel = xlrd.open_workbook("tribunnews_rabu.xlsx")

        self.tampung_data={}

        for cluster in range(1,total_kluster+1):
            tem=[]
            for objek in range(1,self.data.nrows):
                data=self.data.cell_value(rowx=objek,colx=self.data.ncols-1)
                if cluster == data:
                    tem.append(objek)
            self.tampung_data[cluster]=tem

        print(self.tampung_data)
        self.calc_data()

    def calc_data(self):
        self.temp_ai={}
        self.temp_bi={}

        for baris in range(1, self.data.nrows):
            klusterlain_sebelumnya=0
            for kluster in range(1, self.total_cluster + 1):
                if baris in self.tampung_data[kluster]:
                    self.temp_ai[baris]=self.hitung_ai(baris,kluster)
                    print("ai pada objek ke", baris, "cluster ke", kluster, "adalah",
                          self.hitung_ai(baris, kluster))



                else:
                    if klusterlain_sebelumnya <= self.hitung_bi(baris,kluster):
                        self.temp_bi[baris]=klusterlain_sebelumnya
                        klusterlain_sebelumnya=self.hitung_bi(baris,kluster)
                        print("bi pada objek ke", baris, "cluster ke", kluster, "adalah",
                              self.hitung_bi(baris, kluster))

                    else:
                        self.temp_bi[baris]=self.hitung_bi(baris,kluster)
                        print("bi pada objek ke", baris, "cluster ke", kluster, "adalah",
                              self.hitung_bi(baris, kluster))

            print("baris ke", baris, "nilai ai=", self.temp_ai[baris], "nilai bi=", self.temp_bi[baris])


            self.sheet_ai_bi_si.row(baris).write(1, str(self.temp_ai[baris]))
            self.sheet_ai_bi_si.row(baris).write(2, str(self.temp_bi[baris]))
            self.excel_baru.save("tribunnews_silhout_kmean.xlsx")
            self.hitung_si(baris,self.temp_ai[baris],self.temp_bi[baris])

    def hitung_si(self,baris,ai,bi):

        if ai<bi:
            hasil_si=1-ai/bi

        elif ai==bi:
            hasil_si=0

        elif ai> bi:
            hasil_si=bi/ai -1

        else:
            hasil_si="error"

        self.temp_si[baris]=hasil_si
        self.sheet_ai_bi_si.row(baris).write(3,str(hasil_si))


        self.excel_baru.save("tribunnews_silhout_kmean.xlsx")

    def hitung_ai(self,baris,kluster):


        temp_hasil_ai = 0
        for baris_pembanding in self.tampung_data[kluster]:
            if baris == baris_pembanding:
                continue
            else:
                temp_hasil_ai=temp_hasil_ai+ self.hitung_jarak(baris,baris_pembanding,self.data_asli)

        if len(self.tampung_data[kluster])==1:
            hasil=0
        else:
            hasil= temp_hasil_ai / (len(self.tampung_data[kluster])-1)
 #       print("hasil ai antara objek ke", baris, "dengan cluster ke", kluster, "=", temp_hasil_ai,"/",len(self.tampung_data[kluster])-1,">>", hasil)
        return hasil

    def hitung_bi(self,baris,kluster):
        temp_hasil_bi = 0
        for baris_pembanding in self.tampung_data[kluster]:
            temp_hasil_bi = temp_hasil_bi + self.hitung_jarak(baris, baris_pembanding, self.data_asli)

        hasil = temp_hasil_bi / (len(self.tampung_data[kluster]))
#        print("hasil bi antara objek ke",baris,"dengan cluster ke",kluster,"=",temp_hasil_bi,"/",len(self.tampung_data[kluster])-1,">>",hasil)

        return hasil





    def hitung_jarak(self,baris,baris_pembanding,data):
        tem=0
        for j in range (1,data.ncols):
            a=data.cell_value(rowx=baris, colx=j)
            print(a,"-",data.cell_value(rowx=baris_pembanding, colx=j))
            #tem=math.fabs((a- data.cell_value(rowx=baris_pembanding, colx=j)) ) + tem #pake fabs / tidak

            tem = ((a - data.cell_value(rowx=baris_pembanding, colx=j)) ** 2) + tem #pake ED
        hasil = math.sqrt(tem)

        print("jarak antara objek", baris, "dengan", baris_pembanding,"=",tem)
        #return tem
        return hasil

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
