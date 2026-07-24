"""
RusMenu - Русское контекстное меню для Python GUI
"""

from .core import RusContextMenu, RusMenuConfig
from .tkinter_backend import RusTkinterMenu
from .qt_backend import RusQtMenu
from .wx_backend import RusWxMenu
from .dpg_backend import RusDPGMenu

__version__ = "4.0.0"
__all__ = [
    "RusContextMenu",
    "RusMenuConfig",
    "RusTkinterMenu",
    "RusQtMenu",
    "RusWxMenu",
    "RusDPGMenu",
]