# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\CT_dynamic_2.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from mplwidget import MplWidget


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(933, 760)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.MplWidget = MplWidget(self.centralwidget)
        self.MplWidget.setGeometry(QtCore.QRect(10, 54, 701, 217))
        self.MplWidget.setObjectName("MplWidget")
        self.Input_file = QtWidgets.QLineEdit(self.centralwidget)
        self.Input_file.setGeometry(QtCore.QRect(10, 300, 261, 25))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.Input_file.setFont(font)
        self.Input_file.setObjectName("Input_file")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(540, 342, 161, 157))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 336, 261, 151))
        self.groupBox.setCheckable(True)
        self.groupBox.setObjectName("groupBox")
        self.layoutWidget = QtWidgets.QWidget(self.groupBox)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 18, 241, 130))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.A8_radio = QtWidgets.QRadioButton(self.layoutWidget)
        self.A8_radio.setCheckable(True)
        self.A8_radio.setChecked(False)
        self.A8_radio.setObjectName("A8_radio")
        self.gridLayout_3.addWidget(self.A8_radio, 3, 1, 1, 1)
        self.Clear_radio = QtWidgets.QRadioButton(self.layoutWidget)
        self.Clear_radio.setCheckable(True)
        self.Clear_radio.setChecked(False)
        self.Clear_radio.setObjectName("Clear_radio")
        self.gridLayout_3.addWidget(self.Clear_radio, 4, 1, 1, 1)
        self.A7_radio = QtWidgets.QRadioButton(self.layoutWidget)
        self.A7_radio.setCheckable(True)
        self.A7_radio.setChecked(False)
        self.A7_radio.setObjectName("A7_radio")
        self.gridLayout_3.addWidget(self.A7_radio, 2, 1, 1, 1)
        self.A2_radio = QtWidgets.QRadioButton(self.layoutWidget)
        self.A2_radio.setCheckable(True)
        self.A2_radio.setChecked(False)
        self.A2_radio.setObjectName("A2_radio")
        self.gridLayout_3.addWidget(self.A2_radio, 1, 0, 1, 1)
        self.A5_radio = QtWidgets.QRadioButton(self.layoutWidget)
        self.A5_radio.setCheckable(True)
        self.A5_radio.setChecked(False)
        self.A5_radio.setObjectName("A5_radio")
        self.gridLayout_3.addWidget(self.A5_radio, 0, 1, 1, 1)
        self.A3_radio = QtWidgets.QRadioButton(self.layoutWidget)
        self.A3_radio.setCheckable(True)
        self.A3_radio.setChecked(False)
        self.A3_radio.setObjectName("A3_radio")
        self.gridLayout_3.addWidget(self.A3_radio, 2, 0, 1, 1)
        self.A4_radio = QtWidgets.QRadioButton(self.layoutWidget)
        self.A4_radio.setCheckable(True)
        self.A4_radio.setChecked(False)
        self.A4_radio.setObjectName("A4_radio")
        self.gridLayout_3.addWidget(self.A4_radio, 3, 0, 1, 1)
        self.A6_radio = QtWidgets.QRadioButton(self.layoutWidget)
        self.A6_radio.setCheckable(True)
        self.A6_radio.setChecked(False)
        self.A6_radio.setObjectName("A6_radio")
        self.gridLayout_3.addWidget(self.A6_radio, 1, 1, 1, 1)
        self.All_radio = QtWidgets.QRadioButton(self.layoutWidget)
        self.All_radio.setCheckable(True)
        self.All_radio.setChecked(True)
        self.All_radio.setObjectName("All_radio")
        self.gridLayout_3.addWidget(self.All_radio, 4, 0, 1, 1)
        self.A1_radio = QtWidgets.QRadioButton(self.layoutWidget)
        self.A1_radio.setCheckable(True)
        self.A1_radio.setChecked(False)
        self.A1_radio.setObjectName("A1_radio")
        self.gridLayout_3.addWidget(self.A1_radio, 0, 0, 1, 1)
        self.B1_radio = QtWidgets.QRadioButton(self.layoutWidget)
        self.B1_radio.setCheckable(True)
        self.B1_radio.setChecked(False)
        self.B1_radio.setObjectName("B1_radio")
        self.gridLayout_3.addWidget(self.B1_radio, 0, 2, 1, 1)
        self.B2_radio = QtWidgets.QRadioButton(self.layoutWidget)
        self.B2_radio.setCheckable(True)
        self.B2_radio.setChecked(False)
        self.B2_radio.setObjectName("B2_radio")
        self.gridLayout_3.addWidget(self.B2_radio, 1, 2, 1, 1)
        self.B3_radio = QtWidgets.QRadioButton(self.layoutWidget)
        self.B3_radio.setCheckable(True)
        self.B3_radio.setChecked(False)
        self.B3_radio.setObjectName("B3_radio")
        self.gridLayout_3.addWidget(self.B3_radio, 2, 2, 1, 1)
        self.B4_radio = QtWidgets.QRadioButton(self.layoutWidget)
        self.B4_radio.setCheckable(True)
        self.B4_radio.setChecked(False)
        self.B4_radio.setObjectName("B4_radio")
        self.gridLayout_3.addWidget(self.B4_radio, 3, 2, 1, 1)
        self.B5_radio = QtWidgets.QRadioButton(self.layoutWidget)
        self.B5_radio.setCheckable(True)
        self.B5_radio.setChecked(False)
        self.B5_radio.setObjectName("B5_radio")
        self.gridLayout_3.addWidget(self.B5_radio, 0, 3, 1, 1)
        self.B6_radio = QtWidgets.QRadioButton(self.layoutWidget)
        self.B6_radio.setCheckable(True)
        self.B6_radio.setChecked(False)
        self.B6_radio.setObjectName("B6_radio")
        self.gridLayout_3.addWidget(self.B6_radio, 1, 3, 1, 1)
        self.B7_radio = QtWidgets.QRadioButton(self.layoutWidget)
        self.B7_radio.setCheckable(True)
        self.B7_radio.setChecked(False)
        self.B7_radio.setObjectName("B7_radio")
        self.gridLayout_3.addWidget(self.B7_radio, 2, 3, 1, 1)
        self.B8_radio = QtWidgets.QRadioButton(self.layoutWidget)
        self.B8_radio.setCheckable(True)
        self.B8_radio.setChecked(False)
        self.B8_radio.setObjectName("B8_radio")
        self.gridLayout_3.addWidget(self.B8_radio, 3, 3, 1, 1)
        self.layoutWidget1 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget1.setGeometry(QtCore.QRect(280, 354, 251, 133))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget1)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.slider_threshold = QtWidgets.QSlider(self.layoutWidget1)
        self.slider_threshold.setMinimum(0)
        self.slider_threshold.setMaximum(15)
        self.slider_threshold.setOrientation(QtCore.Qt.Horizontal)
        self.slider_threshold.setObjectName("slider_threshold")
        self.gridLayout.addWidget(self.slider_threshold, 0, 1, 1, 1)
        self.ns_threshold = QtWidgets.QLCDNumber(self.layoutWidget1)
        self.ns_threshold.setObjectName("ns_threshold")
        self.gridLayout.addWidget(self.ns_threshold, 0, 2, 1, 1)
        self.baseline_begin = QtWidgets.QLabel(self.layoutWidget1)
        self.baseline_begin.setAlignment(QtCore.Qt.AlignCenter)
        self.baseline_begin.setObjectName("baseline_begin")
        self.gridLayout.addWidget(self.baseline_begin, 1, 0, 1, 1)
        self.slider_begin = QtWidgets.QSlider(self.layoutWidget1)
        self.slider_begin.setMinimum(0)
        self.slider_begin.setMaximum(15)
        self.slider_begin.setOrientation(QtCore.Qt.Horizontal)
        self.slider_begin.setObjectName("slider_begin")
        self.gridLayout.addWidget(self.slider_begin, 1, 1, 1, 1)
        self.ns_baseline_begin = QtWidgets.QLCDNumber(self.layoutWidget1)
        self.ns_baseline_begin.setObjectName("ns_baseline_begin")
        self.gridLayout.addWidget(self.ns_baseline_begin, 1, 2, 1, 1)
        self.baseline_end = QtWidgets.QLabel(self.layoutWidget1)
        self.baseline_end.setAlignment(QtCore.Qt.AlignCenter)
        self.baseline_end.setObjectName("baseline_end")
        self.gridLayout.addWidget(self.baseline_end, 2, 0, 1, 1)
        self.slider_end = QtWidgets.QSlider(self.layoutWidget1)
        self.slider_end.setMinimum(0)
        self.slider_end.setMaximum(15)
        self.slider_end.setOrientation(QtCore.Qt.Horizontal)
        self.slider_end.setObjectName("slider_end")
        self.gridLayout.addWidget(self.slider_end, 2, 1, 1, 1)
        self.ns_baseline_end = QtWidgets.QLCDNumber(self.layoutWidget1)
        self.ns_baseline_end.setObjectName("ns_baseline_end")
        self.gridLayout.addWidget(self.ns_baseline_end, 2, 2, 1, 1)
        self.layoutWidget2 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget2.setGeometry(QtCore.QRect(280, 294, 295, 37))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.layoutWidget2)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.btn_open = QtWidgets.QPushButton(self.layoutWidget2)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.btn_open.setFont(font)
        self.btn_open.setStyleSheet("color: rgb(0, 0, 255);")
        self.btn_open.setObjectName("btn_open")
        self.gridLayout_4.addWidget(self.btn_open, 0, 0, 1, 1)
        self.btn_save = QtWidgets.QPushButton(self.layoutWidget2)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.btn_save.setFont(font)
        self.btn_save.setStyleSheet("color: rgb(0, 170, 0);")
        self.btn_save.setObjectName("btn_save")
        self.gridLayout_4.addWidget(self.btn_save, 0, 1, 1, 1)
        self.btn_clear = QtWidgets.QPushButton(self.layoutWidget2)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.btn_clear.setFont(font)
        self.btn_clear.setStyleSheet("color: rgb(255, 0, 0);")
        self.btn_clear.setObjectName("btn_clear")
        self.gridLayout_4.addWidget(self.btn_clear, 0, 2, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 933, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "CH"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Value"))
        self.groupBox.setTitle(_translate("MainWindow", "Seleccionar"))
        self.A8_radio.setText(_translate("MainWindow", "A8"))
        self.Clear_radio.setText(_translate("MainWindow", "Clear"))
        self.A7_radio.setText(_translate("MainWindow", "A7"))
        self.A2_radio.setText(_translate("MainWindow", "A2"))
        self.A5_radio.setText(_translate("MainWindow", "A5"))
        self.A3_radio.setText(_translate("MainWindow", "A3"))
        self.A4_radio.setText(_translate("MainWindow", "A4"))
        self.A6_radio.setText(_translate("MainWindow", "A6"))
        self.All_radio.setText(_translate("MainWindow", "All"))
        self.A1_radio.setText(_translate("MainWindow", "A1"))
        self.B1_radio.setText(_translate("MainWindow", "B1"))
        self.B2_radio.setText(_translate("MainWindow", "B2"))
        self.B3_radio.setText(_translate("MainWindow", "B3"))
        self.B4_radio.setText(_translate("MainWindow", "B4"))
        self.B5_radio.setText(_translate("MainWindow", "B5"))
        self.B6_radio.setText(_translate("MainWindow", "B6"))
        self.B7_radio.setText(_translate("MainWindow", "B7"))
        self.B8_radio.setText(_translate("MainWindow", "B8"))
        self.label_3.setText(_translate("MainWindow", "Threshold"))
        self.baseline_begin.setText(_translate("MainWindow", "Baseline Begin:"))
        self.baseline_end.setText(_translate("MainWindow", "Baseline End:"))
        self.btn_open.setText(_translate("MainWindow", "Open"))
        self.btn_save.setText(_translate("MainWindow", "Save"))
        self.btn_clear.setText(_translate("MainWindow", "Clear"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
