"""
wxPython backend for RusMenu
"""

import wx


class RusWxMenu:
    """
    Реализация русского контекстного меню для wxPython
    
    Поддерживает: TextCtrl, ComboBox, TextAreaBase
    """
    
    def __init__(self, widget, include_default=True, config=None):
        self.widget = widget
        self.config = config
        self.custom_items = []
        self._shortcuts_setup = False
        
        # Создаем меню
        self.menu = wx.Menu()
        
        if include_default:
            self.build_default_menu()
        
        # Привязываем событие правого клика
        widget.Bind(wx.EVT_CONTEXT_MENU, self.show_menu)
        
        # Добавляем горячие клавиши
        self._setup_shortcuts()
        
        # Применяем стили
        self._apply_styles()
    
    def _apply_styles(self):
        """Применяет стили к меню (wxPython)"""
        try:
            # Устанавливаем шрифт
            font = wx.Font(
                self.config.font_size,
                wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_NORMAL if self.config.font_weight == "normal" else wx.FONTWEIGHT_BOLD,
                False,
                self.config.font_family
            )
            self.menu.SetFont(font)
            
            # Цвета для wxPython (зависит от версии)
            if hasattr(self.menu, 'SetBackgroundColour'):
                self.menu.SetBackgroundColour(wx.Colour(self.config.bg_color))
            if hasattr(self.menu, 'SetForegroundColour'):
                self.menu.SetForegroundColour(wx.Colour(self.config.fg_color))
        except:
            pass  # Некоторые версии wxPython могут не поддерживать все методы
    
    def _setup_shortcuts(self):
        """Настраивает горячие клавиши для виджета"""
        if self._shortcuts_setup:
            return
        self._shortcuts_setup = True
        
        widget = self.widget
        widget.Bind(wx.EVT_KEY_DOWN, self._on_key_down)
    
    def _on_key_down(self, event):
        """
        Обработчик нажатия клавиш для горячих клавиш
        """
        key_code = event.GetKeyCode()
        modifiers = event.GetModifiers()
        
        # Проверяем Ctrl+C
        if key_code == ord('C') and modifiers == wx.MOD_CONTROL:
            self.copy()
            return
        # Ctrl+X
        elif key_code == ord('X') and modifiers == wx.MOD_CONTROL:
            self.cut()
            return
        # Ctrl+V
        elif key_code == ord('V') and modifiers == wx.MOD_CONTROL:
            self.paste()
            return
        # Ctrl+A
        elif key_code == ord('A') and modifiers == wx.MOD_CONTROL:
            self.select_all()
            return
        # Delete
        elif key_code == wx.WXK_DELETE:
            self.delete()
            return
        
        event.Skip()
    
    def build_default_menu(self):
        """Собирает стандартное меню"""
        trans = self.config.translations
        shortcuts = self.config.shortcuts
        
        # Отменить/Повторить
        self.menu.Append(wx.ID_UNDO, f"{trans['undo']}\t{shortcuts['undo']}")
        self.menu.Append(wx.ID_REDO, f"{trans['redo']}\t{shortcuts['redo']}")
        self.menu.AppendSeparator()
        
        # Основные команды
        self.menu.Append(wx.ID_CUT, f"{trans['cut']}\t{shortcuts['cut']}")
        self.menu.Append(wx.ID_COPY, f"{trans['copy']}\t{shortcuts['copy']}")
        self.menu.Append(wx.ID_PASTE, f"{trans['paste']}\t{shortcuts['paste']}")
        self.menu.Append(wx.ID_DELETE, f"{trans['delete']}\t{shortcuts['delete']}")
        self.menu.AppendSeparator()
        
        self.menu.Append(wx.ID_SELECTALL, f"{trans['select_all']}\t{shortcuts['select_all']}")
        
        # Привязываем события к стандартным ID
        self.widget.Bind(wx.EVT_MENU, lambda e: self.undo(), id=wx.ID_UNDO)
        self.widget.Bind(wx.EVT_MENU, lambda e: self.redo(), id=wx.ID_REDO)
        self.widget.Bind(wx.EVT_MENU, lambda e: self.cut(), id=wx.ID_CUT)
        self.widget.Bind(wx.EVT_MENU, lambda e: self.copy(), id=wx.ID_COPY)
        self.widget.Bind(wx.EVT_MENU, lambda e: self.paste(), id=wx.ID_PASTE)
        self.widget.Bind(wx.EVT_MENU, lambda e: self.delete(), id=wx.ID_DELETE)
        self.widget.Bind(wx.EVT_MENU, lambda e: self.select_all(), id=wx.ID_SELECTALL)
    
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
        
        self.menu.AppendSeparator()
        custom_id = wx.NewIdRef()
        self.menu.Append(custom_id, label)
        self.widget.Bind(wx.EVT_MENU, lambda e: command(), id=custom_id)
        self.custom_items.append((label, command))
        
        # Добавляем горячую клавишу через акселератор
        if shortcut:
            # Создаем акселератор для виджета
            accel_table = wx.AcceleratorTable([
                (self._parse_shortcut(shortcut), custom_id)
            ])
            self.widget.SetAcceleratorTable(accel_table)
        
        return self
    
    def _parse_shortcut(self, shortcut):
        """
        Парсит строку горячей клавиши в код wx
        
        Примеры:
            "Ctrl+C" -> wx.ACCEL_CTRL | ord('C')
            "Ctrl+Shift+C" -> wx.ACCEL_CTRL | wx.ACCEL_SHIFT | ord('C')
        """
        modifiers = 0
        key = None
        
        parts = shortcut.split('+')
        for part in parts:
            if part.lower() == 'ctrl':
                modifiers |= wx.ACCEL_CTRL
            elif part.lower() == 'shift':
                modifiers |= wx.ACCEL_SHIFT
            elif part.lower() == 'alt':
                modifiers |= wx.ACCEL_ALT
            else:
                if len(part) == 1:
                    key = ord(part.upper())
        
        if key is None:
            return 0
        
        return wx.AcceleratorEntry(modifiers, key)
    
    def show_menu(self, event):
        """Показывает меню в месте клика"""
        # Получаем позицию мыши
        pos = self.widget.ScreenToClient(wx.GetMousePosition())
        self.widget.PopupMenu(self.menu, pos)
    
    # --- Базовые функции для wxPython ---
    def copy(self):
        """Копировать выделенный текст"""
        if hasattr(self.widget, 'Copy'):
            self.widget.Copy()
        else:
            text = self._get_selection()
            if text and wx.TheClipboard.Open():
                wx.TheClipboard.SetData(wx.TextDataObject(text))
                wx.TheClipboard.Close()
    
    def cut(self):
        """Вырезать выделенный текст"""
        if hasattr(self.widget, 'Cut'):
            self.widget.Cut()
        else:
            text = self._get_selection()
            if text:
                self.copy()
                self.delete()
    
    def paste(self):
        """Вставить текст из буфера обмена"""
        if hasattr(self.widget, 'Paste'):
            self.widget.Paste()
        else:
            if wx.TheClipboard.Open():
                data = wx.TextDataObject()
                if wx.TheClipboard.GetData(data):
                    text = data.GetText()
                    if text:
                        self.delete()
                        self.widget.WriteText(text)
                wx.TheClipboard.Close()
    
    def delete(self):
        """Удалить выделенный текст"""
        if hasattr(self.widget, 'RemoveSelected'):
            self.widget.RemoveSelected()
        elif hasattr(self.widget, 'DeleteSelected'):
            self.widget.DeleteSelected()
        else:
            # Универсальный способ
            if hasattr(self.widget, 'GetSelection'):
                start, end = self.widget.GetSelection()
                if start != end:
                    self.widget.Remove(start, end)
    
    def select_all(self):
        """Выделить весь текст"""
        if hasattr(self.widget, 'SelectAll'):
            self.widget.SelectAll()
        else:
            self.widget.SetSelection(0, -1)
    
    def undo(self):
        """Отменить действие"""
        if hasattr(self.widget, 'Undo'):
            self.widget.Undo()
    
    def redo(self):
        """Повторить действие"""
        if hasattr(self.widget, 'Redo'):
            self.widget.Redo()
    
    def _get_selection(self):
        """Получить выделенный текст (для нестандартных виджетов)"""
        if hasattr(self.widget, 'GetStringSelection'):
            return self.widget.GetStringSelection()
        elif hasattr(self.widget, 'GetSelectedText'):
            return self.widget.GetSelectedText()
        elif hasattr(self.widget, 'GetSelection'):
            start, end = self.widget.GetSelection()
            if start != end and hasattr(self.widget, 'GetValue'):
                return self.widget.GetValue()[start:end]
        return ""