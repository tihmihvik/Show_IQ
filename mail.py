from PyQt6.QtWidgets import QApplication
from start import StartWindow
import sys

class Main:
    def run(self):
        app = QApplication(sys.argv)
        window = StartWindow()
        window.show()
        sys.exit(app.exec())
