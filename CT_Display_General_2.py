from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets
import pandas as pd
import matplotlib.pyplot as plt
import cv2 as cv
from PyQt5.QtGui import QIntValidator
import datetime
from datetime import datetime, timedelta
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QGraphicsScene, QGraphicsPixmapItem,QFileDialog,QDialog,QApplication
from PyQt5 import QtCore, QtGui, QtWidgets
now_output_time = str(datetime.now().strftime('%Y-%m-%d %H-%M-%S'))
import os
from PyQt5 import QtCore, QtGui, QtWidgets

colorTab_More4 = ['#e8a5eb', '#facc9e', '#e8e948', '#1bb763',
                       '#25f2f3', '#1db3ea', '#d1aef8', '#c8c92c',
                       '#f32020', '#fd9b09', '#406386', '#24a1a1',
                       '#1515f8', '#959697', '#744a20', '#7b45a5']
class Ui_MainWindow(QtWidgets.QWidget):
    def browsefile(self):
        if self.Start_time.text() == "" or self.End_time.text() == "" or self.Input_N.text() == "":
            QtWidgets.QMessageBox.critical(self, u"警告", u"請輸入Time of background", buttons=QtWidgets.QMessageBox.Ok, defaultButton=QtWidgets.QMessageBox.Ok)
        elif (int(self.Start_time.text()) > int(self.End_time.text())):
            QtWidgets.QMessageBox.critical(self, u"警告", u"開始時間跟結束時間錯誤", buttons=QtWidgets.QMessageBox.Ok, defaultButton=QtWidgets.QMessageBox.Ok)
        else:
            self.fname = QFileDialog.getOpenFileName(self, '開啟csv檔案', 'C:\Program Files (x86)', 'csv files (*.csv)')
            self.calculate()
            # if os.path.isdir("CT_image"):
            #     print("")
            # else:
            #     os.mkdir("CT_image")
    def calculate(self):
        self.big_well = []
        self.big_data = []
        self.Input_file.setText(self.fname[0])
        self.df_raw = pd.read_csv(self.fname[0])
        self.df_normalization = self.df_raw.copy()
        self.get_accumulation_time()
        self.normalize()
        print("-"*50)
        threshold_value = self.get_ct_threshold()
        # UI顯示 16個CT值
        self.Ct_value = self.get_ct_value(threshold_value)
        self.lineEdit_well_1.setText(str(self.Ct_value[0]))
        self.lineEdit_well_2.setText(str(self.Ct_value[1]))
        self.lineEdit_well_3.setText(str(self.Ct_value[2]))
        self.lineEdit_well_4.setText(str(self.Ct_value[3]))
        self.lineEdit_well_5.setText(str(self.Ct_value[4]))
        self.lineEdit_well_6.setText(str(self.Ct_value[5]))
        self.lineEdit_well_7.setText(str(self.Ct_value[6]))
        self.lineEdit_well_8.setText(str(self.Ct_value[7]))
        self.lineEdit_well_9.setText(str(self.Ct_value[8]))
        self.lineEdit_well_10.setText(str(self.Ct_value[9]))
        self.lineEdit_well_11.setText(str(self.Ct_value[10]))
        self.lineEdit_well_12.setText(str(self.Ct_value[11]))
        self.lineEdit_well_13.setText(str(self.Ct_value[12]))
        self.lineEdit_well_14.setText(str(self.Ct_value[13]))
        self.lineEdit_well_15.setText(str(self.Ct_value[14]))
        self.lineEdit_well_16.setText(str(self.Ct_value[15]))

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

        plt.figure(figsize=(10, 2.5), dpi=100, linewidth=3)
        plt.plot(self.time_array, self.A1_data, '-', color=colorTab_More4[0], label="A1")  # 紅
        plt.plot(self.time_array, self.A2_data, '-', color=colorTab_More4[1], label="A2")  # 澄
        plt.plot(self.time_array, self.A3_data, '-', color=colorTab_More4[2], label="A3")  # 黃
        plt.plot(self.time_array, self.A4_data, '-', color=colorTab_More4[3], label="A4")  # 綠
        plt.plot(self.time_array, self.A5_data, '-', color=colorTab_More4[4], label="A5")  # 藍
        plt.plot(self.time_array, self.A6_data, '-', color=colorTab_More4[5], label="A6")  # 靛
        plt.plot(self.time_array, self.A7_data, '-', color=colorTab_More4[6], label="A7")  # 紫
        plt.plot(self.time_array, self.A8_data, '-', color=colorTab_More4[7], label="A8")  # 黑
        plt.plot(self.time_array, self.B1_data, '-', color=colorTab_More4[8], label="B1")  # 紅
        plt.plot(self.time_array, self.B2_data, '-', color=colorTab_More4[9], label="B2")  # 澄
        plt.plot(self.time_array, self.B3_data, '-', color=colorTab_More4[10], label="B3")  # 黃
        plt.plot(self.time_array, self.B4_data, '-', color=colorTab_More4[11], label="B4")  # 綠
        plt.plot(self.time_array, self.B5_data, '-', color=colorTab_More4[12], label="B5")  # 藍
        plt.plot(self.time_array, self.B6_data, '-', color=colorTab_More4[13], label="B6")  # 靛
        plt.plot(self.time_array, self.B7_data, '-', color=colorTab_More4[14], label="B7")  # 紫
        plt.plot(self.time_array, self.B8_data, '-', color=colorTab_More4[15], label="B8")  # 黑
        plt.ylim(0, 3)
        plt.title("Amplification curve")
        plt.xlabel('Time (min)')  # x軸說明文字
        plt.ylabel('Fluorescence signal intensity (a.u.)')  # y軸說明文字
        plt.legend(loc="upper center", bbox_to_anchor=(0.5, 1.05),
            fancybox=True, shadow=True, ncol=8, fontsize=7.5)
        plt.savefig('./result/Display_result/CT.jpg')
        self.displayphoto()

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
            StdDev.append(df_current_well[int(self.Start_time.text()) * 2:int(self.End_time.text()) * 2].std())
            Avg.append(df_current_well[int(self.Start_time.text()) * 2:int(self.End_time.text()) * 2].mean())
        return StdDev, Avg

    def normalize(self):
        for i in range(0, 16):
            df_current_well = self.df_raw[f'well_{i + 1}']
            self.baseline = df_current_well[int(self.Start_time.text()) * 2:int(self.End_time.text()) * 2].mean()
            self.df_normalization[f'well{i + 1}'] = (self.df_raw[f'well_{i + 1}'] - self.baseline) / self.baseline #(IF(t)-IF(b))/IF(b)
            print(f'well_{i+1}'+" 的baseline值: " + str(self.baseline))
            

    def get_ct_threshold(self):
        threshold_value = []
        StdDev, Avg = self.get_StdDev_and_Avg()
        for i in range(0, 16):
            threshold_value.append(int(self.Input_N.text()) * StdDev[i] + Avg[i])
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
    #重置計算
    def reset_file(self):
        if self.Input_file.text() == "" or self.Start_time.text() == "" or self.End_time.text() == "" or self.Input_N.text() == "":
            QtWidgets.QMessageBox.critical(self, u"未輸入開始時間以及結束時間!", u"未開啟任何Csv檔案", buttons=QtWidgets.QMessageBox.Ok,defaultButton=QtWidgets.QMessageBox.Ok)
        else:
            self.calculate()
    #存檔
    def save_file(self):
        #儲存失敗
        if self.Input_file.text() == "":
            QtWidgets.QMessageBox.critical(self, u"存取失敗", u"未開啟csv檔案", buttons=QtWidgets.QMessageBox.Ok,
                defaultButton=QtWidgets.QMessageBox.Ok)
        #儲存成功
        else:
            QtWidgets.QMessageBox.information(self, u"存取成功", u"已成功另存Excel檔案", buttons=QtWidgets.QMessageBox.Ok,
                defaultButton=QtWidgets.QMessageBox.Ok)
            #設置資料欄位
            self.save_excel = pd.DataFrame({"well_1": [self.Ct_value[0]], "well_2": [self.Ct_value[1]],
                                            "well_3": [self.Ct_value[2]], "well_4": [self.Ct_value[3]],
                                            "well_5": [self.Ct_value[4]], "well_6": [self.Ct_value[5]],
                                            "well_7": [self.Ct_value[6]], "well_8": [self.Ct_value[7]],
                                            "well_9": [self.Ct_value[8]], "well_10": [self.Ct_value[9]],
                                            "well_11": [self.Ct_value[10]], "well_12": [self.Ct_value[11]],
                                            "well_13": [self.Ct_value[12]], "well_14": [self.Ct_value[13]],
                                            "well_15": [self.Ct_value[14]], "well_16": [self.Ct_value[15]]}
                , index=["CT_Value"])
            #儲存資料以及存取位置
            self.move_finish.to_csv('./result/Display_result/CT_Value_'+ now_output_time + '_MA_data.csv', encoding="utf_8_sig")
            self.save_excel.T.to_csv('./result/Display_result/CT_Value' + now_output_time + "all_well.csv", encoding="utf_8_sig")
    #清除顯示
    def clean_log(self):
        self.Input_file.setText("")
        self.lineEdit_well_1.setText("")
        self.lineEdit_well_2.setText("")
        self.lineEdit_well_3.setText("")
        self.lineEdit_well_4.setText("")
        self.lineEdit_well_5.setText("")
        self.lineEdit_well_6.setText("")
        self.lineEdit_well_7.setText("")
        self.lineEdit_well_8.setText("")
        self.lineEdit_well_9.setText("")
        self.lineEdit_well_10.setText("")
        self.lineEdit_well_11.setText("")
        self.lineEdit_well_12.setText("")
        self.lineEdit_well_13.setText("")
        self.lineEdit_well_14.setText("")
        self.lineEdit_well_15.setText("")
        self.lineEdit_well_16.setText("")
        self.Start_time.setText("")
        self.End_time.setText("")
        self.Input_N.setText("")
        self.CT_chart.setScene(None)


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(980, 610)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.CT_chart = QtWidgets.QGraphicsView(self.centralwidget)
        self.CT_chart.setGeometry(QtCore.QRect(10, 6, 961, 289))
        self.CT_chart.setObjectName("CT_chart")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 462, 111, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(510, 300, 461, 295))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_well1 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_well1.setFont(font)
        self.label_well1.setAlignment(QtCore.Qt.AlignCenter)
        self.label_well1.setObjectName("label_well1")
        self.gridLayout.addWidget(self.label_well1, 0, 0, 1, 1)
        self.lineEdit_well_1 = QtWidgets.QLineEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lineEdit_well_1.setFont(font)
        self.lineEdit_well_1.setText("")
        self.lineEdit_well_1.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_well_1.setObjectName("lineEdit_well_1")
        self.gridLayout.addWidget(self.lineEdit_well_1, 0, 1, 1, 1)
        self.label_well9 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_well9.setFont(font)
        self.label_well9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_well9.setObjectName("label_well9")
        self.gridLayout.addWidget(self.label_well9, 0, 2, 1, 1)
        self.lineEdit_well_9 = QtWidgets.QLineEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lineEdit_well_9.setFont(font)
        self.lineEdit_well_9.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_well_9.setObjectName("lineEdit_well_9")
        self.gridLayout.addWidget(self.lineEdit_well_9, 0, 3, 1, 1)
        self.label_well2 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_well2.setFont(font)
        self.label_well2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_well2.setObjectName("label_well2")
        self.gridLayout.addWidget(self.label_well2, 1, 0, 1, 1)
        self.lineEdit_well_2 = QtWidgets.QLineEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lineEdit_well_2.setFont(font)
        self.lineEdit_well_2.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_well_2.setObjectName("lineEdit_well_2")
        self.gridLayout.addWidget(self.lineEdit_well_2, 1, 1, 1, 1)
        self.label_well10 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_well10.setFont(font)
        self.label_well10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_well10.setObjectName("label_well10")
        self.gridLayout.addWidget(self.label_well10, 1, 2, 1, 1)
        self.lineEdit_well_10 = QtWidgets.QLineEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lineEdit_well_10.setFont(font)
        self.lineEdit_well_10.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_well_10.setObjectName("lineEdit_well_10")
        self.gridLayout.addWidget(self.lineEdit_well_10, 1, 3, 1, 1)
        self.label_well3 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_well3.setFont(font)
        self.label_well3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_well3.setObjectName("label_well3")
        self.gridLayout.addWidget(self.label_well3, 2, 0, 1, 1)
        self.lineEdit_well_3 = QtWidgets.QLineEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lineEdit_well_3.setFont(font)
        self.lineEdit_well_3.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_well_3.setObjectName("lineEdit_well_3")
        self.gridLayout.addWidget(self.lineEdit_well_3, 2, 1, 1, 1)
        self.label_well11 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_well11.setFont(font)
        self.label_well11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_well11.setObjectName("label_well11")
        self.gridLayout.addWidget(self.label_well11, 2, 2, 1, 1)
        self.lineEdit_well_11 = QtWidgets.QLineEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lineEdit_well_11.setFont(font)
        self.lineEdit_well_11.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_well_11.setObjectName("lineEdit_well_11")
        self.gridLayout.addWidget(self.lineEdit_well_11, 2, 3, 1, 1)
        self.label_well4 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_well4.setFont(font)
        self.label_well4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_well4.setObjectName("label_well4")
        self.gridLayout.addWidget(self.label_well4, 3, 0, 1, 1)
        self.lineEdit_well_4 = QtWidgets.QLineEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lineEdit_well_4.setFont(font)
        self.lineEdit_well_4.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_well_4.setObjectName("lineEdit_well_4")
        self.gridLayout.addWidget(self.lineEdit_well_4, 3, 1, 1, 1)
        self.label_well12 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_well12.setFont(font)
        self.label_well12.setAlignment(QtCore.Qt.AlignCenter)
        self.label_well12.setObjectName("label_well12")
        self.gridLayout.addWidget(self.label_well12, 3, 2, 1, 1)
        self.lineEdit_well_12 = QtWidgets.QLineEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lineEdit_well_12.setFont(font)
        self.lineEdit_well_12.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_well_12.setObjectName("lineEdit_well_12")
        self.gridLayout.addWidget(self.lineEdit_well_12, 3, 3, 1, 1)
        self.label_well5 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_well5.setFont(font)
        self.label_well5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_well5.setObjectName("label_well5")
        self.gridLayout.addWidget(self.label_well5, 4, 0, 1, 1)
        self.lineEdit_well_5 = QtWidgets.QLineEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lineEdit_well_5.setFont(font)
        self.lineEdit_well_5.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_well_5.setObjectName("lineEdit_well_5")
        self.gridLayout.addWidget(self.lineEdit_well_5, 4, 1, 1, 1)
        self.label_well13 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_well13.setFont(font)
        self.label_well13.setAlignment(QtCore.Qt.AlignCenter)
        self.label_well13.setObjectName("label_well13")
        self.gridLayout.addWidget(self.label_well13, 4, 2, 1, 1)
        self.lineEdit_well_13 = QtWidgets.QLineEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lineEdit_well_13.setFont(font)
        self.lineEdit_well_13.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_well_13.setObjectName("lineEdit_well_13")
        self.gridLayout.addWidget(self.lineEdit_well_13, 4, 3, 1, 1)
        self.label_well6 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_well6.setFont(font)
        self.label_well6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_well6.setObjectName("label_well6")
        self.gridLayout.addWidget(self.label_well6, 5, 0, 1, 1)
        self.lineEdit_well_6 = QtWidgets.QLineEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lineEdit_well_6.setFont(font)
        self.lineEdit_well_6.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_well_6.setObjectName("lineEdit_well_6")
        self.gridLayout.addWidget(self.lineEdit_well_6, 5, 1, 1, 1)
        self.label_well14 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_well14.setFont(font)
        self.label_well14.setAlignment(QtCore.Qt.AlignCenter)
        self.label_well14.setObjectName("label_well14")
        self.gridLayout.addWidget(self.label_well14, 5, 2, 1, 1)
        self.lineEdit_well_14 = QtWidgets.QLineEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lineEdit_well_14.setFont(font)
        self.lineEdit_well_14.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_well_14.setObjectName("lineEdit_well_14")
        self.gridLayout.addWidget(self.lineEdit_well_14, 5, 3, 1, 1)
        self.label_well7 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_well7.setFont(font)
        self.label_well7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_well7.setObjectName("label_well7")
        self.gridLayout.addWidget(self.label_well7, 6, 0, 1, 1)
        self.lineEdit_well_7 = QtWidgets.QLineEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lineEdit_well_7.setFont(font)
        self.lineEdit_well_7.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_well_7.setObjectName("lineEdit_well_7")
        self.gridLayout.addWidget(self.lineEdit_well_7, 6, 1, 1, 1)
        self.label_well15 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_well15.setFont(font)
        self.label_well15.setAlignment(QtCore.Qt.AlignCenter)
        self.label_well15.setObjectName("label_well15")
        self.gridLayout.addWidget(self.label_well15, 6, 2, 1, 1)
        self.lineEdit_well_15 = QtWidgets.QLineEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lineEdit_well_15.setFont(font)
        self.lineEdit_well_15.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_well_15.setObjectName("lineEdit_well_15")
        self.gridLayout.addWidget(self.lineEdit_well_15, 6, 3, 1, 1)
        self.label_well8 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_well8.setFont(font)
        self.label_well8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_well8.setObjectName("label_well8")
        self.gridLayout.addWidget(self.label_well8, 7, 0, 1, 1)
        self.lineEdit_well_8 = QtWidgets.QLineEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lineEdit_well_8.setFont(font)
        self.lineEdit_well_8.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_well_8.setObjectName("lineEdit_well_8")
        self.gridLayout.addWidget(self.lineEdit_well_8, 7, 1, 1, 1)
        self.label_well16 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_well16.setFont(font)
        self.label_well16.setAlignment(QtCore.Qt.AlignCenter)
        self.label_well16.setObjectName("label_well16")
        self.gridLayout.addWidget(self.label_well16, 7, 2, 1, 1)
        self.lineEdit_well_16 = QtWidgets.QLineEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lineEdit_well_16.setFont(font)
        self.lineEdit_well_16.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_well_16.setObjectName("lineEdit_well_16")
        self.gridLayout.addWidget(self.lineEdit_well_16, 7, 3, 1, 1)
        self.layoutWidget1 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget1.setGeometry(QtCore.QRect(10, 378, 491, 61))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.layoutWidget1)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.Start_time = QtWidgets.QLineEdit(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.Start_time.setFont(font)
        self.Start_time.setAlignment(QtCore.Qt.AlignCenter)
        self.Start_time.setObjectName("Start_time")
        self.gridLayout_3.addWidget(self.Start_time, 0, 2, 1, 1)
        self.End_time = QtWidgets.QLineEdit(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.End_time.setFont(font)
        self.End_time.setAlignment(QtCore.Qt.AlignCenter)
        self.End_time.setObjectName("End_time")
        self.gridLayout_3.addWidget(self.End_time, 0, 4, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.gridLayout_3.addWidget(self.label_7, 0, 3, 1, 1)
        self.label_Timeofbackground = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_Timeofbackground.setFont(font)
        self.label_Timeofbackground.setAlignment(QtCore.Qt.AlignCenter)
        self.label_Timeofbackground.setObjectName("label_Timeofbackground")
        self.gridLayout_3.addWidget(self.label_Timeofbackground, 0, 1, 1, 1)
        self.layoutWidget2 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget2.setGeometry(QtCore.QRect(10, 444, 491, 70))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.layoutWidget2)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_Threshold = QtWidgets.QLabel(self.layoutWidget2)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_Threshold.setFont(font)
        self.label_Threshold.setAlignment(QtCore.Qt.AlignCenter)
        self.label_Threshold.setObjectName("label_Threshold")
        self.gridLayout_4.addWidget(self.label_Threshold, 0, 1, 1, 1)
        self.label_N = QtWidgets.QLabel(self.layoutWidget2)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_N.setFont(font)
        self.label_N.setAlignment(QtCore.Qt.AlignCenter)
        self.label_N.setObjectName("label_N")
        self.gridLayout_4.addWidget(self.label_N, 1, 0, 1, 1)
        self.Input_N = QtWidgets.QLineEdit(self.layoutWidget2)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.Input_N.setFont(font)
        self.Input_N.setAlignment(QtCore.Qt.AlignCenter)
        self.Input_N.setObjectName("Input_N")
        self.gridLayout_4.addWidget(self.Input_N, 1, 1, 1, 1)
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(10, 300, 491, 73))
        self.widget.setObjectName("widget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.Input_file = QtWidgets.QLineEdit(self.widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.Input_file.setFont(font)
        self.Input_file.setObjectName("Input_file")
        self.gridLayout_2.addWidget(self.Input_file, 0, 0, 1, 4)
        self.btn_openfile = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.btn_openfile.setFont(font)
        self.btn_openfile.setStyleSheet("color: rgb(85, 0, 255);")
        self.btn_openfile.setObjectName("btn_openfile")
        self.gridLayout_2.addWidget(self.btn_openfile, 1, 0, 1, 1)
        self.btn_savefile = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.btn_savefile.setFont(font)
        self.btn_savefile.setStyleSheet("color: rgb(74, 221, 0);")
        self.btn_savefile.setObjectName("btn_savefile")
        self.gridLayout_2.addWidget(self.btn_savefile, 1, 1, 1, 1)
        self.btn_resetfile = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.btn_resetfile.setFont(font)
        self.btn_resetfile.setStyleSheet("color: rgb(255, 255, 0);\n"
"color: rgb(206, 206, 0);")
        self.btn_resetfile.setObjectName("btn_resetfile")
        self.gridLayout_2.addWidget(self.btn_resetfile, 1, 2, 1, 1)
        self.btn_clean = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.btn_clean.setFont(font)
        self.btn_clean.setStyleSheet("color: rgb(255, 0, 0);")
        self.btn_clean.setObjectName("btn_clean")
        self.gridLayout_2.addWidget(self.btn_clean, 1, 3, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.btn_openfile.clicked.connect(self.browsefile)
        self.btn_savefile.clicked.connect(self.save_file)
        self.btn_clean.clicked.connect(self.clean_log)
        self.btn_resetfile.clicked.connect(self.reset_file)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "CT值曲線圖"))
        self.label_well1.setText(_translate("MainWindow", "A1"))
        self.label_well9.setText(_translate("MainWindow", "B1"))
        self.label_well2.setText(_translate("MainWindow", "A2"))
        self.label_well10.setText(_translate("MainWindow", "B2"))
        self.label_well3.setText(_translate("MainWindow", "A3"))
        self.label_well11.setText(_translate("MainWindow", "B3"))
        self.label_well4.setText(_translate("MainWindow", "A4"))
        self.label_well12.setText(_translate("MainWindow", "B4"))
        self.label_well5.setText(_translate("MainWindow", "A5"))
        self.label_well13.setText(_translate("MainWindow", "B5"))
        self.label_well6.setText(_translate("MainWindow", "A6"))
        self.label_well14.setText(_translate("MainWindow", "B6"))
        self.label_well7.setText(_translate("MainWindow", "A7"))
        self.label_well15.setText(_translate("MainWindow", "B7"))
        self.label_well8.setText(_translate("MainWindow", "A8"))
        self.label_well16.setText(_translate("MainWindow", "B8"))
        self.label_7.setText(_translate("MainWindow", "~"))
        # self.label_Timeofbackground.setText(_translate("MainWindow", "Time of background(min)"))
        self.label_Timeofbackground.setText(_translate("MainWindow", "背景時間(分鐘)"))
        self.label_Threshold.setText(_translate("MainWindow", "Threshold: N  * Std"))
        self.label_N.setText(_translate("MainWindow", "N :"))
        self.btn_openfile.setText(_translate("MainWindow", "Open"))
        self.btn_savefile.setText(_translate("MainWindow", "Save"))
        self.btn_resetfile.setText(_translate("MainWindow", "Reset"))
        self.btn_clean.setText(_translate("MainWindow", "Clean"))
