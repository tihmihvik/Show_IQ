from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QRadioButton, QButtonGroup, QComboBox, QLabel, QLineEdit, QTextEdit
from PyQt6.QtCore import Qt
import os
import re
from save_settings import SaveSettingsDialog

class SettingsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Настройки игры")
        self.setGeometry(200, 200, 300, 200)

        central_widget = QWidget()
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Переключатель "4 команды" и "10 команд" в верхней части окна
        self.radio_group = QButtonGroup(self)
        self.radio_4 = QRadioButton("4 команды")
        self.radio_10 = QRadioButton("10 команд")
        self.radio_4.setChecked(True)
        self.radio_group.addButton(self.radio_4)
        self.radio_group.addButton(self.radio_10)
        self.layout.addWidget(self.radio_4)
        self.layout.addWidget(self.radio_10)

        # Заголовок "Жеребьёвка"
        from PyQt6.QtWidgets import QLabel
        draw_label = QLabel("Жеребьёвка")
        draw_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(draw_label)

        self.radio_4.toggled.connect(self.update_team_selectors)
        self.radio_10.toggled.connect(self.update_team_selectors)

        # Список команд для выпадающих списков
        self.teams = [
            "Анжеро-Судженская МО ВОС",
            "Беловская МО ВОС",
            "Кемеровская МО ВОС",
            "Киселёвская МО ВОС",
            "Ленинск-Кузнецкая МО ВОС",
            "Мариинская МО ВОС",
            "Междуреченская МО ВОС",
            "Новокузнецкая МО ВОС",
            "Осиниковская МО ВОС",
            "Прокопьевская МО ВОС",
            "Юргинская МО ВОС"
        ]

        # Контейнер для выпадающих списков
        self.comboboxes = []
        self.combobox_widget = QWidget()
        self.combobox_layout = QVBoxLayout()
        self.combobox_widget.setLayout(self.combobox_layout)
        self.layout.addWidget(self.combobox_widget)

        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

        self.update_team_selectors()
        self.load_questions()

    def update_team_selectors(self):
        from PyQt6.QtWidgets import QLabel, QHBoxLayout, QPushButton, QTextEdit
        # Очистить старые комбобоксы, лейблы, строки, кнопки и заголовок
        for cb in self.comboboxes:
            self.combobox_layout.removeWidget(cb)
            cb.deleteLater()
        self.comboboxes.clear()
        if hasattr(self, 'combo_labels'):
            for lbl in self.combo_labels:
                self.combobox_layout.removeWidget(lbl)
                lbl.deleteLater()
        self.combo_labels = []
        if hasattr(self, 'combo_rows'):
            for row in self.combo_rows:
                # Удаляем все виджеты из row_layout
                for i in reversed(range(row.count())):
                    item = row.itemAt(i)
                    widget = item.widget()
                    if widget is not None:
                        row.removeWidget(widget)
                        widget.deleteLater()
                self.combobox_layout.removeItem(row)
        self.combo_rows = []
        # Удалить старый заголовок и поле, если они есть
        if hasattr(self, 'load_label') and self.load_label is not None:
            self.combobox_layout.removeWidget(self.load_label)
            self.load_label.deleteLater()
            self.load_label = None
        if hasattr(self, 'questions_info') and self.questions_info is not None:
            self.combobox_layout.removeWidget(self.questions_info)
            self.questions_info.deleteLater()
            self.questions_info = None
        # Удалить старый блок кнопок, если есть
        if hasattr(self, 'button_layout') and self.button_layout is not None:
            # Удаляем все кнопки из layout и сам layout
            for i in reversed(range(self.button_layout.count())):
                btn = self.button_layout.itemAt(i).widget()
                if btn is not None:
                    self.button_layout.removeWidget(btn)
                    btn.deleteLater()
            self.combobox_layout.removeItem(self.button_layout)
            self.button_layout = None

        count = 4 if self.radio_4.isChecked() else 10
        for i in range(count):
            row_layout = QHBoxLayout()
            label = QLabel(f"{i+1}.")
            row_layout.addWidget(label)
            self.combo_labels.append(label)
            combo = QComboBox()
            combo.addItem("")  # Пустой элемент
            combo.addItems(self.teams)
            combo.currentIndexChanged.connect(self.handle_combobox_change)
            row_layout.addWidget(combo)
            self.comboboxes.append(combo)
            clear_btn = QPushButton("Очистить")
            clear_btn.setFixedWidth(70)
            clear_btn.clicked.connect(lambda _, c=combo: c.setCurrentIndex(0))
            row_layout.addWidget(clear_btn)
            self.combobox_layout.addLayout(row_layout)
            self.combo_rows.append(row_layout)

        # Добавить только один заголовок и поле внизу
        self.load_label = QLabel("Загрузка списка вопросов:")
        self.combobox_layout.addWidget(self.load_label)
        self.questions_info = QTextEdit()
        self.questions_info.setReadOnly(True)
        self.questions_info.setFixedHeight(60)
        self.combobox_layout.addWidget(self.questions_info)
        # Кнопки в самом низу окна (добавлять только если ещё не добавлены)
        from PyQt6.QtWidgets import QPushButton, QHBoxLayout
        if not hasattr(self, 'button_layout') or self.button_layout is None:
            self.button_layout = QHBoxLayout()
            self.save_exit_btn = QPushButton("Сохранить и выйти")
            self.save_continue_btn = QPushButton("Сохранить и продолжить")
            self.cancel_btn = QPushButton("Отмена")
            self.combobox_layout.addLayout(self.button_layout)
        else:
            # Очищаем layout, если он уже есть
            for i in reversed(range(self.button_layout.count())):
                btn = self.button_layout.itemAt(i).widget()
                if btn is not None:
                    self.button_layout.removeWidget(btn)
                    btn.deleteLater()
            self.save_exit_btn = QPushButton("Сохранить и выйти")
            self.save_continue_btn = QPushButton("Сохранить и продолжить")
            self.cancel_btn = QPushButton("Отмена")
        # Подключаем обработчики
        self.save_exit_btn.clicked.connect(self.open_save_dialog_exit)
        self.save_continue_btn.clicked.connect(self.open_save_dialog_exit)
        self.cancel_btn.clicked.connect(self.close)
        self.button_layout.addWidget(self.save_exit_btn)
        self.button_layout.addWidget(self.save_continue_btn)
        self.button_layout.addWidget(self.cancel_btn)

        # После обновления — снова вывести информацию
        self.load_questions_info()
        self.adjustSize()

    def handle_combobox_change(self):
        # Получить выбранные значения
        selected = set()
        for cb in self.comboboxes:
            text = cb.currentText()
            if text:
                selected.add(text)
        # Обновить доступность пунктов в каждом комбобоксе
        for cb in self.comboboxes:
            for i in range(1, cb.count()):  # 0 - пустой элемент
                item_text = cb.itemText(i)
                was_selected = cb.currentText() == item_text
                cb.model().item(i).setEnabled(was_selected or item_text not in selected)

    def load_questions(self):
        # Путь к файлу на рабочем столе или в рабочей папке
        file_path = os.path.join(os.path.dirname(__file__), 'Список вопросов.txt')
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        # Регулярное выражение для поиска блоков
        pattern = re.compile(r'(Тема\s*\d+:?.*?)(Оценка вопроса: ?[123] балл[а.]*)', re.DOTALL)
        blocks = pattern.split(text)
        q1, q2, q3 = {}, {}, {}
        i = 1
        while i < len(blocks):
            header = blocks[i].strip().replace('\n', ' ')
            score = blocks[i+1].strip().replace('\n', ' ')
            # Найти текст вопросов после оценки
            questions_text = ''
            if i+2 < len(blocks):
                questions_text = blocks[i+2].strip()
            # Разделить вопросы по пустым строкам
            questions = [q.strip() for q in re.split(r'\n\s*\n', questions_text) if q.strip()]
            key = f"{header} {score}"
            if '1 балл' in score:
                q1[key] = questions
            elif '2 балл' in score:
                q2[key] = questions
            elif '3 балл' in score:
                q3[key] = questions
            i += 3
        self.questions_1 = q1
        self.questions_2 = q2
        self.questions_3 = q3
        # Вывод информации в текстовое поле
        info = (
            f"Тем с оценкой 1 балл: {len(self.questions_1)}, вопросов: {sum(len(v) for v in self.questions_1.values())}\n"
            f"Тем с оценкой 2 балла: {len(self.questions_2)}, вопросов: {sum(len(v) for v in self.questions_2.values())}\n"
            f"Тем с оценкой 3 балла: {len(self.questions_3)}, вопросов: {sum(len(v) for v in self.questions_3.values())}"
        )
        self.questions_info.setPlainText(info)

    def load_questions_info(self):
        if hasattr(self, 'questions_1') and hasattr(self, 'questions_2') and hasattr(self, 'questions_3'):
            info = (
                f"Тем с оценкой 1 балл: {len(self.questions_1)}, вопросов: {sum(len(v) for v in self.questions_1.values())}\n"
                f"Тем с оценкой 2 балла: {len(self.questions_2)}, вопросов: {sum(len(v) for v in self.questions_2.values())}\n"
                f"Тем с оценкой 3 балла: {len(self.questions_3)}, вопросов: {sum(len(v) for v in self.questions_3.values())}"
            )
            self.questions_info.setPlainText(info)

    def open_save_dialog(self):
        dialog = SaveSettingsDialog(self)
        dialog.exec()

    def open_save_dialog_exit(self):
        dialog = SaveSettingsDialog(self)
        dialog.exec()
