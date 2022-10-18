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
        self.open_github.clicked.connect(self.github)
        self.quit_app.clicked.connect(self.end)
        self.open_history.clicked.connect(self.history)
        # self.wind_velocity.setText(f"Hello")

        self.local_history = []

        self.plotWidget = FigureCanvasQTAgg(plt.Figure())
        self.lay = QtWidgets.QVBoxLayout(self.plot_area)
        self.lay.setContentsMargins(0, 0, 0, 0)
        self.lay.addWidget(self.plotWidget)

    def submit(self):

        self.error_field.setText("")

        if self.v_ref.text() and self.hub_height.text() and self.diameter.text() and self.turbine_placement.text() and self.h_ref.text() and self.C_f.text():

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
            if windfarm_var[-1]:
                self.farm_power.setText(str(round(windfarm_var[0]/10**6, 3)))
                self.farm_eff.setText(str(round(windfarm_var[1], 3)))
                self.power_first_turbine.setText(str(round(windfarm_var[2]/10**6, 3)))
                self.energy_yield_yr.setText(str(round(windfarm_var[3]/10**6, 3)))

                self.fig, self.ax = plt.subplots()
                self.ax.plot(windfarm_var[4], windfarm_var[5])
                self.ax.set_ylabel("Wake velocity in m/s")
                self.ax.set_xlabel("Location in m")
                self.plotWidget.deleteLater()
                self.plotWidget = FigureCanvasQTAgg(self.fig)
                self.lay.addWidget(self.plotWidget)

                # Storing data for the history
                self.local_history.append(
                    {
                        "V_ref"             : v_ref,
                        "H_ref"             : h_ref,
                        "Cf"                : c_f,
                        "Hub_height"        : hub_height,
                        "Diameter"          : diameter,
                        "Turbine_placement" : turbine_placement_list,
                        "Farm_power"        : windfarm_var[0],
                        "Farm_efficiency"   : windfarm_var[1],
                        "Power_first"       : windfarm_var[2],
                        "Energy_yield"      : windfarm_var[3],
                    }
                )

            elif not windfarm_var[-1]:
                self.error_field.setText(windfarm_var[0])
        else:
            self.error_field.setText(f"Please fill in all the values in the input boxes on the left to proceed")

    def history(self):
        """
        call history window
        """
        dlg = HistoryDialog(self.local_history)
        dlg.exec()

    def end(self):
        """
        Close program
        """
        sys.exit()

    def github(self):
        """
        Open GitHub
        """
        webbrowser.open('https://github.com/JoshuaBog09/OffShoreWind_Project')

class HistoryDialog(QtWidgets.QDialog):
    """
    Custom dialog window class
    """
    def __init__(self, local_history):
        """
        :param local_history: Local history of the app, all the successful runs are stored here
        """
        super().__init__()

        self.setWindowTitle("Runtime History")

        self.layout = QtWidgets.QVBoxLayout()
        message = QtWidgets.QTextBrowser()

        # Display history items
        for idx, item in enumerate(local_history):
            message.append(f"Run{idx}: {item}")

        # Placing and window size
        self.layout.addWidget(message)
        self.setLayout(self.layout)
        self.resize(1600,300)


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
