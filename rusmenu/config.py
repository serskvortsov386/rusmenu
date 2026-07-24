"""
Configuration module for RusMenu
"""

class RusMenuConfig:
    """Конфигурация для всех меню"""
    
    def __init__(self):
        self.translations = {
            "copy": "Копировать",
            "cut": "Вырезать",
            "paste": "Вставить",
            "delete": "Удалить",
            "select_all": "Выделить всё",
            "undo": "Отменить",
            "redo": "Повторить",
            "clear": "Очистить",
            "find": "Найти",
            "replace": "Заменить",
            "select_word": "Выделить слово",
            "select_line": "Выделить строку"
        }
        
        # Настройки шрифтов и цветов
        self.font_family = "Segoe UI"
        self.font_size = 10
        self.font_weight = "normal"  # normal, bold
        
        self.bg_color = "#f0f0f0"
        self.fg_color = "#000000"
        self.hover_bg = "#cce8ff"
        self.hover_fg = "#000000"
        self.separator_color = "#c0c0c0"
        
        # Горячие клавиши
        self.shortcuts = {
            "copy": "Ctrl+C",
            "cut": "Ctrl+X",
            "paste": "Ctrl+V",
            "delete": "Del",
            "select_all": "Ctrl+A",
            "undo": "Ctrl+Z",
            "redo": "Ctrl+Y",
            "clear": "Ctrl+Shift+C",
            "find": "Ctrl+F",
            "replace": "Ctrl+H"
        }
        
        # Настройки для Dear PyGui
        self.dpg_theme_color = (255, 255, 255, 255)
        self.dpg_bg_color = (40, 40, 40, 255)
        self.dpg_hover_color = (60, 100, 200, 255)