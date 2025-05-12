from PyQt6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget
from settings import SettingsWindow

class StartWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Окно игры")
        self.setGeometry(150, 150, 400, 300)

        # Создаем центральный виджет и компоновку
        central_widget = QWidget()
        layout = QVBoxLayout()

        # Кнопка "Начать игру"
        start_game_button = QPushButton("Начать игру")
        start_game_button.clicked.connect(self.open_settings_window)
        layout.addWidget(start_game_button)

        # Кнопка "Продолжить игру"
        continue_button = QPushButton("Продолжить игру")
        continue_button.clicked.connect(self.continue_game)
        layout.addWidget(continue_button)

        # Кнопка "Выйти из игры"
        exit_button = QPushButton("Выйти из игры")
        exit_button.clicked.connect(self.exit_game)
        layout.addWidget(exit_button)

        # Устанавливаем компоновку и центральный виджет
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def open_settings_window(self):
        # Открытие окна настроек
        self.settings_window = SettingsWindow()
        self.settings_window.show()

    def continue_game(self):
        # Логика для продолжения игры
        print("Продолжить игру")

    def exit_game(self):
        # Логика для выхода из игры
        print("Выйти из игры")
        self.close()