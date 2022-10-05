import sys
from PyQt5 import QtCore,QtGui, QtWidgets
from PyQt5 import uic

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

import numpy as np

# class Counter(QtWidgets.QMainWindow):
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         uic.loadUi("uis/counter.ui", self)
#         self.window = None
#
#         self.pushButton.setStyleSheet("""
#                 QWidget {
#                     border: 5px solid black;
#                     border-radius: 10px;
#                     min-width: 40em;
#                     max-width: 45em;
#                     }
#                 """)
#
#         self.setWindowTitle("Counter")
#
#         self.value = 0
#
#         self.label.setText(f"{self.value}")
#
#         self.pushButton.clicked.connect(self.counter)
#
#     def counter(self):
#         self.value += 1
#         self.label.setText(f"{self.value}")

class Counter(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("uis/plots.ui", self)

        self.pushButton.clicked.connect(self.clear)

        self.fig, self.ax = plt.subplots()
        self.ax.plot([1, 2,3], [1, 20,2])

        self.plotWidget = FigureCanvasQTAgg(self.fig)
        self.lay = QtWidgets.QVBoxLayout(self.widget)
        self.lay.setContentsMargins(0, 0, 0, 0)
        self.lay.addWidget(self.plotWidget)

    def clear(self):
        self.fig, self.ax = plt.subplots()
        self.ax.plot([1, 10], [1, 2])
        self.plotWidget.deleteLater()
        self.plotWidget = FigureCanvasQTAgg(self.fig)
        self.lay.addWidget(self.plotWidget)


app = QtWidgets.QApplication(sys.argv)
window = Counter()
window.show()
app.exec_()