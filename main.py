import sys
from CT_Display_ver1 import *

if __name__ == '__main__':
    app = QApplication(sys.argv)

    mainWindows = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(mainWindows)
    mainWindows.show()
    sys.exit(app.exec_())