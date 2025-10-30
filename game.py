from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

class Game(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Игра")
        self.resize(1000, 600)

        central = QWidget()
        layout = QVBoxLayout()
        label = QLabel("Игровое окно")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        central.setLayout(layout)
        self.setCentralWidget(central)
