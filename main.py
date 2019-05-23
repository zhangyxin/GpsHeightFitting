import sys

from PyQt5.QtWidgets import QApplication

from Gui.mainWindow import Gps

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Gps()
    w.show()
    sys.exit(app.exec_())
