import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtChart import QChartView
from PyQt5 import QtCore, QtGui, QtWidgets
from bleach import clean
from matplotlib.pyplot import cla 
from CT_Manager import Ui_MainWindow


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, app):
        super(QMainWindow, self).__init__()
        self.app = app
        self.setup_ui()  # 渲染画布
        self.connect_signals()  # 绑定触发事件
    
    def setup_ui(self):
        self.setupUi(self)
        
    def connect_signals(self):
        self.btn_clean.clicked.connect(self.btn_clean_clicked)
       
    def btn_clean_clicked(self):
        print("test")


def main():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = Window(app)
    MainWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()


# if __name__ == "__main__":
#     app = QtWidgets.QApplication(sys.argv)
#     MainWindow = QtWidgets.QMainWindow()
#     ui = Ui_MainWindow()
#     ui.setupUi(MainWindow)
#     MainWindow.show()
#     sys.exit(app.exec_())
