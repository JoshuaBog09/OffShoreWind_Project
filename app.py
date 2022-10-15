import sys
import webbrowser

import matplotlib.pyplot as plt

from PyQt5 import QtCore,QtGui, QtWidgets
from PyQt5 import uic

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

import logo_rc

import main
import windFarm


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("uis/mainscreen v5.ui", self)

        self.pushButton.clicked.connect(self.submit)
        self.pushButton_2.clicked.connect(self.github)
        self.pushButton_3.clicked.connect(self.end)
        # self.wind_velocity.setText(f"Hello")

        self.plotWidget = FigureCanvasQTAgg(plt.Figure())
        self.lay = QtWidgets.QVBoxLayout(self.widget)
        self.lay.setContentsMargins(0, 0, 0, 0)
        self.lay.addWidget(self.plotWidget)

    def submit(self):
        print("kikker")
        v_ref = float(self.v_ref.text())
        print(v_ref)
        hub_height = float(self.hub_height.text())
        diameter = float(self.diameter.text())
        turbine_placement = str(self.turbine_placement.text())
        turbine_placement_list = turbine_placement.split(", ")
        h_ref = float(self.h_ref.text())
        print(h_ref)
        # h_blend = float(self.h_blend.text())

        windfarm = windFarm.windfarm(diameter, hub_height, v_ref, h_ref, turbine_placement_list)
        print(windfarm)
        # print(windfarm[0] + " [m/s], " + windfarm[1] + " [-], " + " [W]")
        return

    def end(self):
        sys.exit()

    def github(self):
        webbrowser.open('https://github.com/JoshuaBog09/OffShoreWind_Project')


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
