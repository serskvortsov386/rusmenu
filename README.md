# 🇷🇺 RusMenu - Русское контекстное меню для Python

**RusMenu** - это библиотека для Python, которая добавляет русскоязычное контекстное меню (правой кнопкой мыши) для текстовых полей ввода в различных GUI-фреймворках.

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-Commercial%20with%20Free%20Use-orange)](LICENSE)
[![PyPI version](https://badge.fury.io/py/rusmenu.svg)](https://badge.fury.io/py/rusmenu)
[![Downloads](https://pepy.tech/badge/rusmenu)](https://pepy.tech/project/rusmenu)

## ✨ Особенности

- 🇷🇺 **Полностью на русском языке** - все пункты меню переведены
- 🎨 **Кастомизация** - настройка шрифтов, цветов, стилей
- ⌨️ **Горячие клавиши** - поддержка Ctrl+C, Ctrl+X, Ctrl+V и других
- 🎯 **Универсальность** - работает с 4 популярными фреймворками
- 🔧 **Гибкость** - возможность добавлять свои пункты меню
- ⚡ **Легкость** - минимальное влияние на производительность

## 🚀 Поддерживаемые фреймворки

| Фреймворк | Статус | Установка |
|-----------|--------|-----------|
| **Tkinter** | ✅ Полная поддержка | Встроен в Python |
| **PyQt5 / PySide6** | ✅ Полная поддержка | `pip install PyQt5` |
| **wxPython** | ✅ Полная поддержка | `pip install wxPython` |
| **Dear PyGui** | ✅ Полная поддержка | `pip install dearpygui` |

## 📦 Установка

```bash
pip install rusmenu

Или установка из исходников:

bash
git clone https://github.com/serskvortsov386/rusmenu.git
cd rusmenu
pip install -e .


Быстрый старт:

1) Tkinter
python

import tkinter as tk
from rusmenu import RusContextMenu

root = tk.Tk()
entry = tk.Entry(root)
entry.pack()
entry.insert(0, "Кликни правой кнопкой")

# Добавляем русское меню
RusContextMenu(entry)

root.mainloop()


2) PyQt5
python

from PyQt5 import QtWidgets
from rusmenu import RusContextMenu

app = QtWidgets.QApplication([])
window = QtWidgets.QMainWindow()
text_edit = QtWidgets.QTextEdit(window)

# Добавляем русское меню
RusContextMenu(text_edit)

window.show()
app.exec()

3) wxPython
python

import wx
from rusmenu import RusContextMenu

app = wx.App()
frame = wx.Frame(None, title="RusMenu")
text = wx.TextCtrl(frame, style=wx.TE_MULTILINE)

# Добавляем русское меню
RusContextMenu(text)

frame.Show()
app.MainLoop()


4) Dear PyGui
python

import dearpygui.dearpygui as dpg
from rusmenu import RusContextMenu

dpg.create_context()

with dpg.window(label="RusMenu"):
    input_text = dpg.add_input_text(default_value="Кликни правой кнопкой")
    RusContextMenu(input_text)  # Передаем ID виджета

dpg.create_viewport()
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()


5) Кастомизация
python

from rusmenu import RusContextMenu, RusMenuConfig

# Настраиваем внешний вид
config = RusMenuConfig()
config.font_family = "Segoe UI"
config.font_size = 12
config.bg_color = "#2d2d2d"  # Темная тема
config.fg_color = "#ffffff"
config.hover_bg = "#3a6ea5"

# Создаем меню с кастомной конфигурацией
menu = RusContextMenu(widget, config=config)

# Добавляем свои пункты
def custom_action():
    print("Сработал кастомный пункт!")

menu.add_command("🔍 Поиск", custom_action, shortcut="Ctrl+Shift+F")

📜 Лицензия
Эта библиотека распространяется по двойной лицензии:
Бесплатно для некоммерческого использования, образовательных целей и открытых проектов
Коммерческое использование требует покупки лицензии
Подробнее: LICENSE

🤝 Как поддержать проект
⭐ Поставьте звезду на GitHub
🐛 Сообщайте об ошибках в Issues
💡 Предлагайте новые идеи
📝 Пишите документацию и примеры

📧 Контакты
Автор: Скворцов Сергей Александрович
Email: ser.skvortsov.386@gmail.com
Город: Чебоксары
GitHub: https://github.com/serskvortsov386

🙏 Благодарности
Всем пользователям, которые помогают тестировать библиотеку
Сообществу Python за вдохновение. 

