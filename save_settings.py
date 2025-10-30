from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QMessageBox
import sqlite3
import os
from game import Game

class SaveSettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Введите любое имя")
        self.setModal(True)
        self.setMinimumWidth(300)

        layout = QVBoxLayout()
        label = QLabel("Введите любое имя")
        layout.addWidget(label)

        self.name_edit = QLineEdit()
        layout.addWidget(self.name_edit)

        button_layout = QHBoxLayout()
        self.save_btn = QPushButton("Сохранить")
        self.cancel_btn = QPushButton("Отмена")
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.cancel_btn)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        # Подключаем обработчик сохранения
        self.save_btn.clicked.connect(self.on_save)

    def on_save(self):
        name = self.name_edit.text().strip()
        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите имя для файла базы данных")
            return

        # Путь к файлу базы данных в папке проекта
        db_path = os.path.join(os.path.dirname(__file__), f"{name}.db")

        # Получаем данные из родительского окна (SettingsWindow)
        parent = self.parent()
        questions_1 = getattr(parent, 'questions_1', {}) if parent is not None else {}
        questions_2 = getattr(parent, 'questions_2', {}) if parent is not None else {}
        questions_3 = getattr(parent, 'questions_3', {}) if parent is not None else {}
        # Получаем список игроков из выпадающих списков (текущие выбранные значения)
        players = []
        if parent is not None and hasattr(parent, 'comboboxes'):
            for cb in parent.comboboxes:
                try:
                    text = cb.currentText().strip()
                except Exception:
                    text = ''
                if text:
                    players.append(text)

        try:
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()

            # Создать таблицы
            cur.execute('''
                CREATE TABLE IF NOT EXISTS игроки (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    numeration INTEGER,
                    игрок TEXT
                )
            ''')

            cur.execute('''
                CREATE TABLE IF NOT EXISTS вопросы (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    numeration INTEGER,
                    баллы INTEGER,
                    вопрос TEXT,
                    игрок_id INTEGER,
                    оценка INTEGER,
                    FOREIGN KEY(игрок_id) REFERENCES игроки(id)
                )
            ''')

            # Заполнить таблицу игроков
            cur.execute('DELETE FROM игроки')
            for idx, player_name in enumerate(players, start=1):
                cur.execute('INSERT INTO игроки (numeration, игрок) VALUES (?, ?)', (idx, player_name))

            # Получить id игроков (в порядке вставки)
            cur.execute('SELECT id FROM игроки ORDER BY id')
            player_ids = [row[0] for row in cur.fetchall()]

            # Заполнить таблицу вопросов
            cur.execute('DELETE FROM вопросы')
            numeration = 1
            # helper to insert questions from dict
            def insert_questions(qdict, points):
                nonlocal numeration
                for key, qlist in qdict.items():
                    for q in qlist:
                        cur.execute(
                            'INSERT INTO вопросы (numeration, баллы, вопрос, игрок_id, оценка) VALUES (?, ?, ?, ?, ?)',
                            (numeration, points, q, None, 0)
                        )
                        numeration += 1

            insert_questions(questions_1, 1)
            insert_questions(questions_2, 2)
            insert_questions(questions_3, 3)

            conn.commit()
            conn.close()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить базу данных:\n{e}")
            return

        # Показать сообщение и открыть игровое окно только после нажатия ОК
        ret = QMessageBox.information(self, "Готово", f"База данных сохранена в {db_path}", QMessageBox.StandardButton.Ok)
        if ret == QMessageBox.StandardButton.Ok:
            try:
                # Создаём окно игры и сохраняем ссылку в QApplication, чтобы объект не уничтожался при закрытии диалога
                from PyQt6.QtWidgets import QApplication
                app = QApplication.instance()
                app.game_window = Game()
                app.game_window.show()
                if parent is not None:
                    parent.close()
            except Exception as e:
                QMessageBox.warning(self, "Ошибка", f"Не удалось открыть игровое окно:\n{e}")
            self.accept()
