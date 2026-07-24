"""
RusMenu - Русское контекстное меню для Python GUI
Версия: 4.0.0
"""

from .core import RusContextMenu, RusMenuConfig

# Импортируем бэкенды только если они доступны
try:
    from .tkinter_backend import RusTkinterMenu
except ImportError:
    pass

try:
    from .qt_backend import RusQtMenu
except ImportError:
    pass

try:
    from .wx_backend import RusWxMenu
except ImportError:
    pass

try:
    from .dpg_backend import RusDPGMenu
except ImportError:
    pass

__version__ = "4.0.0"
__author__ = "Скворцов Сергей Александрович"
__license__ = "Proprietary - Commercial with Free Use"

__all__ = [
    "RusContextMenu",
    "RusMenuConfig",
]