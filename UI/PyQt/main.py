# ------------------------------------------------------
# ---------------------- main.py -----------------------
# ------------------------------------------------------
from PyQt5.QtWidgets import*
from PyQt5.uic import loadUi

from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
import pandas as pd
import numpy as np
import random
from datetime import datetime
first_time = 2
twice_time = 7
n_sd = 10
# 讀取該資料
raw_file_path = "./data/2022_04_11_13_11_08.csv"
# now_output_time = str(datetime.now().strftime('%Y-%m-%d %H-%M-%S'))
# 顏色
colorTab_More4 = ['#e8a5eb', '#facc9e', '#e8e948', '#1bb763',
                  '#25f2f3', '#1db3ea', '#d1aef8', '#c8c92c',
                  '#f32020', '#fd9b09', '#406386', '#24a1a1',
                  '#1515f8', '#959697', '#744a20', '#7b45a5']

class MatplotlibWidget(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        loadUi("qt_designer.ui",self)

        self.setWindowTitle("PyQt5 & Matplotlib Example GUI")

        self.pushButton_generate_random_signal.clicked.connect(self.update_graph)

        self.addToolBar(NavigationToolbar(self.MplWidget.canvas, self))

    
    def calculate(self):
        self.big_well = []
        self.big_data = []
        self.df_raw = pd.read_csv(raw_file_path)
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
            # fancybox=True, shadow=True, ncol=8, fontsize=7.5)
        # plt.savefig('./result/Display_result/CT.jpg')
        # self.displayphoto()

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
            StdDev.append(df_current_well[2 * 2:7 * 2].std())
            Avg.append(df_current_well[2* 2:7 * 2].mean())
        return StdDev, Avg

    def normalize(self):
        for i in range(0, 16):
            df_current_well = self.df_raw[f'well_{i + 1}']
            self.baseline = df_current_well[2* 2:7 * 2].mean()
            self.df_normalization[f'well{i + 1}'] = (self.df_raw[f'well_{i + 1}'] - self.baseline) / self.baseline
            if(i<8):
                print(f'A{i+1}'+" baseline value: " + str(self.baseline))
            else:
                print(f'B{i-7}'+" baseline value: " + str(self.baseline))
        print("*"*100)

    def get_ct_threshold(self):
        threshold_value = []
        StdDev, Avg = self.get_StdDev_and_Avg()
        for i in range(0, 16):
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
        
    
    def update_graph(self):
        self.calculate()
        fs = 500
        f = random.randint(1, 100)
        ts = 1/fs
        length_of_signal = 100
        t = np.linspace(0,1,length_of_signal)
        
        cosinus_signal = np.cos(2*np.pi*f*t)
        sinus_signal = np.sin(2*np.pi*f*t)

        self.MplWidget.canvas.axes.clear()
        self.MplWidget.canvas.axes.plot(self.time_array, self.A1_data)
        self.MplWidget.canvas.axes.plot(self.time_array, self.A2_data)
        self.MplWidget.canvas.axes.set_xlim(0,20)
        self.MplWidget.canvas.axes.set_ylim(-0.1,0.1)
        #self.MplWidget.canvas.set_scales(20,0.1)
        # self.MplWidget.canvas.axes.legend(('cosinus', 'sinus'),loc='upper right')
        self.MplWidget.canvas.axes.set_title('Cosinus - Sinus Signal')
        self.MplWidget.canvas.draw()
        

app = QApplication([])
window = MatplotlibWidget()
window.show()
app.exec_()