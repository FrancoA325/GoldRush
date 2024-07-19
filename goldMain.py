from PyQt5 import QtWidgets
import numpy as np
from goldRush import Ui_MainWindow  # Import the auto-generated UI class

class MyMainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.Front_roll_button.clicked.connect(self.Front_roll_calculate)
        self.Rear_roll_button.clicked.connect(self.Rear_roll_calculate)
        self.Roll_stiff_dist.clicked.connect(self.Roll_stiff_dist_calculate)

        self.Static_vehicle_mass_button.clicked.connect(self.Static_vehicle_mass_calculate)

    def setInputErrorStyle(self, input_field):
        input_field.setStyleSheet("border: 1px solid red;")

    def resetInputStyles(self):
        # Reset the style for all input fields to clear any error state
        self.front_spring_rate_input.setStyleSheet("")
        # Repeat for other input fields as necessary  

    def Front_roll_calculate(self):
        self.resetInputStyles()
        error = False  # Initialize error flag

        # Check each input field and set the error flag without returning
        if not self.front_spring_rate_input.text().strip():
            self.setInputErrorStyle(self.front_spring_rate_input)
            error = True
        if not self.front_motion_ratio_input.text().strip():
            self.setInputErrorStyle(self.front_motion_ratio_input)
            error = True
        if not self.front_trackwidth_input.text().strip():
            self.setInputErrorStyle(self.front_trackwidth_input)
            error = True
        if not self.front_target_roll_stiffness_input.text().strip():
            self.setInputErrorStyle(self.front_target_roll_stiffness_input)
            error = True

        # If any input was missing, return early (optionally show a message)
        if error:
            QtWidgets.QMessageBox.warning(self, "Input Error", "One or more inputs are missing.")
            return

        # Proceed with calculations if no errors
        front_spring_rate = float(self.front_spring_rate_input.text())
        front_motion_ratio = float(self.front_motion_ratio_input.text())
        twf = float(self.front_trackwidth_input.text())
        tfrs = float(self.front_target_roll_stiffness_input.text())

        neededFRS = ((1/2) * front_spring_rate * (front_motion_ratio) ** 2 * (twf) ** 2) / (57.2958 * 12)

        self.front_roll_stiffness_spring_input.setText(f"Front Roll Stiffness From Spring: {np.around(neededFRS, 3)}")
        self.front_roll_stiffness_needed_input.setText(f"Front Roll Stiffness Needed From ARB: {np.around((tfrs - neededFRS), 3)}")

    def Rear_roll_calculate(self):
        self.resetInputStyles()
        error = False

        if not self.rear_spring_rate_input.text().strip():
            self.setInputErrorStyle(self.rear_spring_rate_input)
            error = True
        if not self.rear_trackwidth_input.text().strip():
            self.setInputErrorStyle(self.rear_trackwidth_input)
            error = True
        if not self.rear_target_roll_stiffness_input.text().strip():
            self.setInputErrorStyle(self.rear_target_roll_stiffness_input)
            error = True
        if not self.rear_motion_ratio_input.text().strip():
            self.setInputErrorStyle(self.rear_motion_ratio_input)
            error = True
        
        if error:
            QtWidgets.QMessageBox.warning(self, "Input Error", "One or more inputs are missing.")
            return
        
        rear_spring_rate = float(self.rear_spring_rate_input.text())
        trrs = float(self.rear_target_roll_stiffness_input.text())
        rear_motion_ratio = float(self.rear_motion_ratio_input.text())
        twr = float(self.rear_trackwidth_input.text())

        neededRRS = ((1/2) * rear_spring_rate * (rear_motion_ratio) ** 2 * (twr) ** 2) / (57.2958 * 12)

        self.rear_roll_stiffness_spring_input.setText(f"Rear Roll Stiffness From Spring: {np.around(neededRRS, 3)}")
        self.rear_roll_stiffness_needed_input.setText(f"Rear Roll Stiffness Needed From ARB: {np.around((trrs - neededRRS), 3)}")
    
    def Roll_stiff_dist_calculate(self):
        self.resetInputStyles()
        error = False

        if not self.front_target_roll_stiffness_input.text().strip():
            self.setInputErrorStyle(self.front_target_roll_stiffness_input)
            error = True
        if not self.rear_target_roll_stiffness_input.text().strip():
            self.setInputErrorStyle(self.rear_target_roll_stiffness_input)
            error = True

        if error:
            QtWidgets.QMessageBox.warning(self, "Input Error", "One or more inputs are missing.")
            return
        
        trrs = float(self.rear_target_roll_stiffness_input.text())
        tfrs = float(self.front_target_roll_stiffness_input.text())

        self.Front_roll_dist.setText(f"Roll Stiffness Distribution: {np.around(((tfrs / (tfrs + trrs)) * 100), 3)}%")
        self.rear_roll_dist.setText(f"Roll Stiffness Distribution: {np.around(((trrs / (tfrs + trrs)) * 100), 3)}%")
        
    def Static_vehicle_mass_calculate(self):
        self.resetInputStyles()
        error = False

        if not self.lf_weight_input.text().strip():
            self.setInputErrorStyle(self.lf_weight_input)
            error = True
        if not self.rf_weight_input.text().strip():
            self.setInputErrorStyle(self.rf_weight_input)
            error = True
        if not self.lr_weight_input.text().strip():
            self.setInputErrorStyle(self.lr_weight_input)
            error = True
        if not self.rr_weight_input.text().strip():
            self.setInputErrorStyle(self.rr_weight_input)
            error = True

        if error:
            QtWidgets.QMessageBox.warning(self, "Input Error", "One or more inputs are missing.")
            return
        lfw = float(self.lf_weight_input.text())
        rfw = float(self.rf_weight_input.text())
        lrw = float(self.lr_weight_input.text())
        rrw = float(self.rr_weight_input.text())

        self.front_axle_weight_label.setText(f"Front Axle Weight: {np.around((lfw +rfw), 3)}")
        self.rear_axle_weight_label.setText(f"Rear Axle Weight: {np.around((lrw +rrw), 3)}")
        self.total_weight_label.setText(f"Total Weight: {np.around((lfw + rfw + lrw + rrw), 3)}")
        self.Front_Weight_per.setText(f"Front Weight Percentage: {np.around(((lfw + rfw) / (lfw + rfw + lrw + rrw) * 100), 3)}%")
        self.Cross_Weight_per.setText(f"Cross Weight Percentage: {np.around(((rfw + lrw) / (lfw + rfw + lrw + rrw) * 100), 3)}%")

    def setInputErrorStyle(self, input_field):
        input_field.setStyleSheet("border: 1px solid yellow;")

    def resetInputStyles(self):
        # Reset the style for all input fields to clear any error state
        # front reset inputs
        self.front_spring_rate_input.setStyleSheet("")
        self.front_motion_ratio_input.setStyleSheet("")
        self.front_trackwidth_input.setStyleSheet("")
        self.front_target_roll_stiffness_input.setStyleSheet("")

        # rear reset inputs
        self.rear_spring_rate_input.setStyleSheet("")
        self.rear_trackwidth_input.setStyleSheet("")
        self.rear_target_roll_stiffness_input.setStyleSheet("")
        self.rear_motion_ratio_input.setStyleSheet("")
        # Repeat for other input fields as necessary

        # Static mass reset inputs
        self.lf_weight_input.setStyleSheet("")
        self.rf_weight_input.setStyleSheet("")
        self.lr_weight_input.setStyleSheet("")
        self.rr_weight_input.setStyleSheet("")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MyMainWindow()
    mainWindow.show()
    sys.exit(app.exec_())