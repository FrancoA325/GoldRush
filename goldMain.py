from PyQt5 import QtWidgets
import numpy as np
from goldRush import Ui_MainWindow  # Import the auto-generated UI class

class MyMainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    neededFRS = 0
    front_roll_stiffness_arb = 0
    neededRRS = 0
    rear_roll_stiffness_arb = 0
    front_roll_dist = 0
    rear_roll_dist = 0
    front_axle_weight = 0
    rear_axle_weight = 0
    total_weight = 0
    front_weight_percentage = 0
    cross_weight_percentage = 0
    cog_to_rear_axle = 0
    cog_to_front_axle = 0
    rolling_level_arm = 0
    rolling_moment = 0

    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.Front_roll_button.clicked.connect(self.Front_roll_calculate)
        self.Rear_roll_button.clicked.connect(self.Rear_roll_calculate)
        self.Roll_stiff_dist.clicked.connect(self.Roll_stiff_dist_calculate)

        self.Static_vehicle_mass_button.clicked.connect(self.Static_vehicle_mass_calculate)
        self.static_geo_button.clicked.connect(self.Static_vehicle_geometry_calculate)

        self.misc_arb_calc.clicked.connect(self.misc_arb_calculate)

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

        self.neededFRS = np.around(((1/2) * front_spring_rate * (front_motion_ratio) ** 2 * (twf) ** 2) / (57.2958 * 12), 3)
        self.front_roll_stiffness_arb = np.around((tfrs - self.neededFRS), 3)

        self.front_roll_stiffness_spring_input.setText(f"Front Roll Stiffness From Spring: {self.neededFRS}")
        self.front_roll_stiffness_needed_input.setText(f"Front Roll Stiffness Needed From ARB: {self.front_roll_stiffness_arb}")

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

        self.neededRRS = np.around(((1/2) * rear_spring_rate * (rear_motion_ratio) ** 2 * (twr) ** 2) / (57.2958 * 12), 3)
        self.rear_roll_stiffness_arb = np.around((trrs - self.neededRRS), 3)

        self.rear_roll_stiffness_spring_input.setText(f"Rear Roll Stiffness From Spring: {self.neededRRS}")
        self.rear_roll_stiffness_needed_input.setText(f"Rear Roll Stiffness Needed From ARB: {self.rear_roll_stiffness_arb}")
    
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

        self.front_roll_dist = np.around(((tfrs / (tfrs + trrs)) * 100), 3)
        self.rear_roll_dist = np.around(((trrs / (tfrs + trrs)) * 100), 3)

        self.Front_roll_dist.setText(f"Roll Stiffness Distribution: {self.front_roll_dist}%")
        self.Rear_roll_dist.setText(f"Roll Stiffness Distribution: {self.rear_roll_dist}%")
        
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

        self.front_axle_weight = np.around((lfw + rfw), 3)
        self.rear_axle_weight = np.around((lrw + rrw), 3)
        self.total_weight = np.around((lfw + rfw + lrw + rrw), 3)
        self.front_weight_percentage = np.around(((lfw + rfw) / (lfw + rfw + lrw + rrw) * 100), 3)
        self.cross_weight_percentage = np.around(((rfw + lrw) / (lfw + rfw + lrw + rrw) * 100), 3)

        self.front_axle_weight_label.setText(f"Front Axle Weight: {self.front_axle_weight}")
        self.rear_axle_weight_label.setText(f"Rear Axle Weight: {self.rear_axle_weight}")
        self.total_weight_label.setText(f"Total Weight: {self.total_weight}")
        self.Front_Weight_per.setText(f"Front Weight Percentage: {self.front_weight_percentage}%")
        self.Cross_Weight_per.setText(f"Cross Weight Percentage: {self.cross_weight_percentage}%")
    
    def Static_vehicle_geometry_calculate(self):
        self.resetInputStyles()
        error = False

        if not self.front_trackwidth_input.text().strip():
            self.setInputErrorStyle(self.front_trackwidth_input)
            error = True
        if not self.rear_trackwidth_input.text().strip():
            self.setInputErrorStyle(self.rear_trackwidth_input)
            error = True
        if not self.wheelbase_input.text().strip():
            self.setInputErrorStyle(self.wheelbase_input)
            error = True
        if not self.static_front_rc_height_input.text().strip():
            self.setInputErrorStyle(self.static_front_rc_height_input)
            error = True
        if not self.static_rear_rc_height_input.text().strip():
            self.setInputErrorStyle(self.static_rear_rc_height_input)
            error = True
        if not self.cog_height_input.text().strip():
            self.setInputErrorStyle(self.cog_height_input)
            error = True

        if error:
            QtWidgets.QMessageBox.warning(self, "Input Error", "One or more inputs are missing.")
            return
        
        # twf = float(self.front_trackwidth_input.text())
        # twr = float(self.rear_trackwidth_input.text())
        wb = float(self.wheelbase_input.text())
        # sfrc = float(self.static_front_rc_height_input.text())
        # src = float(self.static_rear_rc_height_input.text())
        # cogh = float(self.cog_height_input.text())

        self.cog_to_rear_axle = np.around((wb - 29), 3)
        self.cog_to_front_axle = np.around((wb - (wb - 29)), 3)

        self.COG_rear_axle.setText(f"COG to Rear Axle: {self.cog_to_rear_axle}")
        self.COG_front_axle.setText(f"COG to Front Axle: {self.cog_to_front_axle}")

    def misc_arb_calculate(self):
        self.resetInputStyles()
        error = False

        if not self.static_front_rc_height_input.text().strip():
            self.setInputErrorStyle(self.static_front_rc_height_input)
            error = True
        if not self.static_rear_rc_height_input.text().strip():
            self.setInputErrorStyle(self.static_rear_rc_height_input)
            error = True
        if not self.cog_height_input.text().strip():
            self.setInputErrorStyle(self.cog_height_input)
            error = True
        if not self.total_weight_label:
            error = True
        if not self.front_weight_percentage:
            error = True
        if error:
            QtWidgets.QMessageBox.warning(self, "Input Error", "One or more inputs are missing.")
            return
        
        sfrc = float(self.static_front_rc_height_input.text())
        srrc = float(self.static_rear_rc_height_input.text())
        cogh = float(self.cog_height_input.text())
        fwp = self.front_weight_percentage
        tw = self.total_weight

        rmla = (cogh - (sfrc + (srrc - sfrc) * (1 - (fwp / 100))))

        self.rolling_level_arm = np.around(rmla, 3)
        self.rolling_moment = np.around(((rmla * tw) / 12), 3)
        self.Rolling_lever_arm.setText(f"Rolling Lever Arm: {np.around(rmla, 3)}")
        self.Rolling_Moment.setText(f"Rolling Moment: {np.around(((rmla * tw) / 12), 3)}")

    def front_torsional_stiffness(self):
        self.resetInputStyles()
        error = False

        if not self.neededFRS:
            error = True
        if not self.front_roll_stiffness_arb:
            error = True

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

        # static vehicle geometry reset inputs
        self.front_trackwidth_input.setStyleSheet("")
        self.rear_trackwidth_input.setStyleSheet("")
        self.wheelbase_input.setStyleSheet("")
        self.static_front_rc_height_input.setStyleSheet("")
        self.static_rear_rc_height_input.setStyleSheet("")
        self.cog_height_input.setStyleSheet("")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MyMainWindow()
    mainWindow.show()
    sys.exit(app.exec_())