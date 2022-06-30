from PyQt5.QtWidgets import*
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
import os
import pandas as pd
import numpy as np
from datetime import datetime
first_time = 2
twice_time = 7
n_sd = 10
now_output_time = str(datetime.now().strftime('%Y-%m-%d %H-%M-%S'))
#Color
colorTab_More4 = ['#e8a5eb', '#facc9e', '#e8e948', '#1bb763',
                  '#25f2f3', '#1db3ea', '#d1aef8', '#c8c92c',
                  '#f32020', '#fd9b09', '#406386', '#24a1a1',
                  '#1515f8', '#959697', '#744a20', '#7b45a5']
class MatplotlibWidget(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        loadUi("CT_Manager.ui",self)
        self.setWindowTitle("CT_Value")
        self.addToolBar(NavigationToolbar(self.MplWidget.canvas, self))
        self.connect_signals()
    def connect_signals(self):
        self.btn_open.clicked.connect(self.browsefile)
        self.btn_save.clicked.connect(self.save_file)
        self.btn_clear.clicked.connect(self.clean_log)
        self.slider_begin.valueChanged.connect(self.sl_begin)

    def browsefile(self):
        if not os.path.isdir('./result'):
            os.mkdir('./result')
            os.mkdir('./result/Cali_result/')
            os.mkdir('./result/Display_result/')
        self.fname = QFileDialog.getOpenFileName(self, '開啟csv檔案', 'C:\Program Files (x86)', 'csv files (*.csv)')
        if(self.fname[0]==""):
            print("no file")
        else:
            self.update_graph()
    def calculate(self):
        self.big_well = []
        self.big_data = []
        self.Input_file.setText(self.fname[0])
        self.df_raw = pd.read_csv(self.fname[0])
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
            StdDev.append(df_current_well[int(first_time) * 2:int(twice_time) * 2].std())
            Avg.append(df_current_well[int(first_time) * 2:int(twice_time) * 2].mean())
        return StdDev, Avg

    def normalize(self):
        for i in range(0, 16):
            df_current_well = self.df_raw[f'well_{i + 1}']
            self.baseline = df_current_well[int(first_time) * 2:int(twice_time) * 2].mean()
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
            threshold_value.append(int(n_sd) * StdDev[i] + Avg[i])
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
    
    def save_file(self):
        #儲存失敗
        if self.Input_file.text() == "":
            QtWidgets.QMessageBox.critical(self, u"存取失敗", u"未開啟csv檔案", buttons=QtWidgets.QMessageBox.Ok,
                defaultButton=QtWidgets.QMessageBox.Ok)
        #儲存成功
        else:
            try :
                if len(self.df_raw.index) < 7:
                    raise
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
                #儲存資料以及存取位置
                self.save_excel.to_csv('./result/Display_result/CT_Value' + now_output_time + "all_well.csv", encoding="utf_8_sig")
                self.df_normalization = self.df_normalization.drop(columns=['time','accumulation','shutter_speed','ISO']) #Drop 'time','accumulation','shutter_speed','ISO'
                self.df_normalization.T.to_csv('./result/Display_result/CT_Value_'+ now_output_time + '_MA_data.csv', encoding="utf_8_sig")
                QtWidgets.QMessageBox.information(self, u"存取成功", u"已成功另存Csv檔案", buttons=QtWidgets.QMessageBox.Ok,
                    defaultButton=QtWidgets.QMessageBox.Ok)
                print("Save data successful !!!")

    def clean_log(self):
        self.Input_file.setText("")
        print("Clean data successful !!!")


    def sl_begin(self):
        if self.All_radio.isChecked():
            print("yes")
    def update_graph(self):
        self.calculate()

        self.MplWidget.canvas.axes.clear()
        self.MplWidget.canvas.axes.plot(self.time_array, self.A1_data)
        self.MplWidget.canvas.axes.plot(self.time_array, self.A2_data)
        self.MplWidget.canvas.axes.plot(self.time_array, self.A3_data)
        self.MplWidget.canvas.axes.plot(self.time_array, self.A4_data)
        self.MplWidget.canvas.axes.plot(self.time_array, self.A5_data)
        self.MplWidget.canvas.axes.plot(self.time_array, self.A6_data)
        self.MplWidget.canvas.axes.plot(self.time_array, self.A7_data)
        self.MplWidget.canvas.axes.plot(self.time_array, self.A8_data)
        self.MplWidget.canvas.axes.plot(self.time_array, self.B1_data)
        self.MplWidget.canvas.axes.plot(self.time_array, self.B2_data)
        self.MplWidget.canvas.axes.plot(self.time_array, self.B3_data)
        self.MplWidget.canvas.axes.plot(self.time_array, self.B4_data)
        self.MplWidget.canvas.axes.plot(self.time_array, self.B5_data)
        self.MplWidget.canvas.axes.plot(self.time_array, self.B6_data)
        self.MplWidget.canvas.axes.plot(self.time_array, self.B7_data)
        self.MplWidget.canvas.axes.plot(self.time_array, self.B8_data)
        self.MplWidget.canvas.axes.set_xlim(0,20)
        # self.MplWidget.canvas.axes.set_ylim(-0.1,0.1)
        #self.MplWidget.canvas.set_scales(20,0.1)
        self.MplWidget.canvas.axes.legend(('cosinus', 'sinus','cosinus', 'sinus','cosinus', 'sinus'),loc='upper right')
        self.MplWidget.canvas.axes.set_title('Amplification curve')
        self.MplWidget.canvas.draw()

if __name__ == '__main__':
    app = QApplication([])
    window = MatplotlibWidget()
    window.show()
    app.exec_()