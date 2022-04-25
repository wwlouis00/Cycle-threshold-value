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
import sys
from PyQt5 import QtCore, QtGui, QtWidgets

#曲線顏色
colorTab_More4 = ['#e8a5eb', '#facc9e', '#e8e948', '#1bb763',
                       '#25f2f3', '#1db3ea', '#d1aef8', '#c8c92c',
                       '#f32020', '#fd9b09', '#406386', '#24a1a1',
                       '#1515f8', '#959697', '#744a20', '#7b45a5']



class Ui_MainWindow(QtWidgets.QWidget):
    def browsefile(self):
        if not os.path.isdir('./result'):
            print("Directory 'result' does not exist.")
            os.mkdir('./result')
        print(now_output_time +" >> Choose file(csv) ....")
        self.fname = QFileDialog.getOpenFileName(self, '開啟csv檔案', 'C:\Program Files (x86)', 'csv files (*.csv)')
        self.file_csv_input.setText(self.fname[0])
        print(now_output_time +" >> Open File: " + str(self.fname[0]))
    
    def calculate(self):
        self.big_well = []
        self.big_data = []
        if self.baseline_start_time.text() == "" or self.baseline_end_time.text() == "" or self.Input_N.text() == "":
            QtWidgets.QMessageBox.critical(self, u"Waring", u"Please input 'Start time' and 'End time' and 'Threshold: N * Std: '", buttons=QtWidgets.QMessageBox.Ok, defaultButton=QtWidgets.QMessageBox.Ok)
        self.df_raw = pd.read_csv(self.fname[0])
        self.df_raw.reset_index(inplace=True)

        self.df_raw.rename(columns={'time':'well_1', 'A1':'well_2', 'A2':'well_3', 'A3':'well_4',
                            'A4':'well_5', 'A5':'well_6', 'A6':'well_7', 'A7':'well_8',
                            'A8':'well_9', 'B1':'well_10', 'B2':'well_11', 'B3':'well_12',
                            'B4':'well_13', 'B5':'well_14', 'B6':'well_15', 'B7':'well_16'},inplace = True)
        self.df_raw.drop(labels=["B8"], axis="columns")

        print("*" * 150)
        print(self.df_raw)
        print("*" * 150)

        self.df_normalization = self.df_raw.copy()
        self.get_accumulation_time()
        self.normalize()
        threshold_value = self.get_ct_threshold()
        # UI顯示 16個CT值
        self.Ct_value = self.get_ct_value(threshold_value)

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
            StdDev.append(df_current_well[int(self.baseline_start_time.text()) * 2:int(self.baseline_end_time.text()) * 2].std())
            Avg.append(df_current_well[int(self.baseline_start_time.text()) * 2:int(self.baseline_end_time.text()) * 2].mean())
        return StdDev, Avg

    def normalize(self):
        for i in range(0, 16):
            df_current_well = self.df_raw[f'well_{i + 1}']
            self.baseline = df_current_well[int(self.baseline_start_time.text()) * 2:int(self.baseline_end_time.text()) * 2].mean()
            self.df_normalization[f'well{i + 1}'] = (self.df_raw[f'well_{i + 1}'] - self.baseline) / self.baseline
            if(i<8):
                print(f'A{i+1}'+" baseline value: " + str(self.baseline))
            else:
                print(f'B{i-7}'+" baseline value: " + str(self.baseline))

            # print(f'well_{i+1}'+" 的baseline值: " + str(self.baseline))
            # print(self.baseline)# normalized = (IF(t)-IF(b))/IF(b)
        print("*"*100)

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
        if self.file_csv_input.text() == "":
            QtWidgets.QMessageBox.critical(self, u"存取失敗", u"未開啟csv檔案", buttons=QtWidgets.QMessageBox.Ok,
                defaultButton=QtWidgets.QMessageBox.Ok)
        #儲存成功
        else:
            QtWidgets.QMessageBox.information(self, u"存取成功", u"已成功另存Excel檔案", buttons=QtWidgets.QMessageBox.Ok,
                defaultButton=QtWidgets.QMessageBox.Ok)
            print("Save data successful !!!")
            #設置資料欄位
            self.save_excel = pd.DataFrame({"A1": [self.Ct_value[0]], "A2": [self.Ct_value[1]],
                                            "A3": [self.Ct_value[2]], "A4": [self.Ct_value[3]],
                                            "A5": [self.Ct_value[4]], "A6": [self.Ct_value[5]],
                                            "A7": [self.Ct_value[6]], "A8": [self.Ct_value[7]],
                                            "B1": [self.Ct_value[8]], "B2": [self.Ct_value[9]],
                                            "B3": [self.Ct_value[10]], "B4": [self.Ct_value[11]],
                                            "B5": [self.Ct_value[12]], "B6": [self.Ct_value[13]],
                                            "B7": [self.Ct_value[14]], "B8": [self.Ct_value[15]]}
                , index=["CT_Value"])
            #儲存資料以及存取位置
            self.move_finish.to_csv('./result/Display_result/CT_Value_'+ now_output_time + '_MA_data.csv', encoding="utf_8_sig")
            self.save_excel.T.to_csv('./result/Display_result/CT_Value' + now_output_time + "all_well.csv", encoding="utf_8_sig")
    #清除顯示

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(959, 798)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Threshold = QtWidgets.QGroupBox(self.centralwidget)
        self.Threshold.setGeometry(QtCore.QRect(10, 354, 931, 409))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.Threshold.setFont(font)
        self.Threshold.setStyleSheet("border-color: rgb(85, 255, 255);")
        self.Threshold.setObjectName("Threshold")
        self.Threshold_function = QtWidgets.QGroupBox(self.Threshold)
        self.Threshold_function.setGeometry(QtCore.QRect(20, 96, 341, 301))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.Threshold_function.setFont(font)
        self.Threshold_function.setObjectName("Threshold_function")
        self.Baseline = QtWidgets.QGroupBox(self.Threshold_function)
        self.Baseline.setGeometry(QtCore.QRect(10, 42, 321, 67))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.Baseline.setFont(font)
        self.Baseline.setObjectName("Baseline")
        self.layoutWidget = QtWidgets.QWidget(self.Baseline)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 25, 301, 32))
        self.layoutWidget.setObjectName("layoutWidget")
        self.baseline = QtWidgets.QGridLayout(self.layoutWidget)
        self.baseline.setContentsMargins(0, 0, 0, 0)
        self.baseline.setObjectName("baseline")
        self.baseline_start = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.baseline_start.setFont(font)
        self.baseline_start.setAlignment(QtCore.Qt.AlignCenter)
        self.baseline_start.setObjectName("baseline_start")
        self.baseline.addWidget(self.baseline_start, 0, 0, 1, 1)
        self.baseline_start_time = QtWidgets.QLineEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.baseline_start_time.setFont(font)
        self.baseline_start_time.setAlignment(QtCore.Qt.AlignCenter)
        self.baseline_start_time.setObjectName("baseline_start_time")
        self.baseline.addWidget(self.baseline_start_time, 0, 1, 1, 1)
        self.baseline_end = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.baseline_end.setFont(font)
        self.baseline_end.setAlignment(QtCore.Qt.AlignCenter)
        self.baseline_end.setObjectName("baseline_end")
        self.baseline.addWidget(self.baseline_end, 0, 2, 1, 1)
        self.baseline_end_time = QtWidgets.QLineEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.baseline_end_time.setFont(font)
        self.baseline_end_time.setAlignment(QtCore.Qt.AlignCenter)
        self.baseline_end_time.setObjectName("baseline_end_time")
        self.baseline.addWidget(self.baseline_end_time, 0, 3, 1, 1)
        self.update_calculation = QtWidgets.QPushButton(self.Threshold_function)
        self.update_calculation.setGeometry(QtCore.QRect(140, 252, 191, 37))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.update_calculation.setFont(font)
        self.update_calculation.setObjectName("update_calculation")
        self.widget = QtWidgets.QWidget(self.Threshold_function)
        self.widget.setGeometry(QtCore.QRect(20, 174, 301, 26))
        self.widget.setObjectName("widget")
        self.Threshold_N = QtWidgets.QGridLayout(self.widget)
        self.Threshold_N.setContentsMargins(0, 0, 0, 0)
        self.Threshold_N.setObjectName("Threshold_N")
        self.label_threshold = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_threshold.setFont(font)
        self.label_threshold.setAlignment(QtCore.Qt.AlignCenter)
        self.label_threshold.setObjectName("label_threshold")
        self.Threshold_N.addWidget(self.label_threshold, 0, 0, 1, 1)
        self.Input_N = QtWidgets.QLineEdit(self.widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Input_N.setFont(font)
        self.Input_N.setAlignment(QtCore.Qt.AlignCenter)
        self.Input_N.setObjectName("Input_N")
        self.Threshold_N.addWidget(self.Input_N, 0, 1, 1, 1)
        self.verticalLayoutWidget = QtWidgets.QWidget(self.Threshold)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(380, 108, 311, 289))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.result_grip = QtWidgets.QGridLayout(self.verticalLayoutWidget)
        self.result_grip.setContentsMargins(0, 0, 0, 0)
        self.result_grip.setObjectName("result_grip")
        self.result_value = QtWidgets.QTableWidget(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.result_value.setFont(font)
        self.result_value.setObjectName("result_value")
        self.result_value.setColumnCount(2)
        self.result_value.setRowCount(16)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(12)
        item.setFont(font)
        self.result_value.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(12)
        item.setFont(font)
        self.result_value.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(12)
        item.setFont(font)
        self.result_value.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(12)
        item.setFont(font)
        self.result_value.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(12)
        item.setFont(font)
        self.result_value.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(12)
        item.setFont(font)
        self.result_value.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(12)
        item.setFont(font)
        self.result_value.setVerticalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(12)
        item.setFont(font)
        self.result_value.setVerticalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(12)
        item.setFont(font)
        self.result_value.setVerticalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(12)
        item.setFont(font)
        self.result_value.setVerticalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(12)
        item.setFont(font)
        self.result_value.setVerticalHeaderItem(10, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(12)
        item.setFont(font)
        self.result_value.setVerticalHeaderItem(11, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(12)
        item.setFont(font)
        self.result_value.setVerticalHeaderItem(12, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(12)
        item.setFont(font)
        self.result_value.setVerticalHeaderItem(13, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(12)
        item.setFont(font)
        self.result_value.setVerticalHeaderItem(14, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(12)
        item.setFont(font)
        self.result_value.setVerticalHeaderItem(15, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(12)
        item.setFont(font)
        self.result_value.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(12)
        item.setFont(font)
        self.result_value.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsDropEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsTristate)
        self.result_value.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(12)
        item.setFont(font)
        self.result_value.setItem(0, 1, item)
        self.result_grip.addWidget(self.result_value, 0, 0, 1, 1)
        self.File = QtWidgets.QGroupBox(self.Threshold)
        self.File.setGeometry(QtCore.QRect(20, 24, 901, 67))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.File.setFont(font)
        self.File.setObjectName("File")
        self.file_csv = QtWidgets.QLabel(self.File)
        self.file_csv.setGeometry(QtCore.QRect(10, 30, 71, 25))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.file_csv.setFont(font)
        self.file_csv.setAlignment(QtCore.Qt.AlignCenter)
        self.file_csv.setObjectName("file_csv")
        self.file_csv_input = QtWidgets.QLineEdit(self.File)
        self.file_csv_input.setGeometry(QtCore.QRect(90, 24, 621, 37))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.file_csv_input.setFont(font)
        self.file_csv_input.setObjectName("file_csv_input")
        self.file_open = QtWidgets.QPushButton(self.File)
        self.file_open.setGeometry(QtCore.QRect(720, 24, 171, 37))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.file_open.setFont(font)
        self.file_open.setObjectName("file_open")
        self.layoutWidget1 = QtWidgets.QWidget(self.Threshold)
        self.layoutWidget1.setGeometry(QtCore.QRect(740, 108, 181, 115))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.btn_save = QtWidgets.QPushButton(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btn_save.setFont(font)
        self.btn_save.setStyleSheet("color: rgb(0, 170, 0);")
        self.btn_save.setObjectName("btn_save")
        self.verticalLayout.addWidget(self.btn_save)
        self.btn_capture = QtWidgets.QPushButton(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btn_capture.setFont(font)
        self.btn_capture.setObjectName("btn_capture")
        self.verticalLayout.addWidget(self.btn_capture)
        self.btn_clear = QtWidgets.QPushButton(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btn_clear.setFont(font)
        self.btn_clear.setStyleSheet("color: rgb(255, 0, 0);")
        self.btn_clear.setObjectName("btn_clear")
        self.verticalLayout.addWidget(self.btn_clear)
        self.Sample = QtWidgets.QGroupBox(self.centralwidget)
        self.Sample.setGeometry(QtCore.QRect(800, 6, 141, 343))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Sample.setFont(font)
        self.Sample.setObjectName("Sample")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.Sample)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_A = QtWidgets.QVBoxLayout()
        self.verticalLayout_A.setObjectName("verticalLayout_A")
        self.CT_A1 = QtWidgets.QCheckBox(self.Sample)
        self.CT_A1.setObjectName("CT_A1")
        self.verticalLayout_A.addWidget(self.CT_A1)
        self.CT_A2 = QtWidgets.QCheckBox(self.Sample)
        self.CT_A2.setObjectName("CT_A2")
        self.verticalLayout_A.addWidget(self.CT_A2)
        self.CT_A3 = QtWidgets.QCheckBox(self.Sample)
        self.CT_A3.setObjectName("CT_A3")
        self.verticalLayout_A.addWidget(self.CT_A3)
        self.CT_A4 = QtWidgets.QCheckBox(self.Sample)
        self.CT_A4.setObjectName("CT_A4")
        self.verticalLayout_A.addWidget(self.CT_A4)
        self.CT_A5 = QtWidgets.QCheckBox(self.Sample)
        self.CT_A5.setObjectName("CT_A5")
        self.verticalLayout_A.addWidget(self.CT_A5)
        self.CT_A6 = QtWidgets.QCheckBox(self.Sample)
        self.CT_A6.setObjectName("CT_A6")
        self.verticalLayout_A.addWidget(self.CT_A6)
        self.CT_A7 = QtWidgets.QCheckBox(self.Sample)
        self.CT_A7.setObjectName("CT_A7")
        self.verticalLayout_A.addWidget(self.CT_A7)
        self.CT_A8 = QtWidgets.QCheckBox(self.Sample)
        self.CT_A8.setObjectName("CT_A8")
        self.verticalLayout_A.addWidget(self.CT_A8)
        self.gridLayout.addLayout(self.verticalLayout_A, 0, 0, 1, 1)
        self.verticalLayout_B = QtWidgets.QVBoxLayout()
        self.verticalLayout_B.setObjectName("verticalLayout_B")
        self.CT_B1 = QtWidgets.QCheckBox(self.Sample)
        self.CT_B1.setObjectName("CT_B1")
        self.verticalLayout_B.addWidget(self.CT_B1)
        self.CT_B2 = QtWidgets.QCheckBox(self.Sample)
        self.CT_B2.setObjectName("CT_B2")
        self.verticalLayout_B.addWidget(self.CT_B2)
        self.CT_B3 = QtWidgets.QCheckBox(self.Sample)
        self.CT_B3.setObjectName("CT_B3")
        self.verticalLayout_B.addWidget(self.CT_B3)
        self.CT_B4 = QtWidgets.QCheckBox(self.Sample)
        self.CT_B4.setObjectName("CT_B4")
        self.verticalLayout_B.addWidget(self.CT_B4)
        self.CT_B5 = QtWidgets.QCheckBox(self.Sample)
        self.CT_B5.setObjectName("CT_B5")
        self.verticalLayout_B.addWidget(self.CT_B5)
        self.CT_B6 = QtWidgets.QCheckBox(self.Sample)
        self.CT_B6.setObjectName("CT_B6")
        self.verticalLayout_B.addWidget(self.CT_B6)
        self.CT_B7 = QtWidgets.QCheckBox(self.Sample)
        self.CT_B7.setObjectName("CT_B7")
        self.verticalLayout_B.addWidget(self.CT_B7)
        self.CT_B8 = QtWidgets.QCheckBox(self.Sample)
        self.CT_B8.setObjectName("CT_B8")
        self.verticalLayout_B.addWidget(self.CT_B8)
        self.gridLayout.addLayout(self.verticalLayout_B, 0, 1, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.version = QtWidgets.QLabel(self.centralwidget)
        self.version.setGeometry(QtCore.QRect(10, 762, 301, 25))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.version.setFont(font)
        self.version.setObjectName("version")
        self.Plot = QtWidgets.QGroupBox(self.centralwidget)
        self.Plot.setGeometry(QtCore.QRect(10, 7, 781, 343))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Plot.setFont(font)
        self.Plot.setObjectName("Plot")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.Plot)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.Plot_display = QtWidgets.QGraphicsView(self.Plot)
        self.Plot_display.setObjectName("Plot_display")
        self.gridLayout_2.addWidget(self.Plot_display, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        #執行功能
        self.file_open.clicked.connect(self.browsefile)
        self.update_calculation.clicked.connect(self.calculate)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Amplification Plot"))
        self.Threshold.setTitle(_translate("MainWindow", "Threshold Cycle Calculation"))
        self.Threshold_function.setTitle(_translate("MainWindow", "Threshold"))
        self.Baseline.setTitle(_translate("MainWindow", "Baseline(Min)"))
        self.baseline_start.setText(_translate("MainWindow", "Start:"))
        self.baseline_end.setText(_translate("MainWindow", "End:"))
        self.update_calculation.setText(_translate("MainWindow", "Update Calculations"))
        self.label_threshold.setText(_translate("MainWindow", "Threshold: N  * Std: "))
        item = self.result_value.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "A1"))
        item = self.result_value.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "A2"))
        item = self.result_value.verticalHeaderItem(2)
        item.setText(_translate("MainWindow", "A3"))
        item = self.result_value.verticalHeaderItem(3)
        item.setText(_translate("MainWindow", "A4"))
        item = self.result_value.verticalHeaderItem(4)
        item.setText(_translate("MainWindow", "A5"))
        item = self.result_value.verticalHeaderItem(5)
        item.setText(_translate("MainWindow", "A6"))
        item = self.result_value.verticalHeaderItem(6)
        item.setText(_translate("MainWindow", "A7"))
        item = self.result_value.verticalHeaderItem(7)
        item.setText(_translate("MainWindow", "A8"))
        item = self.result_value.verticalHeaderItem(8)
        item.setText(_translate("MainWindow", "B1"))
        item = self.result_value.verticalHeaderItem(9)
        item.setText(_translate("MainWindow", "B2"))
        item = self.result_value.verticalHeaderItem(10)
        item.setText(_translate("MainWindow", "B3"))
        item = self.result_value.verticalHeaderItem(11)
        item.setText(_translate("MainWindow", "B4"))
        item = self.result_value.verticalHeaderItem(12)
        item.setText(_translate("MainWindow", "B5"))
        item = self.result_value.verticalHeaderItem(13)
        item.setText(_translate("MainWindow", "B6"))
        item = self.result_value.verticalHeaderItem(14)
        item.setText(_translate("MainWindow", "B7"))
        item = self.result_value.verticalHeaderItem(15)
        item.setText(_translate("MainWindow", "B8"))
        item = self.result_value.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Ct Value"))
        item = self.result_value.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Std Dev"))
        __sortingEnabled = self.result_value.isSortingEnabled()
        self.result_value.setSortingEnabled(False)
        self.result_value.setSortingEnabled(__sortingEnabled)
        self.File.setTitle(_translate("MainWindow", "File(Csv)"))
        self.file_csv.setText(_translate("MainWindow", "Dir:"))
        self.file_open.setText(_translate("MainWindow", "Open(Csv)"))
        self.btn_save.setText(_translate("MainWindow", "Save"))
        self.btn_capture.setText(_translate("MainWindow", "Capture"))
        self.btn_clear.setText(_translate("MainWindow", "Clear"))
        self.Sample.setTitle(_translate("MainWindow", "Samples"))
        self.CT_A1.setText(_translate("MainWindow", "A1"))
        self.CT_A2.setText(_translate("MainWindow", "A2"))
        self.CT_A3.setText(_translate("MainWindow", "A3"))
        self.CT_A4.setText(_translate("MainWindow", "A4"))
        self.CT_A5.setText(_translate("MainWindow", "A5"))
        self.CT_A6.setText(_translate("MainWindow", "A6"))
        self.CT_A7.setText(_translate("MainWindow", "A7"))
        self.CT_A8.setText(_translate("MainWindow", "A8"))
        self.CT_B1.setText(_translate("MainWindow", "B1"))
        self.CT_B2.setText(_translate("MainWindow", "B2"))
        self.CT_B3.setText(_translate("MainWindow", "B3"))
        self.CT_B4.setText(_translate("MainWindow", "B4"))
        self.CT_B5.setText(_translate("MainWindow", "B5"))
        self.CT_B6.setText(_translate("MainWindow", "B6"))
        self.CT_B7.setText(_translate("MainWindow", "B7"))
        self.CT_B8.setText(_translate("MainWindow", "B8"))
        self.version.setText(_translate("MainWindow", "WinnoZ. V. 1.0.2"))
        self.Plot.setTitle(_translate("MainWindow", "Plot"))

if __name__ == '__main__':
    print("*" * 50)
    print("Now Time: " + now_output_time)
    app = QApplication(sys.argv)
    mainWindows = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(mainWindows)
    mainWindows.show()
    sys.exit(app.exec_())