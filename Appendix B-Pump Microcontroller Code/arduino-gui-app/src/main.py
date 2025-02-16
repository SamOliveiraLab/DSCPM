from PyQt5.QtWidgets import QApplication
from gui.app import ArduinoGUI
import sys


def main():
    app = QApplication(sys.argv)
    window = ArduinoGUI()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
