from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
import sys
from start import StartWindow  # Предполагается, что в start.py есть класс StartWindow

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Стартовое окно")
        self.setGeometry(100, 100, 400, 300)

        # Создаем центральный виджет и компоновку
        central_widget = QWidget()
        layout = QVBoxLayout()

        # Кнопка "Начать новую игру"
        new_game_button = QPushButton("Начать новую игру")
        new_game_button.clicked.connect(self.start_new_game)
        layout.addWidget(new_game_button)

        # Кнопка "Запустить сохранённую игру"
        load_game_button = QPushButton("Запустить сохранённую игру")
        load_game_button.clicked.connect(self.load_saved_game)
        layout.addWidget(load_game_button)

        # Устанавливаем компоновку и центральный виджет
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def start_new_game(self):
        # Логика для начала новой игры
        print("Начать новую игру")
        self.open_start_window()

    def load_saved_game(self):
        # Логика для загрузки сохранённой игры
        print("Запустить сохранённую игру")
        self.open_start_window()

    def open_start_window(self):
        # Открытие окна из модуля start.py
        self.start_window = StartWindow()
        self.start_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = Main()
    main_window.show()
    sys.exit(app.exec())