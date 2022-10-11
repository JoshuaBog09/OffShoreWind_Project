import sys
import webbrowser

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

# class Counter(QtWidgets.QMainWindow):
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         uic.loadUi("uis/plots.ui", self)
#
#         self.pushButton.clicked.connect(self.clear)
#
#         self.fig, self.ax = plt.subplots()
#         self.ax.plot([1, 2,3], [1, 20,2])
#
#         self.plotWidget = FigureCanvasQTAgg(self.fig)
#         self.lay = QtWidgets.QVBoxLayout(self.widget)
#         self.lay.setContentsMargins(0, 0, 0, 0)
#         self.lay.addWidget(self.plotWidget)
#
#     def clear(self):
#         self.fig, self.ax = plt.subplots()
#         self.ax.plot([1, 10], [1, 2])
#         self.plotWidget.deleteLater()
#         self.plotWidget = FigureCanvasQTAgg(self.fig)
#         self.lay.addWidget(self.plotWidget)
#
#
# app = QtWidgets.QApplication(sys.argv)
# window = Counter()
# window.show()
# app.exec_()


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("uis/mainscreen.ui", self)

        self.pushButton.clicked.connect(self.submit)
        self.pushButton_2.clicked.connect(self.github)
        self.pushButton_3.clicked.connect(self.end)

    def submit(self):
        wind_velocity_0m = float(self.wind_velocity.text())
        print(wind_velocity_0m)
        hub_height = float(self.hub_height.text())
        print(hub_height)
        diameter = float(self.diameter.text())
        print(diameter)
        turbine_cost = float(self.turbine_cost.text())
        print(turbine_cost)
        turbine_placement = list(self.turbine_placement.text())
        print(turbine_placement)

    def end(self):
        sys.exit()

    def github(self):
        webbrowser.open('https://github.com/JoshuaBog09/OffShoreWind_Project')


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
