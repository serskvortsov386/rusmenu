"""
Qt backend for RusMenu
Поддерживает: PyQt5 и PySide6
"""

import sys

# Пытаемся импортировать Qt
try:
    from PyQt5 import QtWidgets, QtCore, QtGui
    QT_VERSION = "PyQt5"
except ImportError:
    try:
        from PySide6 import QtWidgets, QtCore, QtGui
        QT_VERSION = "PySide6"
    except ImportError:
        raise ImportError("PyQt5 or PySide6 is required for Qt backend")


class RusQtMenu:
    """
    Реализация русского контекстного меню для PyQt5/PySide6
    
    Поддерживает: QLineEdit, QTextEdit, QPlainTextEdit, QComboBox
    """
    
    def __init__(self, widget, include_default=True, config=None):
        self.widget = widget
        self.config = config
        self.custom_actions = []
        self._shortcuts_setup = False
        
        # Создаем меню
        self.menu = QtWidgets.QMenu()
        
        # Применяем стили
        self._apply_styles()
        
        if include_default:
            self.build_default_menu()
        
        # Устанавливаем политику контекстного меню
        widget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        widget.customContextMenuRequested.connect(self.show_menu)
        
        # Добавляем горячие клавиши
        self._setup_shortcuts()
    
    def _apply_styles(self):
        """Применяет стили к меню через CSS"""
        style = f"""
            QMenu {{
                background-color: {self.config.bg_color};
                color: {self.config.fg_color};
                font-family: "{self.config.font_family}";
                font-size: {self.config.font_size}pt;
                border: 1px solid #cccccc;
                padding: 5px 0px;
            }}
            QMenu::item {{
                padding: 5px 30px 5px 20px;
                margin: 0px 0px;
            }}
            QMenu::item:selected {{
                background-color: {self.config.hover_bg};
                color: {self.config.hover_fg};
            }}
            QMenu::separator {{
                height: 1px;
                background-color: {self.config.separator_color};
                margin: 5px 10px;
            }}
        """
        self.menu.setStyleSheet(style)
    
    def _setup_shortcuts(self):
        """Настраивает горячие клавиши для виджета"""
        if self._shortcuts_setup:
            return
        self._shortcuts_setup = True
        
        shortcuts = {
            "Ctrl+C": self.copy,
            "Ctrl+X": self.cut,
            "Ctrl+V": self.paste,
            "Ctrl+A": self.select_all,
            "Del": self.delete,
            "Delete": self.delete,
        }
        
        for key, func in shortcuts.items():
            action = QtWidgets.QAction(self.widget)
            action.setShortcut(QtGui.QKeySequence(key))
            action.triggered.connect(func)
            self.widget.addAction(action)
    
    def build_default_menu(self):
        """Собирает стандартное меню"""
        trans = self.config.translations
        shortcuts = self.config.shortcuts
        
        # Отменить/Повторить
        undo_action = self.menu.addAction(f"{trans['undo']}\t{shortcuts['undo']}")
        undo_action.triggered.connect(self.undo)
        
        redo_action = self.menu.addAction(f"{trans['redo']}\t{shortcuts['redo']}")
        redo_action.triggered.connect(self.redo)
        
        self.menu.addSeparator()
        
        # Основные команды
        cut_action = self.menu.addAction(f"{trans['cut']}\t{shortcuts['cut']}")
        cut_action.triggered.connect(self.cut)
        
        copy_action = self.menu.addAction(f"{trans['copy']}\t{shortcuts['copy']}")
        copy_action.triggered.connect(self.copy)
        
        paste_action = self.menu.addAction(f"{trans['paste']}\t{shortcuts['paste']}")
        paste_action.triggered.connect(self.paste)
        
        delete_action = self.menu.addAction(f"{trans['delete']}\t{shortcuts['delete']}")
        delete_action.triggered.connect(self.delete)
        
        self.menu.addSeparator()
        
        select_all_action = self.menu.addAction(f"{trans['select_all']}\t{shortcuts['select_all']}")
        select_all_action.triggered.connect(self.select_all)
    
    def add_command(self, label, command, shortcut=None):
        """
        Добавляет пользовательский пункт меню
        
        Args:
            label (str): Название пункта
            command (callable): Функция для выполнения
            shortcut (str, optional): Горячая клавиша
        """
        if shortcut:
            label = f"{label}\t{shortcut}"
        
        self.menu.addSeparator()
        action = self.menu.addAction(label)
        action.triggered.connect(command)
        self.custom_actions.append(action)
        
        # Если указан shortcut, добавляем действие в виджет
        if shortcut:
            shortcut_action = QtWidgets.QAction(self.widget)
            shortcut_action.setShortcut(QtGui.QKeySequence(shortcut))
            shortcut_action.triggered.connect(command)
            self.widget.addAction(shortcut_action)
        
        return self
    
    def show_menu(self, position):
        """Показывает меню в позиции курсора"""
        self.menu.exec_(self.widget.mapToGlobal(position))
    
    # --- Базовые функции для Qt ---
    def copy(self):
        """Копировать выделенный текст"""
        self.widget.copy()
    
    def cut(self):
        """Вырезать выделенный текст"""
        self.widget.cut()
    
    def paste(self):
        """Вставить текст из буфера обмена"""
        self.widget.paste()
    
    def delete(self):
        """Удалить выделенный текст"""
        if hasattr(self.widget, 'textCursor'):
            cursor = self.widget.textCursor()
            if cursor.hasSelection():
                cursor.removeSelectedText()
        elif hasattr(self.widget, 'backspace'):
            self.widget.backspace()
        else:
            # Для QLineEdit
            if hasattr(self.widget, 'cursorPosition'):
                cursor_pos = self.widget.cursorPosition()
                if cursor_pos > 0:
                    self.widget.backspace()
    
    def select_all(self):
        """Выделить весь текст"""
        self.widget.selectAll()
    
    def undo(self):
        """Отменить действие"""
        if hasattr(self.widget, 'undo'):
            self.widget.undo()
    
    def redo(self):
        """Повторить действие"""
        if hasattr(self.widget, 'redo'):
            self.widget.redo()