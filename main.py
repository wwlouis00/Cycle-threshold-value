from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
import pandas as pd
import numpy as np
from datetime import datetime
import os, sys
import traceback
import pyperclip  # 需要 pip install pyperclip

# ----- 常數 -----
FIRST_TIME, TWICE_TIME, N_SD = 2, 7, 10
NOW_OUTPUT_TIME = str(datetime.now().strftime('%Y-%m-%d %H-%M-%S'))
COLOR_TAB = [
    '#e8a5eb', '#facc9e', '#e8e948', '#1bb763',
    '#25f2f3', '#1db3ea', '#d1aef8', '#c8c92c',
    '#f32020', '#fd9b09', '#406386', '#24a1a1',
    '#1515f8', '#959697', '#744a20', '#7b45a5'
]

class MatplotlibWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CT Value Analyzer")
        self.resize(1300, 750)
        self.df_raw = None
        self.df_normalization = None
        self.Ct_value = []
        self.time_array = []
        self.big_array = []
        self.last_error_log = ""  # 儲存最後一次錯誤訊息
        self._setup_ui()
        self._connect_signals()

    # ===== UI 設計 =====
    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QHBoxLayout(central)
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)

        # ---- 左邊控制面板 ----
        control_panel = QWidget()
        control_layout = QVBoxLayout(control_panel)

        # 檔案操作區
        file_group = QGroupBox("檔案操作")
        file_layout = QVBoxLayout(file_group)
        self.btn_open = QPushButton("📂 開啟 CSV")
        self.btn_save = QPushButton("💾 儲存結果")
        self.Input_file = QLineEdit()
        self.Input_file.setPlaceholderText("尚未選擇檔案")
        self.Input_file.setReadOnly(True)
        file_layout.addWidget(self.Input_file)
        file_layout.addWidget(self.btn_open)
        file_layout.addWidget(self.btn_save)

        # 複製錯誤 log 按鈕
        self.btn_copy_log = QPushButton("📋 複製錯誤 Log")
        self.btn_copy_log.setToolTip("將最後一次錯誤訊息複製到剪貼簿")
        file_layout.addWidget(self.btn_copy_log)

        # 曲線選擇區
        curve_group = QGroupBox("曲線選擇")
        curve_layout = QGridLayout(curve_group)
        self.All_radio = QRadioButton("全部曲線")
        self.Clear_radio = QRadioButton("清除")
        self.nor_radio = QRadioButton("Normalize")
        self.main_radio = QRadioButton("主要曲線")
        radios = []
        for ch in ["A1","A2","A3","A4","A5","A6","A7","A8",
                   "B1","B2","B3","B4","B5","B6","B7","B8"]:
            radios.append(QRadioButton(ch))
        self.radios = radios

        curve_layout.addWidget(self.All_radio,0,0,1,2)
        curve_layout.addWidget(self.Clear_radio,0,2,1,2)
        curve_layout.addWidget(self.nor_radio,1,0,1,2)
        curve_layout.addWidget(self.main_radio,1,2,1,2)
        for i, r in enumerate(radios):
            row, col = divmod(i,4)
            curve_layout.addWidget(r, row+2, col)

        control_layout.addWidget(file_group)
        control_layout.addWidget(curve_group)
        control_layout.addStretch()

        splitter.addWidget(control_panel)

        # ---- 右邊圖表 + 表格 ----
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)

        from matplotlib.figure import Figure
        from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
        self.fig = Figure()
        self.canvas = FigureCanvasQTAgg(self.fig)
        self.ax = self.fig.add_subplot(111)

        toolbar = NavigationToolbar(self.canvas, self)
        right_layout.addWidget(toolbar)
        right_layout.addWidget(self.canvas, 5)

        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(["Well", "CT Value"])
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        right_layout.addWidget(self.tableWidget, 2)

        splitter.addWidget(right_panel)
        splitter.setSizes([250, 950])

        self.setStyleSheet("""
            QMainWindow { background-color: #f7f9fc; }
            QGroupBox { font-weight: bold; border: 1px solid gray; border-radius: 6px; margin-top: 8px; }
            QPushButton { padding: 6px; border-radius: 6px; background-color: #0078d7; color: white; }
            QPushButton:hover { background-color: #005a9e; }
            QLineEdit { padding: 4px; background: #fff; border: 1px solid #aaa; }
            QRadioButton { font-size: 11pt; }
            QTableWidget { background: white; border: 1px solid #ccc; gridline-color: #ddd; }
        """)
        self.setFont(QFont("Segoe UI", 10))

    def _connect_signals(self):
        self.btn_open.clicked.connect(self.browsefile)
        self.btn_save.clicked.connect(self.save_file)
        self.btn_copy_log.clicked.connect(self.copy_log_to_clipboard)
        self.All_radio.clicked.connect(self.update_graph)
        self.Clear_radio.clicked.connect(self.update_graph)
        self.nor_radio.clicked.connect(self.update_graph)
        self.main_radio.clicked.connect(self.update_graph)
        for r in self.radios:
            r.clicked.connect(self.update_graph)

    # ===== 功能區 =====
    def browsefile(self):
        try:
            fname, _ = QFileDialog.getOpenFileName(self, "開啟 CSV 檔案", "", "CSV files (*.csv)")
            if not fname:
                return
            self.Input_file.setText(fname)
            self.df_raw = pd.read_csv(fname)
            self.calculate()
        except Exception as e:
            self.last_error_log = f"讀取檔案錯誤：\n{str(e)}\n{traceback.format_exc()}"
            QMessageBox.critical(self, "錯誤", self.last_error_log)

    def calculate(self):
        try:
            self.df_raw.reset_index(inplace=True)
            self.df_raw.rename(columns={'time':'well_1', 'A1':'well_2', 'A2':'well_3', 'A3':'well_4',
                                        'A4':'well_5', 'A5':'well_6', 'A6':'well_7', 'A7':'well_8',
                                        'A8':'well_9', 'B1':'well_10', 'B2':'well_11', 'B3':'well_12',
                                        'B4':'well_13', 'B5':'well_14', 'B6':'well_15', 'B7':'well_16'},
                               inplace=True)
            if "B8" in self.df_raw.columns:
                self.df_raw = self.df_raw.drop(labels=["B8"], axis="columns")
            self.df_raw.rename(columns={"index": "time"}, inplace=True)

            self.df_normalization = self.df_raw.copy()
            self.get_accumulation_time()
            self.normalize()
            threshold_value = self.get_ct_threshold()
            self.Ct_value = self.get_ct_value(threshold_value)

            self.big_array.clear()
            self.time_array = np.arange(len(self.df_normalization)) / 2.0
            for i in range(1, 17):
                self.big_array.append(self.df_normalization[f'well{i}'])

            self.update_graph()
            self.update_table()
        except Exception as e:
            self.last_error_log = f"計算過程錯誤：\n{str(e)}\n{traceback.format_exc()}"
            QMessageBox.critical(self, "錯誤", self.last_error_log)

    def get_accumulation_time(self):
        try:
            df_time = self.df_normalization['time']
            try:
                time_ori = datetime.strptime(str(df_time.iloc[0]), "%H:%M:%S")
            except ValueError:
                time_ori = datetime.strptime(str(df_time.iloc[0]), "%H%M%S")
            time_delta = []
            for t in df_time:
                try:
                    t_now = datetime.strptime(str(t), "%H:%M:%S")
                except ValueError:
                    t_now = datetime.strptime(str(t), "%H%M%S")
                time_delta.append((t_now - time_ori).seconds / 60)
            self.df_normalization.insert(1, column="accumulation", value=time_delta)
        except Exception as e:
            self.last_error_log = f"時間解析錯誤：\n{str(e)}\n{traceback.format_exc()}"
            QMessageBox.critical(self, "錯誤", self.last_error_log)
            raise

    def normalize(self):
        try:
            for i in range(0, 16):
                df_current_well = self.df_raw[f'well_{i + 1}']
                baseline = df_current_well[FIRST_TIME*2+1:TWICE_TIME*2+1].mean()
                self.df_normalization[f'well{i + 1}'] = (df_current_well - baseline) / baseline
        except Exception as e:
            self.last_error_log = f"資料正規化錯誤：\n{str(e)}\n{traceback.format_exc()}"
            QMessageBox.critical(self, "錯誤", self.last_error_log)

    def get_ct_threshold(self):
        try:
            StdDev, Avg = [], []
            for i in range(0, 16):
                df_current_well = self.df_normalization[f'well_{i + 1}']
                StdDev.append(df_current_well[FIRST_TIME*2+1:TWICE_TIME*2+1].std())
                Avg.append(df_current_well[FIRST_TIME*2+1:TWICE_TIME*2+1].mean())
            return [N_SD*StdDev[i] + Avg[i] for i in range(16)]
        except Exception as e:
            self.last_error_log = f"計算閾值錯誤：\n{str(e)}\n{traceback.format_exc()}"
            QMessageBox.critical(self, "錯誤", self.last_error_log)
            return [0]*16

    def get_ct_value(self, threshold_value):
        Ct_value = []
        try:
            for i in range(0, 16):
                df_current_well = self.df_normalization[f'well_{i + 1}']
                df_accumulation = self.df_normalization['accumulation']
                found = False
                for j, row in enumerate(df_current_well):
                    if row >= threshold_value[i]:
                        if j == 0:
                            Ct_value.append("N/A")
                        else:
                            thres_lower = df_current_well.iloc[j - 1]
                            thres_upper = df_current_well[j]
                            acc_time_lower = df_accumulation[j - 1]
                            acc_time_upper = df_accumulation[j]
                            x = (acc_time_upper - acc_time_lower) * \
                                (threshold_value[i] - thres_lower) / (thres_upper - thres_lower) + acc_time_lower
                            Ct_value.append(round(x, 2))
                        found = True
                        break
                if not found:
                    Ct_value.append("N/A")
        except Exception as e:
            self.last_error_log = f"計算CT值錯誤：\n{str(e)}\n{traceback.format_exc()}"
            QMessageBox.critical(self, "錯誤", self.last_error_log)
        return Ct_value

    def update_graph(self):
        try:
            self.ax.clear()
            if self.df_normalization is None:
                self.canvas.draw()
                return

            if self.All_radio.isChecked():
                for i in range(16):
                    self.ax.plot(self.time_array, self.big_array[i], label=f"Well {i+1}", color=COLOR_TAB[i])
            elif self.nor_radio.isChecked():
                mean_line = np.mean([arr.mean() for arr in self.big_array])
                self.ax.plot(self.time_array, [mean_line]*len(self.time_array), 'g--', label="Normalize")
            elif self.Clear_radio.isChecked():
                self.canvas.draw()
                return
            else:
                for i, r in enumerate(self.radios):
                    if r.isChecked():
                        self.ax.plot(self.time_array, self.big_array[i], label=r.text(), color=COLOR_TAB[i])

            self.ax.set_title("Amplification Curve")
            self.ax.set_xlabel("Time (min)")
            self.ax.set_ylabel("Normalized Fluorescent Intensity")
            self.ax.legend(fontsize=8, loc="upper right", ncol=2)
            self.canvas.draw()
        except Exception as e:
            self.last_error_log = f"更新圖表錯誤：\n{str(e)}\n{traceback.format_exc()}"
            QMessageBox.critical(self, "錯誤", self.last_error_log)

    def update_table(self):
        try:
            self.tableWidget.setRowCount(0)
            for i, ct in enumerate(self.Ct_value):
                self.tableWidget.insertRow(i)
                self.tableWidget.setItem(i,0,QTableWidgetItem(f"Well {i+1}"))
                self.tableWidget.setItem(i,1,QTableWidgetItem(str(ct)))
        except Exception as e:
            self.last_error_log = f"更新表格錯誤：\n{str(e)}\n{traceback.format_exc()}"
            QMessageBox.critical(self, "錯誤", self.last_error_log)

    def save_file(self):
        try:
            if self.df_raw is None:
                QMessageBox.critical(self,"錯誤","尚未載入資料")
                return
            if not os.path.isdir("./result"):
                os.mkdir("./result")
            outname = f"./result/CT_Value_{NOW_OUTPUT_TIME}.csv"
            pd.DataFrame({
                "Well":[f"Well{i+1}" for i in range(16)],
                "CT Value":self.Ct_value
            }).to_csv(outname,index=False)
            QMessageBox.information(self,"成功",f"已儲存至 {outname}")
        except Exception as e:
            self.last_error_log = f"儲存檔案錯誤：\n{str(e)}\n{traceback.format_exc()}"
            QMessageBox.critical(self, "錯誤", self.last_error_log)

    def copy_log_to_clipboard(self):
        if self.last_error_log:
            pyperclip.copy(self.last_error_log)
            QMessageBox.information(self, "成功", "錯誤訊息已複製到剪貼簿")
        else:
            QMessageBox.information(self, "訊息", "目前沒有錯誤訊息")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MatplotlibWidget()
    w.show()
    sys.exit(app.exec_())
