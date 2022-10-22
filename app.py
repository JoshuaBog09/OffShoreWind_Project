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

        self.setWindowTitle("Wake effect simulator")

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
            try:
                v_ref = float(self.v_ref.text())
                hub_height = float(self.hub_height.text())
                diameter = float(self.diameter.text())
                turbine_placement = str(self.turbine_placement.text())
                turbine_placement_list = turbine_placement.split(", ")
                turbine_placement_list = [float(ele) for ele in turbine_placement_list]
                h_ref = float(self.h_ref.text())
                c_f = float(self.C_f.text())

                windfarm_var = windfarm(diameter, hub_height, v_ref, h_ref, turbine_placement_list, c_f)
                if windfarm_var[-1]:
                    self.farm_power.setText(str(round(windfarm_var[0]/10**6, 3)))
                    self.farm_eff.setText(str(round(windfarm_var[1], 3)))
                    self.power_first_turbine.setText(str(round(windfarm_var[2]/10**6, 3)))
                    self.energy_yield_yr.setText(str(round(windfarm_var[3]/10**6, 3)))

                    turbine_placement_list.insert(0, 0)

                    self.fig, self.ax = plt.subplots()
                    self.ax.plot(windfarm_var[4], windfarm_var[5])
                    ymin, ymax = self.ax.get_ylim()
                    self.ax.vlines(x=turbine_placement_list[:], ymin=ymin, ymax=ymax, colors='teal', ls='--', lw=1)
                    for i, x in enumerate(turbine_placement_list, start=1):
                        plt.text(x, ymin+ymin/10, f"Turbine {i}", rotation=90, verticalalignment='center')
                    self.ax.set_ylabel("Wake velocity in m/s")
                    self.ax.set_xlabel("Location in m")
                    self.plotWidget.deleteLater()
                    self.plotWidget = FigureCanvasQTAgg(self.fig)
                    self.lay.addWidget(self.plotWidget)

                    # Storing data for the history
                    self.local_history.append(
                        {
                            "V_ref[m/s]"                : v_ref,
                            "H_ref[m]"                  : h_ref,
                            "Cf[-]"                     : c_f,
                            "Hub_height[m]"             : hub_height,
                            "Diameter[m]"               : diameter,
                            "Turbine_placement[m]"      : turbine_placement_list,
                            "Farm_power[W](Out)"        : windfarm_var[0],
                            "Farm_efficiency[-](Out)"   : windfarm_var[1],
                            "Power_first[W](Out)"       : windfarm_var[2],
                            "Energy_yield[Wh](Out)"     : windfarm_var[3],
                        }
                    )

                elif not windfarm_var[-1]:
                    self.error_field.setText(windfarm_var[0])
            except:
                self.error_field.setText(f"An incorrect character was identified, in the input fields")
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

        QBtn = QtWidgets.QDialogButtonBox.Ok

        self.buttonBox = QtWidgets.QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)

        self.layout = QtWidgets.QVBoxLayout()
        message = QtWidgets.QTextBrowser()

        # Display history items
        for idx, item in enumerate(local_history, start=1):
            message.append(f"Run{idx}: {item}")

        # Placing and window size
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
        self.resize(1600,300)


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
