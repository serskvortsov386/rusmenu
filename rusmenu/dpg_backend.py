"""
Dear PyGui backend for RusMenu
"""

import dearpygui.dearpygui as dpg


class RusDPGMenu:
    """
    Реализация русского контекстного меню для Dear PyGui
    
    Особенности:
    - Контекстное меню создается через dpg.add_popup
    - Использует колбэки для обработки действий
    - Поддерживает все стандартные текстовые виджеты DPG
    
    Поддерживает: mvInputText, mvInputTextMultiline, mvTextEditor
    """
    
    def __init__(self, widget_id, include_default=True, config=None):
        """
        Args:
            widget_id: ID виджета Dear PyGui
            include_default (bool): Добавлять стандартные пункты
            config (RusMenuConfig): Конфигурация меню
        """
        self.widget_id = widget_id
        self.config = config
        self.custom_commands = []
        self.menu_id = None
        self._shortcuts_setup = False
        
        # Проверяем, существует ли виджет
        if not dpg.does_item_exist(widget_id):
            raise ValueError(f"Виджет с ID '{widget_id}' не существует")
        
        # Получаем информацию о виджете
        self._widget_type = dpg.get_item_type(widget_id)
        
        # Создаем popup меню
        with dpg.popup(widget_id, mouse_button=dpg.mvMouseButton_Right, 
                       popup_pos="mouse_pos") as self.menu_id:
            if include_default:
                self.build_default_menu()
        
        # Применяем стили
        self._apply_styles()
        
        # Добавляем горячие клавиши (в DPG они настраиваются через хендлеры)
        self._setup_shortcuts()
    
    def _apply_styles(self):
        """Применяет стили к меню в Dear PyGui"""
        if not self.menu_id:
            return
        
        try:
            # Создаем тему для меню
            with dpg.theme() as theme_id:
                with dpg.theme_component(dpg.mvMenuItem):
                    dpg.add_theme_color(dpg.mvThemeCol_Text, 
                                       self.config.dpg_theme_color)
                    dpg.add_theme_color(dpg.mvThemeCol_Button, 
                                       self.config.dpg_bg_color)
                    dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, 
                                       self.config.dpg_hover_color)
                    dpg.add_theme_color(dpg.mvThemeCol_ButtonActive,
                                       self.config.dpg_hover_color)
            
            dpg.bind_item_theme(self.menu_id, theme_id)
        except:
            pass  # В старых версиях DPG может не работать
    
    def _setup_shortcuts(self):
        """Настраивает горячие клавиши в Dear PyGui"""
        if self._shortcuts_setup:
            return
        self._shortcuts_setup = True
        
        # Добавляем хендлеры клавиш для виджета
        with dpg.handler_registry() as handlers:
            # Ctrl+C
            dpg.add_key_down_handler(
                key=dpg.mvKey_C,
                callback=lambda: self.copy(),
                user_data=self.widget_id,
                modifiers=dpg.mvMod_Ctrl
            )
            
            # Ctrl+X
            dpg.add_key_down_handler(
                key=dpg.mvKey_X,
                callback=lambda: self.cut(),
                user_data=self.widget_id,
                modifiers=dpg.mvMod_Ctrl
            )
            
            # Ctrl+V
            dpg.add_key_down_handler(
                key=dpg.mvKey_V,
                callback=lambda: self.paste(),
                user_data=self.widget_id,
                modifiers=dpg.mvMod_Ctrl
            )
            
            # Ctrl+A
            dpg.add_key_down_handler(
                key=dpg.mvKey_A,
                callback=lambda: self.select_all(),
                user_data=self.widget_id,
                modifiers=dpg.mvMod_Ctrl
            )
            
            # Delete
            dpg.add_key_down_handler(
                key=dpg.mvKey_Delete,
                callback=lambda: self.delete(),
                user_data=self.widget_id
            )
            
            # Backspace
            dpg.add_key_down_handler(
                key=dpg.mvKey_Back,
                callback=lambda: self.delete(),
                user_data=self.widget_id
            )
    
    def build_default_menu(self):
        """Собирает стандартное меню для Dear PyGui"""
        trans = self.config.translations
        shortcuts = self.config.shortcuts
        
        # Отменить/Повторить
        dpg.add_menu_item(
            label=f"{trans['undo']}   {shortcuts['undo']}", 
            callback=lambda: self.undo()
        )
        dpg.add_menu_item(
            label=f"{trans['redo']}   {shortcuts['redo']}", 
            callback=lambda: self.redo()
        )
        dpg.add_separator()
        
        # Основные команды
        dpg.add_menu_item(
            label=f"{trans['cut']}   {shortcuts['cut']}", 
            callback=lambda: self.cut()
        )
        dpg.add_menu_item(
            label=f"{trans['copy']}   {shortcuts['copy']}", 
            callback=lambda: self.copy()
        )
        dpg.add_menu_item(
            label=f"{trans['paste']}   {shortcuts['paste']}", 
            callback=lambda: self.paste()
        )
        dpg.add_menu_item(
            label=f"{trans['delete']}   {shortcuts['delete']}", 
            callback=lambda: self.delete()
        )
        dpg.add_separator()
        
        dpg.add_menu_item(
            label=f"{trans['select_all']}   {shortcuts['select_all']}", 
            callback=lambda: self.select_all()
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
            label = f"{label}   {shortcut}"
        
        dpg.add_separator(parent=self.menu_id)
        dpg.add_menu_item(label=label, callback=command, parent=self.menu_id)
        self.custom_commands.append((label, command))
        
        # Добавляем горячую клавишу
        if shortcut:
            # Парсим shortcut и добавляем хендлер
            key_map = {
                'Ctrl+C': (dpg.mvKey_C, dpg.mvMod_Ctrl),
                'Ctrl+X': (dpg.mvKey_X, dpg.mvMod_Ctrl),
                'Ctrl+V': (dpg.mvKey_V, dpg.mvMod_Ctrl),
                'Ctrl+A': (dpg.mvKey_A, dpg.mvMod_Ctrl),
                'Ctrl+Shift+C': (dpg.mvKey_C, dpg.mvMod_Ctrl | dpg.mvMod_Shift),
                'Ctrl+Shift+X': (dpg.mvKey_X, dpg.mvMod_Ctrl | dpg.mvMod_Shift),
                'Ctrl+Shift+V': (dpg.mvKey_V, dpg.mvMod_Ctrl | dpg.mvMod_Shift),
                'Ctrl+Shift+A': (dpg.mvKey_A, dpg.mvMod_Ctrl | dpg.mvMod_Shift),
                'Del': (dpg.mvKey_Delete, 0),
                'Delete': (dpg.mvKey_Delete, 0),
                'Ctrl+Z': (dpg.mvKey_Z, dpg.mvMod_Ctrl),
                'Ctrl+Y': (dpg.mvKey_Y, dpg.mvMod_Ctrl),
            }
            
            if shortcut in key_map:
                key, modifiers = key_map[shortcut]
                with dpg.handler_registry():
                    dpg.add_key_down_handler(
                        key=key,
                        callback=lambda: command(),
                        user_data=self.widget_id,
                        modifiers=modifiers
                    )
        
        return self
    
    # --- Базовые функции для Dear PyGui ---
    def _get_text(self):
        """Получить текст из виджета"""
        # Определяем тип виджета и получаем текст
        widget_type = dpg.get_item_type(self.widget_id)
        
        if widget_type in ["mvAppItemType::mvInputText", 
                          "mvAppItemType::mvTextEditor",
                          "mvAppItemType::mvInputTextMultiline"]:
            return dpg.get_value(self.widget_id)
        else:
            # Пытаемся получить значение
            try:
                return dpg.get_value(self.widget_id)
            except:
                return ""
    
    def _set_text(self, text):
        """Установить текст в виджете"""
        widget_type = dpg.get_item_type(self.widget_id)
        
        if widget_type in ["mvAppItemType::mvInputText", 
                          "mvAppItemType::mvTextEditor",
                          "mvAppItemType::mvInputTextMultiline"]:
            dpg.set_value(self.widget_id, text)
        else:
            try:
                dpg.set_value(self.widget_id, text)
            except:
                pass
    
    def _get_selection(self):
        """Получить выделенный текст в Dear PyGui"""
        # В DPG сложнее получить выделение, но для InputText есть методы
        widget_type = dpg.get_item_type(self.widget_id)
        
        if widget_type in ["mvAppItemType::mvInputText", 
                          "mvAppItemType::mvInputTextMultiline"]:
            # DPG не предоставляет прямой доступ к выделению,
            # поэтому используем альтернативный подход
            try:
                # Пытаемся получить выделение через get_selection
                if hasattr(dpg, 'get_selection'):
                    return dpg.get_selection(self.widget_id) or ""
            except:
                pass
        
        # Возвращаем весь текст, если выделение не поддерживается
        return self._get_text()
    
    def copy(self):
        """Копировать выделенный текст"""
        text = self._get_selection()
        if text:
            dpg.set_clipboard_text(text)
    
    def cut(self):
        """Вырезать выделенный текст"""
        text = self._get_selection()
        if text:
            dpg.set_clipboard_text(text)
            self.delete()
    
    def paste(self):
        """Вставить текст из буфера обмена"""
        try:
            text = dpg.get_clipboard_text()
            if text:
                # Удаляем выделенное и вставляем
                self.delete()
                current_text = self._get_text()
                # Простая вставка в конец (для сложных случаев нужен cursor_pos)
                self._set_text(current_text + text)
        except:
            pass
    
    def delete(self):
        """Удалить выделенный текст"""
        # В DPG сложно удалить выделенный текст, поэтому
        # просто очищаем всё поле (для простоты)
        # В реальном приложении нужно использовать get_selection
        text = self._get_text()
        if text:
            self._set_text("")
    
    def select_all(self):
        """Выделить всё"""
        # В DPG select_all может не поддерживаться для всех виджетов
        try:
            if hasattr(dpg, 'select_all'):
                dpg.select_all(self.widget_id)
        except:
            pass
    
    def undo(self):
        """Отменить действие"""
        # В DPG может быть свой механизм undo/redo
        try:
            if hasattr(dpg, 'undo'):
                dpg.undo(self.widget_id)
        except:
            pass
    
    def redo(self):
        """Повторить действие"""
        try:
            if hasattr(dpg, 'redo'):
                dpg.redo(self.widget_id)
        except:
            pass