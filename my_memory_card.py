import sys
import random
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QRadioButton, QVBoxLayout, QHBoxLayout,
    QGroupBox, QButtonGroup, QMessageBox
)
from PyQt5.QtGui import QPalette, QColor


class Question:
    def __init__(self, question, answers, correct_answer):
        self.question = question
        self.answers = answers
        self.correct_answer = correct_answer


class QuestionForm(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Форма Вопроса")
        self.setGeometry(100, 100, 400, 300)

        self.background_color = QColor(220, 220, 220)
        self.groupbox_color = QColor(200, 200, 200)

        palette = self.palette()
        palette.setColor(QPalette.Background, self.background_color)
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        self.question_label = QLabel("", self)
        self.question_label.setAlignment(Qt.AlignCenter)

        self.answer_groupbox = QGroupBox("Варианты ответов")
        self.set_groupbox_background(self.answer_groupbox, self.groupbox_color)

        self.answer_layout = QVBoxLayout()

        self.answer_buttons = []
        self.answer_group = QButtonGroup()
        self.answer_groupbox.setLayout(self.answer_layout)

        self.result_label = QLabel("", self)
        self.correct_answer_label = QLabel("", self)
        self.result_label.setAlignment(Qt.AlignCenter)
        self.correct_answer_label.setAlignment(Qt.AlignCenter)

        self.submit_button = QPushButton("Ответить", self)
        self.submit_button.clicked.connect(self.click_ok)

        self.initUI()

        self.current_question = None
        self.asked_questions = []

        self.questions = [
            Question("Какой язык программирования используется для создания интерфейсов PyQt?", ["Python", "C++", "Java", "C#"], 0),
            Question("Какая функция используется для создания приложения PyQt?", ["QApplication", "QWidget", "QDialog", "QMainWindow"], 0),
            Question("Какой layout используется для вертикального расположения виджетов?", ["QVBoxLayout", "QHBoxLayout", "QGridLayout", "QFormLayout"], 0),
            Question("Что такое сигнал в PyQt?", ["Сообщение от виджета", "Функция обработки события", "Таймер", "Класс для работы с файлами"], 0),
            Question("Для чего используется QTimer?", ["Для задержки", "Для создания цикла", "Для отображения времени", "Для создания анимации"], 0),
        ]

        self.total_questions = len(self.questions)
        self.correct_answers = 0

        self.next_question()

    def set_groupbox_background(self, groupbox, color):
        palette = groupbox.palette()
        palette.setColor(QPalette.Window, color)
        groupbox.setPalette(palette)
        groupbox.setAutoFillBackground(True)

    def initUI(self):
        answers = [""] * 4
        horizontal_layouts = [QHBoxLayout() for _ in range(2)]
        for i in range(4):
            radio_button = QRadioButton(answers[i])
            self.answer_buttons.append(radio_button)
            horizontal_layouts[i // 2].addWidget(radio_button)
            self.answer_group.addButton(radio_button, i)


        for layout in horizontal_layouts:
            self.answer_layout.addLayout(layout)

        self.answer_groupbox.hide()

        result_layout = QVBoxLayout()
        result_layout.addWidget(self.result_label)
        result_layout.addWidget(self.correct_answer_label)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.question_label)
        main_layout.addWidget(self.answer_groupbox)
        main_layout.addWidget(self.submit_button)
        main_layout.addLayout(result_layout)

        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)


        self.setLayout(main_layout)
        self.result_label.hide()
        self.correct_answer_label.hide()

    def ask(self, question_obj):
        self.current_question = question_obj
        current_answers = question_obj.answers.copy()

        random.shuffle(current_answers)

        self.question_label.setText(question_obj.question)

        for i, button in enumerate(self.answer_buttons):
            button.setText(current_answers[i])

        correct_answer_text = question_obj.answers[question_obj.correct_answer]
        for i, answer in enumerate(current_answers):
            if answer == correct_answer_text:
                self.correct_answer_index = i

        self.show_question()

    def check_answer(self):
        selected_id = self.answer_group.checkedId()
        correct_answer_index = self.correct_answer_index
        is_correct = selected_id == correct_answer_index

        if is_correct:
            self.correct_answers += 1

        self.show_correct("Правильно" if is_correct else "Неверно")

    def show_correct(self, result_text):
        self.answer_groupbox.hide()
        self.result_label.setText(result_text)

        correct_answer_text = self.current_question.answers[self.current_question.correct_answer]
        self.correct_answer_label.setText(f"Правильный ответ: {correct_answer_text}")

        self.result_label.show()
        self.correct_answer_label.show()
        self.submit_button.setText("Следующий вопрос")
        self.submit_button.clicked.disconnect(self.click_ok)
        self.submit_button.clicked.connect(self.click_ok)

    def show_question(self):
        self.answer_groupbox.show()
        self.result_label.hide()
        self.correct_answer_label.hide()
        self.submit_button.setText("Ответить")

        self.answer_group.setExclusive(False)
        for button in self.answer_buttons:
            button.setChecked(False)
        self.answer_group.setExclusive(True)

    def next_question(self):
        available_questions = [q for i, q in enumerate(self.questions) if i not in self.asked_questions]

        if not available_questions:
            self.end_test()
            return

        next_question_index = self.questions.index(random.choice(available_questions))
        self.asked_questions.append(next_question_index)
        self.ask(self.questions[next_question_index])

    def click_ok(self):
        if self.submit_button.text() == "Ответить":
            self.check_answer()
        else:
            self.show_question()
            self.next_question()
            self.submit_button.clicked.disconnect(self.click_ok)
            self.submit_button.clicked.connect(self.click_ok)

    def end_test(self):
        QMessageBox.information(self, "Тест завершен",
                                f"Тест завершен!\nПравильных ответов: {self.correct_answers} / {self.total_questions}")
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QuestionForm()
    window.show()
    sys.exit(app.exec_())