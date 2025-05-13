from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget

class SettingsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Настройки игры")
        self.setGeometry(200, 200, 300, 200)

        central_widget = QWidget()
        layout = QVBoxLayout()

        label = QLabel("Здесь будут настройки игры")
        layout.addWidget(label)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
