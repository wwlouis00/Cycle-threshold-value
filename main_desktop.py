from PyQt5.QtWidgets import*
# from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication, QLabel
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
import os
import pandas as pd
import numpy as np
from datetime import datetime
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import sys

first_time,twice_time,n_sd  = 4,14,10

now_output_time = str(datetime.now().strftime('%Y-%m-%d %H-%M-%S'))
#Color
colorTab_More4 = ['#e8a5eb', '#facc9e', '#e8e948', '#1bb763',
                  '#25f2f3', '#1db3ea', '#d1aef8', '#c8c92c',
                  '#f32020', '#fd9b09', '#406386', '#24a1a1',
                  '#1515f8', '#959697', '#744a20', '#7b45a5']
class MatplotlibWidget(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        # loadUi("CT_Manager.ui",self)
        loadUi("CT_Manager_desktop.ui",self)
        self.setWindowTitle("CT_Value")
        self.addToolBar(NavigationToolbar(self.MplWidget.canvas, self))
        self.connect_signals()
        self.slider_func()

        
        
    def connect_signals(self):
        self.slider_begin.valueChanged.connect(self.sl_begin)
        self.slider_end.valueChanged.connect(self.sl_begin)
        self.A1_radio.clicked.connect(self.slider_func)
        self.A2_radio.clicked.connect(self.slider_func)
        self.A3_radio.clicked.connect(self.slider_func)
        self.A4_radio.clicked.connect(self.slider_func)
        self.A5_radio.clicked.connect(self.slider_func)
        self.A6_radio.clicked.connect(self.slider_func)
        self.A7_radio.clicked.connect(self.slider_func)
        self.A8_radio.clicked.connect(self.slider_func)
        self.B1_radio.clicked.connect(self.slider_func)
        self.B2_radio.clicked.connect(self.slider_func)
        self.B3_radio.clicked.connect(self.slider_func)
        self.B4_radio.clicked.connect(self.slider_func)
        self.B5_radio.clicked.connect(self.slider_func)
        self.B6_radio.clicked.connect(self.slider_func)
        self.B7_radio.clicked.connect(self.slider_func)
        self.B8_radio.clicked.connect(self.slider_func)
        self.All_radio.clicked.connect(self.slider_func)
        self.actionOpen.triggered.connect(self.browsefile)
        self.actionSave.triggered.connect(self.save_file)
        self.actionExit.triggered.connect(qApp.quit)
        ################################################
        # self.CT_A1.clicked.connect(self.slider_func)
        # self.CT_A2.clicked.connect(self.slider_func)
        # self.CT_A3.clicked.connect(self.slider_func)
        # self.A4_radio.clicked.connect(self.slider_func)
        # self.A5_radio.clicked.connect(self.slider_func)
        # self.A6_radio.clicked.connect(self.slider_func)
        # self.A7_radio.clicked.connect(self.slider_func)
        # self.A8_radio.clicked.connect(self.slider_func)
        # self.B1_radio.clicked.connect(self.slider_func)
        # self.B2_radio.clicked.connect(self.slider_func)
        # self.B3_radio.clicked.connect(self.slider_func)
        # self.B4_radio.clicked.connect(self.slider_func)
        # self.B5_radio.clicked.connect(self.slider_func)
        # self.B6_radio.clicked.connect(self.slider_func)
        # self.B7_radio.clicked.connect(self.slider_func)
        # self.B8_radio.clicked.connect(self.slider_func)
        self.All_radio.clicked.connect(self.slider_func)
        self.origin_radio.clicked.connect(self.slider_func)
        self.Clear_radio.clicked.connect(self.clear_radio)
        self.nor_radio.clicked.connect(self.nor_data)
        self.main_radio.clicked.connect(self.main_data)
        
        
        
    def browsefile(self):
        if not os.path.isdir('./result'):
            os.mkdir('./result')
            os.mkdir('./result/Cali_result/')
            os.mkdir('./result/Display_result/')
        self.fname = QFileDialog.getOpenFileName(self, '開啟csv檔案', 'C:\Program Files (x86)', 'csv files (*.csv)')
        if(self.fname[0]==""):
            None
        else:
            self.Input_file.setText(self.fname[0])
            self.df_raw = pd.read_csv(self.fname[0])
            self.df_raw.reset_index(inplace=True)
            self.origin_time = []
            #Csv data has "accumulated time" column
            if 'accumulated time' in self.df_raw.columns:
                self.df_raw = self.df_raw.drop(labels=["time"], axis="columns")
                self.df_raw.rename(columns={'A1':'well_2', 'A2':'well_3', 'A3':'well_4',
                                            'A4':'well_5', 'A5':'well_6', 'A6':'well_7', 'A7':'well_8',
                                            'A8':'well_9', 'B1':'well_10', 'B2':'well_11', 'B3':'well_12',
                                            'B4':'well_13','B5':'well_14', 'B6':'well_15', 'B7':'well_16'},inplace = True)
                self.df_raw.rename(columns={'accumulated time':'well_1','index':'time'},inplace = True)
                self.df_raw = self.df_raw.drop(labels=["B8"], axis="columns")
            #Csv data has not "accumulated time" column
            else:
                self.df_raw.rename(columns={'time':'well_1','A1':'well_2', 'A2':'well_3', 'A3':'well_4',
                                            'A4':'well_5', 'A5':'well_6', 'A6':'well_7', 'A7':'well_8',
                                            'A8':'well_9', 'B1':'well_10', 'B2':'well_11', 'B3':'well_12',
                                            'B4':'well_13','B5':'well_14', 'B6':'well_15', 'B7':'well_16'},inplace = True)
                self.df_raw = self.df_raw.drop(labels=["B8"], axis="columns")
                self.df_raw.rename(columns={"index": "time"},inplace=True)
            print("-"*150)
            print(self.df_raw)
            print("-"*150)
            for j in range(0, len(self.df_raw.index), 1):
                self.origin_time.append(j)
            print(self.origin_time)
            self.origin_data()
            self.calculate()
    
    def origin_data(self):
        self.MplWidget.canvas.axes.clear()
        self.MplWidget.canvas.axes.plot(self.origin_time, self.df_raw['well_1'],color =colorTab_More4[0],label="A1")
        self.MplWidget.canvas.axes.plot(self.origin_time, self.df_raw['well_2'],color =colorTab_More4[1],label="A2")
        self.MplWidget.canvas.axes.plot(self.origin_time, self.df_raw['well_3'],color =colorTab_More4[2],label="A3")
        self.MplWidget.canvas.axes.plot(self.origin_time, self.df_raw['well_4'],color =colorTab_More4[3],label="A4")
        self.MplWidget.canvas.axes.plot(self.origin_time, self.df_raw['well_5'],color =colorTab_More4[4],label="A5")
        self.MplWidget.canvas.axes.plot(self.origin_time, self.df_raw['well_6'],color =colorTab_More4[5],label="A6")
        self.MplWidget.canvas.axes.plot(self.origin_time, self.df_raw['well_7'],color =colorTab_More4[6],label="A7")
        self.MplWidget.canvas.axes.plot(self.origin_time, self.df_raw['well_8'],color =colorTab_More4[7],label="A8")
        self.MplWidget.canvas.axes.plot(self.origin_time, self.df_raw['well_9'],color =colorTab_More4[8],label="B1")
        self.MplWidget.canvas.axes.plot(self.origin_time, self.df_raw['well_10'],color =colorTab_More4[9],label="B2")
        self.MplWidget.canvas.axes.plot(self.origin_time, self.df_raw['well_11'],color =colorTab_More4[10],label="B3")
        self.MplWidget.canvas.axes.plot(self.origin_time, self.df_raw['well_12'],color =colorTab_More4[11],label="B4")
        self.MplWidget.canvas.axes.plot(self.origin_time, self.df_raw['well_13'],color =colorTab_More4[12],label="B5")
        self.MplWidget.canvas.axes.plot(self.origin_time, self.df_raw['well_14'],color =colorTab_More4[13],label="B6")
        self.MplWidget.canvas.axes.plot(self.origin_time, self.df_raw['well_15'],color =colorTab_More4[14],label="B7")
        self.MplWidget.canvas.axes.plot(self.origin_time, self.df_raw['well_16'],color =colorTab_More4[15],label="B8")
        self.MplWidget.canvas.axes.set_xlim(0,len(self.df_raw.index))
        self.MplWidget.canvas.axes.set_xlabel("Time (min)", fontsize=10)  # Inserta el título del eje X
        self.MplWidget.canvas.axes.set_ylabel("Normalized fluorescent intensity", fontsize=10) 
        self.MplWidget.canvas.axes.legend(loc='upper left',shadow=True, ncol=4, fontsize=10)
        self.MplWidget.canvas.axes.set_title('Amplification curve', fontsize=10)
        self.MplWidget.canvas.draw()
            
    def calculate(self):
        self.big_well = []
        self.big_data = []
        self.big_array = []
        self.df_normalization = self.df_raw.copy()
        self.get_accumulation_time()
        self.normalize()
        threshold_value = self.get_ct_threshold()
        #Display A1~B8 CT Value
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
        self.B5_data = []
        self.B6_data = []
        self.B7_data = []
        self.B8_data = []
        self.time_array,self.nor_array,self.nor_plot = [],[],[]
        for i in range(0,16,1):      
            self.nor_array.append(self.df_normalization[f'well{i+1}'].mean())
        self.nor_mean = np.mean(self.nor_array)

        for i in range(1, 17, 1):
            self.big_data.append(self.df_normalization["well"+str(i)])
            # self.big_data.append(self.df_normalization["well"+str(i)].rolling(window=5).mean())
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
            self.nor_plot.append(self.nor_mean)

        for j in range(0, len(self.move_finish.index), 1):
            self.time_array.append(j / 2)
        
        self.big_array.append(self.A1_data)
        self.big_array.append(self.A2_data)
        self.big_array.append(self.A3_data)
        self.big_array.append(self.A4_data)
        self.big_array.append(self.A5_data)
        self.big_array.append(self.A6_data)
        self.big_array.append(self.A7_data)
        self.big_array.append(self.A8_data)
        self.big_array.append(self.B1_data)
        self.big_array.append(self.B2_data)
        self.big_array.append(self.B3_data)
        self.big_array.append(self.B4_data)
        self.big_array.append(self.B5_data)
        self.big_array.append(self.B6_data)
        self.big_array.append(self.B7_data)
        self.big_array.append(self.B8_data)

        self.slider_func()
        self.CT_A1.setText(str(self.Ct_value[0]))
        self.CT_A2.setText(str(self.Ct_value[1]))
        self.CT_A3.setText(str(self.Ct_value[2]))
        self.CT_A4.setText(str(self.Ct_value[3]))
        self.CT_A5.setText(str(self.Ct_value[4]))
        self.CT_A6.setText(str(self.Ct_value[5]))
        self.CT_A7.setText(str(self.Ct_value[6]))
        self.CT_A8.setText(str(self.Ct_value[7]))
        self.CT_B1.setText(str(self.Ct_value[8]))
        self.CT_B2.setText(str(self.Ct_value[9]))
        self.CT_B3.setText(str(self.Ct_value[10]))
        self.CT_B4.setText(str(self.Ct_value[11]))
        self.CT_B5.setText(str(self.Ct_value[12]))
        self.CT_B6.setText(str(self.Ct_value[13]))
        self.CT_B7.setText(str(self.Ct_value[14]))
        self.CT_B8.setText(str(self.Ct_value[15]))

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
            # StdDev.append(df_current_well[int(first_time) * 2 + 1:int(twice_time) * 2 + 1].std())
            StdDev.append(df_current_well[int(self.Start_time.text()) * 2 + 1:int(self.End_time.text()) * 2 + 1].std())
            
            Avg.append(df_current_well[int(self.Start_time.text()) * 2 + 1:int(self.End_time.text()) * 2 + 1].mean())
        return StdDev, Avg

    def normalize(self):
        for i in range(0, 16):
            df_current_well = self.df_raw[f'well_{i + 1}']
            # self.baseline = df_current_well[int(first_time) * 2 + 1:int(twice_time) * 2 + 1].mean()
            self.baseline = df_current_well[int(self.Start_time.text()) * 2 + 1:int(self.End_time.text()) * 2 + 1].mean()
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
            threshold_value.append(int(self.Input_std.text()) * StdDev[i] + Avg[i])
        return threshold_value

    def get_ct_value(self, threshold_value):
        Ct_value = []
        for i in range(0, 16):
            df_current_well = self.df_normalization[f'well_{i + 1}']
            df_accumulation = self.df_normalization['accumulation']
            try:
                for j, row in enumerate(df_current_well):
                    if row >= threshold_value[i] and j > first_time:
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
                        print("Ct value is not available")
            except:
                for j, row in enumerate(df_current_well):
                    if row >= threshold_value[i] and j > first_time:
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
                        break
                    # if there is no Ct_value availible
                    elif j == len(df_current_well) - 1:
                        Ct_value.append("N/A")
                        print("Ct value is not available")
        return Ct_value
    
    def save_file(self):
        #Save fail
        if self.Input_file.text() == "":
            QtWidgets.QMessageBox.critical(self, u"存取失敗", u"未開啟csv檔案", buttons=QtWidgets.QMessageBox.Ok,
                defaultButton=QtWidgets.QMessageBox.Ok)
        #Save successful
        else:
            try :
                if len(self.df_raw.index) < 7:
                    raise
                #setup data 
                self.save_excel = pd.DataFrame({"A1": [self.Ct_value[0]], "A2": [self.Ct_value[1]],
                                                "A3": [self.Ct_value[2]], "A4": [self.Ct_value[3]],
                                                "A5": [self.Ct_value[4]], "A6": [self.Ct_value[5]],
                                                "A7": [self.Ct_value[6]], "A8": [self.Ct_value[7]],
                                                "B1": [self.Ct_value[8]], "B2": [self.Ct_value[9]],
                                                "B3": [self.Ct_value[10]], "B4": [self.Ct_value[11]],
                                                "B5": [self.Ct_value[12]], "B6": [self.Ct_value[13]],
                                                "B7": [self.Ct_value[14]], "B8": [self.Ct_value[15]]}
                    , index=["CT_Value"])
                #Save data and path
                self.save_excel.to_csv('./result/Display_result/CT_Value' + now_output_time + "all_well.csv", encoding="utf_8_sig")
                self.move_finish.T.to_csv('./result/Display_result/CT_Value_'+ now_output_time + '_MA_data.csv', encoding="utf_8_sig")
                print(self.save_excel)
                QtWidgets.QMessageBox.information(self, u"存取成功", u"已成功另存Csv檔案", buttons=QtWidgets.QMessageBox.Ok,
                    defaultButton=QtWidgets.QMessageBox.Ok)
                print("Save data successful !!!")
            except:
                self.save_excel = pd.DataFrame({"A1": [self.Ct_value[0]], "A2": [self.Ct_value[1]],
                                                "A3": [self.Ct_value[2]], "A4": [self.Ct_value[3]],
                                                "A5": [self.Ct_value[4]], "A6": [self.Ct_value[5]],
                                                "A7": [self.Ct_value[6]], "A8": [self.Ct_value[7]],
                                                "B1": [self.Ct_value[8]], "B2": [self.Ct_value[9]],
                                                "B3": [self.Ct_value[10]], "B4": [self.Ct_value[11]],
                                                "B5": [self.Ct_value[12]], "B6": [self.Ct_value[13]],
                                                "B7": [self.Ct_value[14]], "B8": [self.Ct_value[15]]}
                    , index=["CT_Value"])
                #Save data and path
                self.save_excel.to_csv('./result/Display_result/CT_Value' + now_output_time + "all_well.csv", encoding="utf_8_sig")
                self.df_normalization = self.df_normalization.drop(columns=['time','accumulation','shutter_speed','ISO']) #Drop 'time','accumulation','shutter_speed','ISO'
                self.df_normalization.T.to_csv('./result/Display_result/CT_Value_'+ now_output_time + '_MA_data.csv', encoding="utf_8_sig")
                QtWidgets.QMessageBox.information(self, u"存取成功", u"已成功另存Csv檔案", buttons=QtWidgets.QMessageBox.Ok,
                    defaultButton=QtWidgets.QMessageBox.Ok)
                print("Save data successful !!!")
    #Clean all display information
    def clean_log(self):
        self.Input_file.setText("")
        self.MplWidget.canvas.axes.clear()
        self.MplWidget.canvas.draw()
        print("Clean data successful !!!")
    
    def rollingMean(self):
        value = self.ns_baseline_begin.value()
        return value

    def sl_begin(self):
        if self.All_radio.isChecked():
            slider = self.rollingMean()
            self.ns_baseline_begin.display(slider)
            print(slider)
    
    # Display Normalize all chart
    def update_graph(self):
        self.MplWidget.canvas.axes.clear()
        self.MplWidget.canvas.axes.plot(self.time_array, self.A1_data,color =colorTab_More4[0],label="A1")
        self.MplWidget.canvas.axes.plot(self.time_array, self.A2_data,color =colorTab_More4[1],label="A2")
        self.MplWidget.canvas.axes.plot(self.time_array, self.A3_data,color =colorTab_More4[2],label="A3")
        self.MplWidget.canvas.axes.plot(self.time_array, self.A4_data,color =colorTab_More4[3],label="A4")
        self.MplWidget.canvas.axes.plot(self.time_array, self.A5_data,color =colorTab_More4[4],label="A5")
        self.MplWidget.canvas.axes.plot(self.time_array, self.A6_data,color =colorTab_More4[5],label="A6")
        self.MplWidget.canvas.axes.plot(self.time_array, self.A7_data,color =colorTab_More4[6],label="A7")
        self.MplWidget.canvas.axes.plot(self.time_array, self.A8_data,color =colorTab_More4[7],label="A8")
        self.MplWidget.canvas.axes.plot(self.time_array, self.B1_data,color =colorTab_More4[8],label="B1")
        self.MplWidget.canvas.axes.plot(self.time_array, self.B2_data,color =colorTab_More4[9],label="B2")
        self.MplWidget.canvas.axes.plot(self.time_array, self.B3_data,color =colorTab_More4[10],label="B3")
        self.MplWidget.canvas.axes.plot(self.time_array, self.B4_data,color =colorTab_More4[11],label="B4")
        self.MplWidget.canvas.axes.plot(self.time_array, self.B5_data,color =colorTab_More4[12],label="B5")
        self.MplWidget.canvas.axes.plot(self.time_array, self.B6_data,color =colorTab_More4[13],label="B6")
        self.MplWidget.canvas.axes.plot(self.time_array, self.B7_data,color =colorTab_More4[14],label="B7")
        self.MplWidget.canvas.axes.plot(self.time_array, self.B8_data,color =colorTab_More4[15],label="B8")
        self.MplWidget.canvas.axes.plot(self.time_array,self.nor_plot,'o',color = "green", label="Threshold")
        # self.MplWidget.canvas.axes.vlines(first_time,0,2,color="red")
        self.MplWidget.canvas.axes.set_xlim(0,len(self.df_raw.index)/2)
        # self.MplWidget.canvas.axes.set_ylim(-2,4)
        #self.MplWidget.canvas.set_scales(20,0.1)
        self.MplWidget.canvas.axes.set_xlabel("Time (min)", fontsize=10)  # Inserta el título del eje X
        self.MplWidget.canvas.axes.set_ylabel("Normalized fluorescent intensity", fontsize=10) 
        self.MplWidget.canvas.axes.legend(loc='upper center',shadow=True, ncol=5, fontsize=7)
        self.MplWidget.canvas.axes.set_title('Amplification curve', fontsize=10)

        self.MplWidget.canvas.draw()
    
    # Display threshold chart
    def nor_data(self):
        if self.Input_file.text() == "":
            None
        else:
            self.groupBox.setChecked(False)
            self.MplWidget.canvas.axes.clear()
            self.MplWidget.canvas.axes.plot(self.time_array,self.nor_plot,'-',color = "green", label="Normalize")
            self.MplWidget.canvas.axes.set_xlim(0,20)
            # self.MplWidget.canvas.axes.set_ylim(-0.1,0.1)
            #self.MplWidget.canvas.set_scales(20,0.1)
            self.MplWidget.canvas.axes.set_xlabel("Time (min)", fontsize=5)  # Inserta el título del eje X
            self.MplWidget.canvas.axes.set_ylabel("Normalized fluorescent intensity", fontsize=7) 
            self.MplWidget.canvas.axes.legend(loc='upper center',shadow=True, ncol=4, fontsize=5)
            self.MplWidget.canvas.axes.set_title('Amplification curve', fontsize=7)
            self.MplWidget.canvas.draw()
    #Display Normalize and all(A1~B8) chart
    def main_data(self):
        if self.Input_file.text() == "":
            None
        else:
            self.groupBox.setChecked(True)
            self.slider_func()
    #Choose one chart
    def slider_func(self):
        if self.Input_file.text() == "":
            None
        elif self.Clear_radio.isChecked():
            self.MplWidget.canvas.axes.clear()
            self.MplWidget.canvas.draw()

        elif self.nor_radio.isChecked():
            self.nor_data()
        
        elif self.origin_radio.isChecked():
            self.origin_data()

        else:
            if self.All_radio.isChecked():
                self.update_graph()
            else:
                if self.A1_radio.isChecked():
                    plot = 0
                    plot_color = 0
                    plot_channel = 'A1'

                if self.A2_radio.isChecked():
                    plot = 1
                    plot_color = 1
                    plot_channel = 'A2'
                if self.A3_radio.isChecked():
                    plot = 2
                    plot_color = 2
                    plot_channel = 'A3'
                if self.A4_radio.isChecked():
                    plot = 3
                    plot_color = 3
                    plot_channel = 'A4'
                if self.A5_radio.isChecked():
                    plot = 4
                    plot_color = 4
                    plot_channel = 'A5'
                if self.A6_radio.isChecked():
                    plot = 5
                    plot_color = 5
                    plot_channel = 'A6'
                if self.A7_radio.isChecked():
                    plot = 6
                    plot_color = 6
                    plot_channel = 'A7'
                if self.A8_radio.isChecked():
                    plot = 7
                    plot_color = 7
                    plot_channel = 'A8'
                if self.B1_radio.isChecked():
                    plot = 8
                    plot_color = 8
                    plot_channel = 'B1'
                if self.B2_radio.isChecked():
                    plot = 9
                    plot_color = 9
                    plot_channel = 'B2'
                if self.B3_radio.isChecked():
                    plot = 10
                    plot_color = 10
                    plot_channel = 'B3'
                if self.B4_radio.isChecked():
                    plot = 11
                    plot_color = 11
                    plot_channel = 'B4'
                if self.B5_radio.isChecked():
                    plot = 12
                    plot_color = 12
                    plot_channel = 'B5'
                if self.B6_radio.isChecked():
                    plot = 13
                    plot_color = 13
                    plot_channel = 'B6'
                if self.B7_radio.isChecked():
                    plot = 14
                    plot_color = 14
                    plot_channel = 'B7'
                if self.B8_radio.isChecked():
                    plot = 15
                    plot_color = 15
                    plot_channel = 'B8'
                self.slider_func_plot(plot,plot_color,plot_channel)
    def clear_radio(self):
        if self.Clear_radio.isChecked():
            self.MplWidget.canvas.axes.clear()
            self.MplWidget.canvas.draw()
    def slider_func_plot(self,plot,plot_color,plot_channel):
        self.MplWidget.canvas.axes.clear()
        self.MplWidget.canvas.axes.plot(self.time_array, self.big_array[plot],color =colorTab_More4[plot_color],label= plot_channel)
        self.MplWidget.canvas.axes.set_xlim(0,len(self.df_raw.index)/2)
        # self.MplWidget.canvas.axes.set_ylim(-0.1,0.1)
        #self.MplWidget.canvas.set_scales(20,0.1)
        self.MplWidget.canvas.axes.set_xlabel("Time (min)", fontsize=10)  # Inserta el título del eje X
        self.MplWidget.canvas.axes.set_ylabel("Normalized fluorescent intensity", fontsize=7)
        self.MplWidget.canvas.axes.plot(self.time_array,self.nor_plot,'o',color = "green", label="Threshold") 
        self.MplWidget.canvas.axes.legend(loc='upper center',shadow=True, ncol=4, fontsize=10)
        self.MplWidget.canvas.axes.set_title('Amplification curve', fontsize=7)
        self.MplWidget.canvas.draw()

if __name__ == '__main__':
    app = QApplication([])
    window = MatplotlibWidget()
    window.show()
    app.exec_()