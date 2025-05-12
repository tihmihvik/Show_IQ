from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel

class SettingsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Настройки игры")
        self.setGeometry(200, 200, 400, 300)

        # Создаем центральный виджет и компоновку
        central_widget = QWidget()
        layout = QVBoxLayout()

        # Пример настройки: текстовая метка
        label = QLabel("Настройки игры будут здесь")
        layout.addWidget(label)

        # Устанавливаем компоновку и центральный виджет
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)