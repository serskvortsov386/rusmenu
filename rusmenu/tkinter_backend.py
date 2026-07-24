"""
Tkinter backend for RusMenu
"""

import tkinter as tk
from tkinter import ttk, TclError


class RusTkinterMenu:
    """
    Реализация русского контекстного меню для Tkinter
    
    Поддерживает: Entry, Text, Spinbox, Combobox
    """
    
    def __init__(self, widget, include_default=True, config=None):
        self.widget = widget
        self.config = config
        self.menu = tk.Menu(widget, tearoff=0)
        self.custom_commands = []
        self._shortcuts_bound = False
        
        # Применяем стили
        try:
            self.menu.configure(
                bg=self.config.bg_color,
                fg=self.config.fg_color,
                activebackground=self.config.hover_bg,
                activeforeground=self.config.hover_fg,
                font=(self.config.font_family, self.config.font_size)
            )
        except:
            pass
        
        if include_default:
            self.build_default_menu()
        
        # Привязываем события
        widget.bind("<Button-3>", self.show_menu)
        widget.bind("<Button-2>", self.show_menu, add=True)
        
        # Добавляем горячие клавиши
        self._bind_shortcuts()
    
    def _bind_shortcuts(self):
        """Привязывает горячие клавиши к виджету"""
        if self._shortcuts_bound:
            return
        self._shortcuts_bound = True
        
        widget = self.widget
        shortcuts = {
            "<Control-c>": self.copy,
            "<Control-C>": self.copy,
            "<Control-x>": self.cut,
            "<Control-X>": self.cut,
            "<Control-v>": self.paste,
            "<Control-V>": self.paste,
            "<Control-a>": self.select_all,
            "<Control-A>": self.select_all,
            "<Delete>": self.delete,
            "<BackSpace>": self.delete,
        }
        
        for key, func in shortcuts.items():
            try:
                widget.bind(key, lambda e, f=func: f())
            except:
                pass
    
    def build_default_menu(self):
        """Собирает стандартное меню"""
        trans = self.config.translations
        shortcuts = self.config.shortcuts
        
        # Отменить/Повторить
        try:
            self.menu.add_command(
                label=f"{trans['undo']}\t{shortcuts['undo']}", 
                command=self.undo
            )
            self.menu.add_command(
                label=f"{trans['redo']}\t{shortcuts['redo']}", 
                command=self.redo
            )
            self.menu.add_separator()
        except:
            pass
        
        # Основные команды
        self.menu.add_command(
            label=f"{trans['cut']}\t{shortcuts['cut']}", 
            command=self.cut
        )
        self.menu.add_command(
            label=f"{trans['copy']}\t{shortcuts['copy']}", 
            command=self.copy
        )
        self.menu.add_command(
            label=f"{trans['paste']}\t{shortcuts['paste']}", 
            command=self.paste
        )
        self.menu.add_command(
            label=f"{trans['delete']}\t{shortcuts['delete']}", 
            command=self.delete
        )
        self.menu.add_separator()
        self.menu.add_command(
            label=f"{trans['select_all']}\t{shortcuts['select_all']}", 
            command=self.select_all
        )
    
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
        self.menu.add_separator()
        self.menu.add_command(label=label, command=command)
        self.custom_commands.append((label, command))
        return self
    
    def show_menu(self, event):
        """Показывает меню в месте клика"""
        try:
            self.menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.menu.grab_release()
    
    # --- Базовые функции ---
    def _get_selection(self):
        """Получить выделенный текст"""
        try:
            if isinstance(self.widget, (tk.Entry, tk.Spinbox, tk.ttk.Entry, tk.ttk.Combobox)):
                if self.widget.selection_present():
                    return self.widget.selection_get()
                return ""
            else:
                if self.widget.tag_ranges("sel"):
                    return self.widget.selection_get()
                return ""
        except TclError:
            return ""
    
    def copy(self):
        """Копировать выделенный текст"""
        text = self._get_selection()
        if text:
            self.widget.clipboard_clear()
            self.widget.clipboard_append(text)
    
    def cut(self):
        """Вырезать выделенный текст"""
        text = self._get_selection()
        if text:
            self.copy()
            self.delete()
    
    def paste(self):
        """Вставить текст из буфера обмена"""
        try:
            text = self.widget.clipboard_get()
            if text:
                self.delete()
                self.widget.insert(tk.INSERT, text)
        except TclError:
            pass
    
    def delete(self):
        """Удалить выделенный текст"""
        try:
            if isinstance(self.widget, (tk.Entry, tk.Spinbox, tk.ttk.Entry, tk.ttk.Combobox)):
                if self.widget.selection_present():
                    self.widget.delete(tk.SEL_FIRST, tk.SEL_LAST)
            else:
                if self.widget.tag_ranges("sel"):
                    self.widget.delete(tk.SEL_FIRST, tk.SEL_LAST)
        except TclError:
            pass
    
    def select_all(self):
        """Выделить весь текст"""
        try:
            self.widget.focus_set()
            if isinstance(self.widget, (tk.Entry, tk.Spinbox, tk.ttk.Entry, tk.ttk.Combobox)):
                self.widget.select_range(0, tk.END)
            else:
                self.widget.tag_add("sel", "1.0", tk.END)
        except TclError:
            pass
    
    def undo(self):
        """Отменить действие (базовая реализация)"""
        try:
            self.widget.event_generate("<<Undo>>")
        except:
            pass
    
    def redo(self):
        """Повторить действие (базовая реализация)"""
        try:
            self.widget.event_generate("<<Redo>>")
        except:
            pass