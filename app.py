import sys
import webbrowser

import matplotlib.pyplot as plt

from PyQt5 import QtCore,QtGui, QtWidgets
from PyQt5 import uic

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

import logo_rc

from windFarm import windfarm


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("uis/mainscreen.ui", self)

        self.pushButton.clicked.connect(self.submit)
        self.pushButton_2.clicked.connect(self.github)
        self.pushButton_3.clicked.connect(self.end)
        # self.wind_velocity.setText(f"Hello")

        self.plotWidget = FigureCanvasQTAgg(plt.Figure())
        self.lay = QtWidgets.QVBoxLayout(self.plot_area)
        self.lay.setContentsMargins(0, 0, 0, 0)
        self.lay.addWidget(self.plotWidget)

    def submit(self):
        v_ref = float(self.v_ref.text())
        hub_height = float(self.hub_height.text())
        diameter = float(self.diameter.text())
        turbine_placement = str(self.turbine_placement.text())
        turbine_placement_list = turbine_placement.split(", ")
        turbine_placement_list = [float(ele) for ele in turbine_placement_list]
        h_ref = float(self.h_ref.text())
        c_f = float(self.C_f.text())
        # print(h_ref)
        # print(v_ref)
        # print(hub_height)
        # print(diameter)
        # print(turbine_placement_list)
        # h_blend = float(self.h_blend.text())

        windfarm_var = windfarm(diameter, hub_height, v_ref, h_ref, turbine_placement_list, c_f)

        self.farm_power.setText(str(round(windfarm_var[0]/10**6, 3)))
        self.farm_eff.setText(str(round(windfarm_var[1], 3)))
        self.power_first_turbine.setText(str(round(windfarm_var[2]/10**6, 3)))
        self.energy_yield_yr.setText(str(round(windfarm_var[3]/10**6, 3)))

        self.fig, self.ax = plt.subplots()
        self.ax.plot(windfarm_var[4], windfarm_var[5])
        self.plotWidget.deleteLater()
        self.plotWidget = FigureCanvasQTAgg(self.fig)
        self.lay.addWidget(self.plotWidget)

    def end(self):
        sys.exit()

    def github(self):
        webbrowser.open('https://github.com/JoshuaBog09/OffShoreWind_Project')


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
