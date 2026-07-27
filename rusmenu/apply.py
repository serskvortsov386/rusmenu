"""
Функции для массового применения русского меню ко всем виджетам
"""

import sys

# Проверяем доступность фреймворков
try:
    import tkinter as tk
    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False

try:
    from PyQt5 import QtWidgets
    PYQT_AVAILABLE = True
except ImportError:
    try:
        from PySide6 import QtWidgets
        PYQT_AVAILABLE = True
    except ImportError:
        PYQT_AVAILABLE = False

try:
    import wx
    WX_AVAILABLE = True
except ImportError:
    WX_AVAILABLE = False

try:
    import dearpygui.dearpygui as dpg
    DPG_AVAILABLE = True
except ImportError:
    DPG_AVAILABLE = False


def apply_rus_menu(widget, config=None):
    """
    Универсальная функция для применения русского меню к виджету.
    
    Автоматически определяет фреймворк и применяет меню ко всем
    текстовым виджетам внутри переданного контейнера.
    
    Args:
        widget: Виджет или контейнер (окно, фрейм, панель)
        config: Конфигурация меню (RusMenuConfig)
    
    Returns:
        bool: True если меню применено, False если ошибка
    """
    try:
        from .core import RusContextMenu
        
        # Проверяем Tkinter
        if TKINTER_AVAILABLE and isinstance(widget, (tk.Widget, tk.ttk.Widget)):
            return _apply_tkinter(widget, config)
        
        # Проверяем Qt
        elif PYQT_AVAILABLE and isinstance(widget, QtWidgets.QWidget):
            return _apply_qt(widget, config)
        
        # Проверяем wxPython
        elif WX_AVAILABLE and isinstance(widget, wx.Window):
            return _apply_wx(widget, config)
        
        # Проверяем Dear PyGui (по ID)
        elif DPG_AVAILABLE:
            try:
                if isinstance(widget, (int, str)) and dpg.does_item_exist(widget):
                    RusContextMenu(widget, config=config)
                    return True
            except:
                pass
        
        # Если ничего не подошло, пробуем рекурсивно обойти детей
        return _apply_recursive(widget, config)
        
    except Exception as e:
        print(f"Ошибка применения русского меню: {e}")
        return False


def _apply_tkinter(widget, config=None):
    """Применяет меню ко всем текстовым виджетам Tkinter"""
    from .core import RusContextMenu
    
    # Если виджет сам является текстовым
    if isinstance(widget, (tk.Entry, tk.Text, tk.Spinbox, tk.ttk.Entry, tk.ttk.Combobox)):
        RusContextMenu(widget, config=config)
        return True
    
    # Рекурсивно обходим детей
    try:
        for child in widget.winfo_children():
            _apply_tkinter(child, config)
        return True
    except:
        return False


def _apply_qt(widget, config=None):
    """Применяет меню ко всем текстовым виджетам Qt"""
    from .core import RusContextMenu
    
    text_types = (QtWidgets.QLineEdit, QtWidgets.QTextEdit, 
                  QtWidgets.QPlainTextEdit, QtWidgets.QComboBox)
    
    # Если виджет сам является текстовым
    if isinstance(widget, text_types):
        RusContextMenu(widget, config=config)
        return True
    
    # Рекурсивно обходим детей
    try:
        for child in widget.findChildren(QtWidgets.QWidget):
            _apply_qt(child, config)
        return True
    except:
        return False


def _apply_wx(widget, config=None):
    """Применяет меню ко всем текстовым виджетам wxPython"""
    from .core import RusContextMenu
    
    text_types = (wx.TextCtrl, wx.ComboBox)
    
    # Если виджет сам является текстовым
    if isinstance(widget, text_types):
        RusContextMenu(widget, config=config)
        return True
    
    # Рекурсивно обходим детей
    try:
        for child in widget.GetChildren():
            _apply_wx(child, config)
        return True
    except:
        return False


def _apply_recursive(widget, config=None):
    """
    Универсальная рекурсивная попытка применить меню
    """
    from .core import RusContextMenu
    
    # Пробуем применить меню к самому виджету
    try:
        RusContextMenu(widget, config=config)
        return True
    except:
        pass
    
    # Пробуем обойти детей
    try:
        if hasattr(widget, 'children'):
            for child in widget.children():
                _apply_recursive(child, config)
        elif hasattr(widget, 'winfo_children'):
            for child in widget.winfo_children():
                _apply_recursive(child, config)
        elif hasattr(widget, 'findChildren'):
            for child in widget.findChildren(type(widget)):
                _apply_recursive(child, config)
        elif hasattr(widget, 'GetChildren'):
            for child in widget.GetChildren():
                _apply_recursive(child, config)
        return True
    except:
        return False