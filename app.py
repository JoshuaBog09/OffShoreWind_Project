import sys
from PyQt5 import QtCore,QtGui, QtWidgets
from PyQt5 import uic


class Counter(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("uis/counter.ui", self)

        self.setWindowTitle("Counter")

        self.value = 0

        self.label.setText(f"{self.value}")

        self.pushButton.clicked.connect(self.counter)

    def counter(self):
        self.value += 1
        self.label.setText(f"{self.value}")


app = QtWidgets.QApplication(sys.argv)
window = Counter()
window.show()
app.exec_()