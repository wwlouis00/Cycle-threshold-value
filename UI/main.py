import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem,QFileDialog, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtGui import QImage, QPixmap
from CT_dynamic import Ui_MainWindow
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
import datetime
from datetime import datetime, timedelta
import cv2 as cv
import pandas as pd
import numpy as np
import matplotlib as plt
now_output_time = str(datetime.now().strftime('%Y-%m-%d %H-%M-%S'))
colorTab_More4 = ['#e8a5eb', '#facc9e', '#e8e948', '#1bb763',
                       '#25f2f3', '#1db3ea', '#d1aef8', '#c8c92c',
                       '#f32020', '#fd9b09', '#406386', '#24a1a1',
                       '#1515f8', '#959697', '#744a20', '#7b45a5']
class MatplotlibWidget(QMainWindow,Ui_MainWindow):
    def __init__(self,app):
        super(QMainWindow,self).__init__()
        self.app = app
        self.setup_ui()
        self.setWindowTitle("Dashboard Covid 19 QT Designer ") 
        self.connect_signals()
        self.plotPaisMuertes()

    def setup_ui(self):
        self.setupUi(self)
    
    def connect_signals(self):
        self.setupUi(self)
        self.btn_open.clicked.connect(self.browsefile)
        self.slider_threshold.valueChanged.connect(self.sl_threshold)
        self.slider_begin.valueChanged.connect(self.sl_begin)
        self.slider_end.valueChanged.connect(self.sl_end)
        self.A1_radio.clicked.connect(self.plotPaisMuertes)
        self.A2_radio.clicked.connect(self.plotPaisMuertes)
        self.A3_radio.clicked.connect(self.plotPaisMuertes)
        self.A4_radio.clicked.connect(self.plotPaisMuertes)
        self.A5_radio.clicked.connect(self.plotPaisMuertes)
        self.A6_radio.clicked.connect(self.plotPaisMuertes)
        self.A7_radio.clicked.connect(self.plotPaisMuertes)
        self.A8_radio.clicked.connect(self.plotPaisMuertes)
        self.B1_radio.clicked.connect(self.plotPaisMuertes)
        self.B2_radio.clicked.connect(self.plotPaisMuertes)
        self.B3_radio.clicked.connect(self.plotPaisMuertes)
        self.B4_radio.clicked.connect(self.plotPaisMuertes)
        self.B5_radio.clicked.connect(self.plotPaisMuertes)
        self.B6_radio.clicked.connect(self.plotPaisMuertes)
        self.B7_radio.clicked.connect(self.plotPaisMuertes)
        self.B8_radio.clicked.connect(self.plotPaisMuertes)
        

    def browsefile(self):
        if not os.path.isdir('./result'):
            os.mkdir('./result')
            os.mkdir('./result/Cali_result/')
            os.mkdir('./result/Display_result/')
        self.fname = QFileDialog.getOpenFileName(self, '開啟csv檔案', 'C:\Program Files (x86)', 'csv files (*.csv)')
        if(self.fname[0]==""):
            print("no file")
        else:
            self.calculate()
    
    def plotPaisMuertes(self):
        if self.A1_radio.isChecked():
            print("yes")

    def calculate(self):
        self.big_well = []
        self.big_data = []
        self.Input_file.setText(self.fname[0])
        self.df_raw = pd.read_csv(self.fname[0])
        # print(self.coco)
        self.df_raw.reset_index(inplace=True)
        
        self.df_raw.rename(columns={'time':'well_1', 'A1':'well_2', 'A2':'well_3', 'A3':'well_4',
                            'A4':'well_5', 'A5':'well_6', 'A6':'well_7', 'A7':'well_8',
                            'A8':'well_9', 'B1':'well_10', 'B2':'well_11', 'B3':'well_12',
                            'B4':'well_13', 'B5':'well_14', 'B6':'well_15', 'B7':'well_16'},inplace = True)
        self.df_raw.drop(labels=["B8"], axis="columns")
        self.df_raw.rename(columns={"index": "time", "B": "c"},inplace=True)
        print("-"*150)
        print(self.df_raw)
        print("-"*150)
        self.df_normalization = self.df_raw.copy()
        self.get_accumulation_time()
        self.normalize()
        threshold_value = self.get_ct_threshold()
        # UI顯示 16個CT值
        self.Ct_value = self.get_ct_value(threshold_value)
        # self.lineEdit_well_1.setText(str(self.Ct_value[0]))
        # self.lineEdit_well_2.setText(str(self.Ct_value[1]))
        # self.lineEdit_well_3.setText(str(self.Ct_value[2]))
        # self.lineEdit_well_4.setText(str(self.Ct_value[3]))
        # self.lineEdit_well_5.setText(str(self.Ct_value[4]))
        # self.lineEdit_well_6.setText(str(self.Ct_value[5]))
        # self.lineEdit_well_7.setText(str(self.Ct_value[6]))
        # self.lineEdit_well_8.setText(str(self.Ct_value[7]))
        # self.lineEdit_well_9.setText(str(self.Ct_value[8]))
        # self.lineEdit_well_10.setText(str(self.Ct_value[9]))
        # self.lineEdit_well_11.setText(str(self.Ct_value[10]))
        # self.lineEdit_well_12.setText(str(self.Ct_value[11]))
        # self.lineEdit_well_13.setText(str(self.Ct_value[12]))
        # self.lineEdit_well_14.setText(str(self.Ct_value[13]))
        # self.lineEdit_well_15.setText(str(self.Ct_value[14]))
        # self.lineEdit_well_16.setText(str(self.Ct_value[15]))

        self.A1_data = []
        self.A2_data = []
        self.A3_data = []
        self.A4_data = []
        self.A5_data = []
        self.A6_data = []
        self.A7_data = []
        self.A8_data = []
        self.B1_data = []
        self.B2_data = []
        self.B3_data = []
        self.B4_data = []
        self.B5_data = []
        self.B6_data = []
        self.B7_data = []
        self.B8_data = []
        self.time_array = []

        for i in range(1, 17, 1):
            self.big_data.append(self.df_normalization["well"+str(i)].rolling(window=5).mean())
        self.all_well = pd.DataFrame(self.big_data)
        self.move_finish = self.all_well.T
        for i in range(0, len(self.move_finish.index), 1):
            self.A1_data.append(self.move_finish.loc[i,'well1'])
            self.A2_data.append(self.move_finish.loc[i,'well2'])
            self.A3_data.append(self.move_finish.loc[i,'well3'])
            self.A4_data.append(self.move_finish.loc[i,'well4'])
            self.A5_data.append(self.move_finish.loc[i,'well5'])
            self.A6_data.append(self.move_finish.loc[i,'well6'])
            self.A7_data.append(self.move_finish.loc[i,'well7'])
            self.A8_data.append(self.move_finish.loc[i,'well8'])
            self.B1_data.append(self.move_finish.loc[i,'well9'])
            self.B2_data.append(self.move_finish.loc[i,'well10'])
            self.B3_data.append(self.move_finish.loc[i,'well11'])
            self.B4_data.append(self.move_finish.loc[i,'well12'])
            self.B5_data.append(self.move_finish.loc[i,'well13'])
            self.B6_data.append(self.move_finish.loc[i,'well14'])
            self.B7_data.append(self.move_finish.loc[i,'well15'])
            self.B8_data.append(self.move_finish.loc[i,'well16'])

        for j in range(0, len(self.move_finish.index), 1):
            self.time_array.append(j / 2)
        
        print(self.move_finish)
        self.loadEstados()
        # plt.figure(figsize=(10, 2.5), dpi=100, linewidth=3)
        # plt.plot(self.time_array, self.A1_data, '-', color=colorTab_More4[0], label="A1")  # 紅
        # plt.plot(self.time_array, self.A2_data, '-', color=colorTab_More4[1], label="A2")  # 澄
        # plt.plot(self.time_array, self.A3_data, '-', color=colorTab_More4[2], label="A3")  # 黃
        # plt.plot(self.time_array, self.A4_data, '-', color=colorTab_More4[3], label="A4")  # 綠
        # plt.plot(self.time_array, self.A5_data, '-', color=colorTab_More4[4], label="A5")  # 藍
        # plt.plot(self.time_array, self.A6_data, '-', color=colorTab_More4[5], label="A6")  # 靛
        # plt.plot(self.time_array, self.A7_data, '-', color=colorTab_More4[6], label="A7")  # 紫
        # plt.plot(self.time_array, self.A8_data, '-', color=colorTab_More4[7], label="A8")  # 黑
        # plt.plot(self.time_array, self.B1_data, '-', color=colorTab_More4[8], label="B1")  # 紅
        # plt.plot(self.time_array, self.B2_data, '-', color=colorTab_More4[9], label="B2")  # 澄
        # plt.plot(self.time_array, self.B3_data, '-', color=colorTab_More4[10], label="B3")  # 黃
        # plt.plot(self.time_array, self.B4_data, '-', color=colorTab_More4[11], label="B4")  # 綠
        # plt.plot(self.time_array, self.B5_data, '-', color=colorTab_More4[12], label="B5")  # 藍
        # plt.plot(self.time_array, self.B6_data, '-', color=colorTab_More4[13], label="B6")  # 靛
        # plt.plot(self.time_array, self.B7_data, '-', color=colorTab_More4[14], label="B7")  # 紫
        # plt.plot(self.time_array, self.B8_data, '-', color=colorTab_More4[15], label="B8")  # 黑
        # plt.ylim(-1, 3)
        # plt.title("Amplification curve")
        # plt.xlabel('Time (min)')  # x軸說明文字
        # plt.ylabel('Normalized fluorescent intensity')  # y軸說明文字
        # plt.legend(loc="upper center", bbox_to_anchor=(0.5, 1.05),
        #     fancybox=True, shadow=True, ncol=8, fontsize=7.5)
        # plt.savefig('./result/Display_result/CT.jpg')
        # self.displayphoto()
    def loadEstados(self):
            # Borrar Axes
        self.MplWidget.canvas.axes.cla()
        self.MplWidget.canvas.axes1.cla()

    def displayphoto(self):
        self.img = cv.imread('./result/Display_result/CT.jpg')
        self.img = cv.cvtColor(self.img, cv.COLOR_BGR2RGB)
        x = self.img.shape[1]
        y = self.img.shape[0]
        frame = QImage(self.img, x, y, x * 3, QImage.Format_RGB888)
        self.pix = QPixmap.fromImage(frame)
        self.item = QGraphicsPixmapItem(self.pix)
        self.scene = QGraphicsScene()
        self.scene.addItem(self.item)
        self.CT_chart.setScene(self.scene)

    def get_accumulation_time(self):
        df_time = self.df_normalization['time']
        time_ori = datetime.strptime(df_time[0], "%H:%M:%S")
        time_delta = []
        for time in df_time:
            time_now = datetime.strptime(time, "%H:%M:%S")
            time_delta.append((time_now - time_ori).seconds / 60)
        self.df_normalization.insert(1, column="accumulation", value=time_delta)

    def get_StdDev_and_Avg(self):
        StdDev = []
        Avg = []
        for i in range(0, 16):
            df_current_well = self.df_normalization[f'well_{i + 1}']
            # StdDev.append(df_current_well[int(self.Start_time.text()) * 2:int(self.End_time.text()) * 2].std())
            # Avg.append(df_current_well[int(self.Start_time.text()) * 2:int(self.End_time.text()) * 2].mean())
            StdDev.append(df_current_well[2 * 2:7 * 2].std())
            Avg.append(df_current_well[2 * 2:7 * 2].mean())
        return StdDev, Avg

    def normalize(self):
        for i in range(0, 16):
            df_current_well = self.df_raw[f'well_{i + 1}']
            # self.baseline = df_current_well[int(self.Start_time.text()) * 2:int(self.End_time.text()) * 2].mean()
            self.baseline = df_current_well[2* 2:7 * 2].mean()
            self.df_normalization[f'well{i + 1}'] = (self.df_raw[f'well_{i + 1}'] - self.baseline) / self.baseline
            if(i<8):
                print(f'A{i+1}'+" baseline value: " + str(self.baseline))
            else:
                print(f'B{i-7}'+" baseline value: " + str(self.baseline))
        print("-"*150)

    def get_ct_threshold(self):
        threshold_value = []
        StdDev, Avg = self.get_StdDev_and_Avg()
        for i in range(0, 16):
            # threshold_value.append(int(self.Input_N.text()) * StdDev[i] + Avg[i])
            threshold_value.append(10 * StdDev[i] + Avg[i])
        return threshold_value

    def get_ct_value(self, threshold_value):
        Ct_value = []
        for i in range(0, 16):
            df_current_well = self.df_normalization[f'well_{i + 1}']
            df_accumulation = self.df_normalization['accumulation']
            try:
                for j, row in enumerate(df_current_well):
                    if row >= threshold_value[i]:
                        thres_lower = df_current_well[j - 1]
                        thres_upper = df_current_well[j]
                        acc_time_lower = df_accumulation[j - 1]
                        acc_time_upper = df_accumulation[j + 1]
                        # linear regression
                        x2 = acc_time_upper
                        y2 = thres_upper
                        x1 = acc_time_lower
                        y1 = thres_lower
                        y = threshold_value[i]
                        x = (x2 - x1) * (y - y1) / (y2 - y1) + x1
                        Ct_value.append(round(x, 2))
                        # print(f"Ct of well_{i + 1} is {round(x, 2)}")
                        break
                    # if there is no Ct_value availible
                    elif j == len(df_current_well) - 1:
                        Ct_value.append("N/A")
                        # print("Ct value is not available")
            except Exception as e:
                Ct_value.append("N/A")
        return Ct_value
    
    def sl_threshold(self):
        print("test")
    def sl_begin(self):
        print("test")
    def sl_end(self):
        print("test")
        # if self.ui.radioButtonCasos.isChecked():
        #     self.selectPlotCasos()
        # elif self.ui.radioButtonMuertes.isChecked():
        #     self.selectPlotMuertes()
        # elif self.ui.radioButtonAmbos.isChecked():
        #     self.selectPlotAmbos()
        # self.calculate()
        # if self.Start_time.text() == "" or self.End_time.text() == "" or self.Input_N.text() == "":
        #     QtWidgets.QMessageBox.critical(self, u"警告", u"請輸入Time of background", buttons=QtWidgets.QMessageBox.Ok, defaultButton=QtWidgets.QMessageBox.Ok)
        # elif (int(self.Start_time.text()) > int(self.End_time.text())):
        #     QtWidgets.QMessageBox.critical(self, u"警告", u"開始時間跟結束時間錯誤", buttons=QtWidgets.QMessageBox.Ok, defaultButton=QtWidgets.QMessageBox.Ok)
        # else:
        #     self.fname = QFileDialog.getOpenFileName(self, '開啟csv檔案', 'C:\Program Files (x86)', 'csv files (*.csv)')
        #     self.calculate()
    # def setup
        # self.getCSV()  # Cargar datos CSV
        # self.indexState()  # Indice para estados
        # self.indexDate()  # Indice de fechas
        # self.setWindowTitle("Dashboard Covid 19 QT Designer ")  # Título de MainWindows
        # self.addToolBar(NavigationToolbar(self.ui.MplWidget.canvas, self))  # Agregar Axes
        # self.ui.comboBoxCountry.activated.connect(self.clearStates)  # Limpiar listBox de estados, para una carga nueva
        # self.ui.comboBoxCountry.activated.connect(self.loadEstados)  # Cargar estados al listBox
        # self.plotAmbosPaises()  # Graficar de inicio Muertes y casos acumulativos

        # # llamar métodos según el radio Button seleccionado para graficar
        # self.ui.radioButtonCasos.clicked.connect(self.selectPlotCasos)
        # self.ui.radioButtonMuertes.clicked.connect(self.selectPlotMuertes)
        # self.ui.radioButtonAmbos.clicked.connect(self.selectPlotAmbos)

        # # llamar métodos según el radio Button seleccionado para graficar datos diarios y acumulados
        # self.ui.radioButtonDiarios.clicked.connect(self.DatosDiarios)
        # self.ui.radioButton_2.clicked.connect(self.DatosAcumulativos)

        # # Al hacer clic en un pais se grafica de forma automática segun los radio Buttos y listBox activados
        # self.ui.comboBoxCountry.activated.connect(self.btnstate)

        # # Al hacer clic en un estado se grafica de forma automática segun los radio Buttos y listBox activados
        # self.ui.comboBoxEstado.activated.connect(self.btnstate2)

        # # Según se mueva el slider y de acurdo a los radio buttons selccionados se presentará la media móvil
        # self.ui.sliderPromedio.valueChanged.connect(self.sliderSelect)

    # =============== Funciones ======================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MatplotlibWidget(app)
    window.show()
    sys.exit(app.exec_())

    