from PyQt6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt
from settings import SettingsWindow

class StartWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Окно игры")
        self.setGeometry(150, 150, 400, 300)

        # Создаем центральный виджет и компоновку
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Кнопка "Начать игру"
        start_button = QPushButton("Начать игру")
        start_button.setFixedWidth(start_button.sizeHint().width())
        start_button.clicked.connect(self.open_settings)
        layout.addWidget(start_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Кнопка "Запуск сохранённой игры"
        load_button = QPushButton("Запуск сохранённой игры")
        load_button.setFixedWidth(load_button.sizeHint().width())
        load_button.clicked.connect(self.load_game)
        layout.addWidget(load_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Кнопка "Выход"
        exit_button = QPushButton("Выход")
        exit_button.setFixedWidth(exit_button.sizeHint().width())
        exit_button.clicked.connect(self.exit_app)
        layout.addWidget(exit_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Устанавливаем компоновку и центральный виджет
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.adjustSize()

    def open_settings(self):
        self.settings_window = SettingsWindow()
        self.settings_window.show()
        self.close()

    def start_game(self):
        # Логика для начала новой игры
        print("Начать игру")

    def load_game(self):
        # Логика для запуска сохранённой игры
        print("Запуск сохранённой игры")

    def exit_app(self):
        self.close()