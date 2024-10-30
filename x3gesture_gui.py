# x3gesture_gui.py
# Developer: X3NIDE
# GitHub: https://github.com/mubbashirulislam

from PyQt5 import QtWidgets, QtGui
import sys
import subprocess
from x3gesture_controller import X3GestureController  # Core gesture detection logic

class X3GestureToolGUI(QtWidgets.QWidget):
    """
    GUI class for X3Gesture tool. Allows users to configure gesture detection settings
    and choose actions to be triggered upon fist gesture detection.
    """

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.controller = None

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout()

        # Branding Information
        self.brand_label = QtWidgets.QLabel("X3Gesture")
        self.brand_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.dev_info = QtWidgets.QLabel("Developer: X3NIDE | GitHub: https://github.com/mubbashirulislam")
        self.dev_info.setStyleSheet("font-size: 10px; color: gray;")
        
        # Cooldown Configuration
        self.cooldown_label = QtWidgets.QLabel("Gesture Cooldown (seconds):")
        self.cooldown_input = QtWidgets.QDoubleSpinBox()
        self.cooldown_input.setRange(0.1, 10.0)
        self.cooldown_input.setValue(1.0)

        # Resolution Toggle
        self.resolution_checkbox = QtWidgets.QCheckBox("High Resolution Mode")
        
        # Action Selection Dropdown
        self.action_label = QtWidgets.QLabel("Select Action on Fist Gesture:")
        self.action_dropdown = QtWidgets.QComboBox()
        self.action_dropdown.addItems(["Lock Screen", "Open Calculator", "Show Notification", "Shutdown PC"])

        # Start Button
        self.start_button = QtWidgets.QPushButton("Start Gesture Detection")
        self.start_button.clicked.connect(self.start_detection)

        # Arrange layout
        layout.addWidget(self.brand_label)
        layout.addWidget(self.dev_info)
        layout.addWidget(self.cooldown_label)
        layout.addWidget(self.cooldown_input)
        layout.addWidget(self.resolution_checkbox)
        layout.addWidget(self.action_label)
        layout.addWidget(self.action_dropdown)
        layout.addWidget(self.start_button)

        self.setLayout(layout)
        self.setWindowTitle("X3Gesture Tool")
        self.setGeometry(100, 100, 400, 250)

    def start_detection(self):
        """Initialize gesture controller and start detection based on user settings."""
        cooldown = self.cooldown_input.value()
        high_res = self.resolution_checkbox.isChecked()
        action = self.action_dropdown.currentText()

        # Initialize controller with callback action
        self.controller = X3GestureController(
            camera_index=0,
            high_resolution=high_res,
            gesture_cooldown=cooldown,
            action_callback=lambda: self.perform_action(action)
        )
        self.controller.run()

    def perform_action(self, action: str):
        """Perform the user-selected action upon gesture detection."""
        if action == "Lock Screen":
            subprocess.run(['rundll32.exe', 'user32.dll,LockWorkStation'], check=True)
        elif action == "Open Calculator":
            subprocess.Popen("calc.exe")
        elif action == "Show Notification":
            self.show_notification("Gesture Detected!", "Fist gesture was detected.")
        elif action == "Shutdown PC":
            subprocess.run(['shutdown', '/s', '/f', '/t', '0'], check=True)

    def show_notification(self, title: str, message: str):
        """Display a notification when a gesture is detected."""
        notification = QtWidgets.QSystemTrayIcon(self)
        notification.showMessage(title, message, QtGui.QIcon())

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    gui = X3GestureToolGUI()
    gui.show()
    sys.exit(app.exec_())
