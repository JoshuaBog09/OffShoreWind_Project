import sys
import webbrowser

import matplotlib.pyplot as plt

from PyQt5 import QtCore,QtGui, QtWidgets
from PyQt5 import uic

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

import logo_rc


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("uis/mainscreen.ui", self)

        self.pushButton.clicked.connect(self.submit)
        self.pushButton_2.clicked.connect(self.github)
        self.pushButton_3.clicked.connect(self.end)
        # self.wind_velocity.setText(f"Hello")

        self.plotWidget = FigureCanvasQTAgg(plt.Figure())
        self.lay = QtWidgets.QVBoxLayout(self.widget)
        self.lay.setContentsMargins(0, 0, 0, 0)
        self.lay.addWidget(self.plotWidget)

    def submit(self):
        wind_velocity_0m = float(self.wind_velocity.text())
        print(wind_velocity_0m)
        hub_height = float(self.hub_height.text())
        print(hub_height)
        diameter = float(self.diameter.text())
        print(diameter)
        turbine_cost = float(self.turbine_cost.text())
        print(turbine_cost)
        turbine_placement = str(self.turbine_placement.text())
        turbine_placement_list = turbine_placement.split(", ")
        print(turbine_placement_list)

    def end(self):
        sys.exit()

    def github(self):
        webbrowser.open('https://github.com/JoshuaBog09/OffShoreWind_Project')


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
