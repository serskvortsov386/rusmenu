"""
Core module for RusMenu
"""

import sys
import warnings

from .config import RusMenuConfig

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


class RusContextMenu:
    """
    Главный класс-фабрика. Автоматически определяет фреймворк
    и создает соответствующее меню.
    """
    
    def __new__(cls, widget, include_default=True, config=None):
        """
        Создает экземпляр меню в зависимости от типа виджета
        
        :param widget: Виджет (для DPG передается ID виджета)
        :param include_default: Добавлять стандартные пункты
        :param config: Конфигурация меню
        """
        config = config or RusMenuConfig()
        
        # Проверяем Dear PyGui (передаем ID, а не объект)
        if DPG_AVAILABLE:
            try:
                if isinstance(widget, (int, str)) and dpg.does_item_exist(widget):
                    from .dpg_backend import RusDPGMenu
                    return RusDPGMenu(widget, include_default, config)
            except:
                pass
        
        # Проверяем Tkinter
        if TKINTER_AVAILABLE and isinstance(widget, (tk.Widget, tk.ttk.Widget)):
            from .tkinter_backend import RusTkinterMenu
            return RusTkinterMenu(widget, include_default, config)
        
        # Проверяем Qt
        elif PYQT_AVAILABLE and isinstance(widget, QtWidgets.QWidget):
            from .qt_backend import RusQtMenu
            return RusQtMenu(widget, include_default, config)
        
        # Проверяем wxPython
        elif WX_AVAILABLE and isinstance(widget, wx.Window):
            from .wx_backend import RusWxMenu
            return RusWxMenu(widget, include_default, config)
        
        raise TypeError(f"Неподдерживаемый тип виджета: {type(widget)}")


# Экспортируем утилиты
__all__ = ["RusContextMenu", "RusMenuConfig"]