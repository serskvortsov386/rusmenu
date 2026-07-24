"""
Пример использования RusMenu с PyQt5/PySide6
"""

import sys

try:
    from PyQt5 import QtWidgets, QtCore
except ImportError:
    from PySide6 import QtWidgets, QtCore

from rusmenu import RusContextMenu, RusMenuConfig


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RusMenu - Qt Example")
        self.setGeometry(100, 100, 600, 500)
        
        # Создаем центральный виджет
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QVBoxLayout(central)
        layout.setSpacing(15)
        
        # Заголовок
        label = QtWidgets.QLabel("Кликни правой кнопкой на любом поле ввода")
        label.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(label)
        
        # Поле ввода
        layout.addWidget(QtWidgets.QLabel("Поле ввода (QLineEdit):"))
        self.line_edit = QtWidgets.QLineEdit()
        self.line_edit.setText("Пример текста для тестирования")
        layout.addWidget(self.line_edit)
        
        # Многострочное поле
        layout.addWidget(QtWidgets.QLabel("Многострочное поле (QTextEdit):"))
        self.text_edit = QtWidgets.QTextEdit()
        self.text_edit.setPlainText("Многострочное поле\nс русским контекстным меню")
        layout.addWidget(self.text_edit)
        
        # Поле с паролем
        layout.addWidget(QtWidgets.QLabel("Поле с паролем (QLineEdit):"))
        self.password_edit = QtWidgets.QLineEdit()
        self.password_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_edit.setText("secret_password")
        layout.addWidget(self.password_edit)
        
        # Выпадающий список
        layout.addWidget(QtWidgets.QLabel("Выпадающий список (QComboBox):"))
        self.combo = QtWidgets.QComboBox()
        self.combo.addItems(["Пункт 1", "Пункт 2", "Пункт 3", "Пункт 4"])
        layout.addWidget(self.combo)
        
        # Применяем конфигурацию
        config = RusMenuConfig()
        config.font_family = "Arial"
        config.font_size = 11
        config.bg_color = "#f0f0f0"
        config.hover_bg = "#4a90d9"
        config.hover_fg = "#ffffff"
        
        # Создаем меню для каждого виджета
        menu1 = RusContextMenu(self.line_edit, config=config)
        menu2 = RusContextMenu(self.text_edit, config=config)
        menu3 = RusContextMenu(self.password_edit, config=config)
        menu4 = RusContextMenu(self.combo, config=config)
        
        # Добавляем кастомные пункты
        
        # Для line_edit
        def show_text():
            QtWidgets.QMessageBox.information(
                self, "Информация", 
                f"Текст: {self.line_edit.text()}"
            )
        menu1.add_command("ℹ️ Информация", show_text, shortcut="Ctrl+I")
        
        # Для text_edit
        def count_words():
            text = self.text_edit.toPlainText()
            words = len(text.split())
            QtWidgets.QMessageBox.information(
                self, "Статистика", 
                f"Количество слов: {words}"
            )
        menu2.add_command("📊 Статистика", count_words, shortcut="Ctrl+Shift+W")
        
        # Для password_edit
        def toggle_password():
            if self.password_edit.echoMode() == QtWidgets.QLineEdit.Password:
                self.password_edit.setEchoMode(QtWidgets.QLineEdit.Normal)
            else:
                self.password_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        menu3.add_command("👁️ Показать пароль", toggle_password, shortcut="Ctrl+P")
        
        # Для combo
        def show_selection():
            QtWidgets.QMessageBox.information(
                self, "Выбор", 
                f"Выбрано: {self.combo.currentText()}"
            )
        menu4.add_command("ℹ️ Показать выбор", show_selection, shortcut="Ctrl+Shift+S")


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()