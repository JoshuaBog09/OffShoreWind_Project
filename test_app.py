import sys
import webbrowser

from PyQt5 import QtCore,QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import uic


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("uis/Test v2.ui", self)

        self.pushButton.clicked.connect(self.hi)

        self.pushButton.clicked.connect(self.on_click)


    def hi(self):
        print("je mama moeder")

    def on_click(self):
        # textboxValue = self.kikker.text()
        # print(textboxValue)
        name = self.kikker.text()
        print(name)
        # print("aaaa")
        # self.kikker.setText("")


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
