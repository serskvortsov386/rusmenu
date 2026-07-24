"""
Пример использования RusMenu с wxPython
"""

import wx
from rusmenu import RusContextMenu, RusMenuConfig


class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="RusMenu - wxPython Example", 
                        size=(600, 500))
        
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.SetSpacing(15)
        
        # Заголовок
        label = wx.StaticText(panel, label="Кликни правой кнопкой на любом поле ввода")
        font = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        label.SetFont(font)
        sizer.Add(label, 0, wx.ALL, 10)
        
        # Поле ввода
        sizer.Add(wx.StaticText(panel, label="Поле ввода (TextCtrl):"), 0, wx.LEFT, 10)
        self.text_ctrl = wx.TextCtrl(panel)
        self.text_ctrl.SetValue("Пример текста для тестирования")
        sizer.Add(self.text_ctrl, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        
        # Многострочное поле
        sizer.Add(wx.StaticText(panel, label="Многострочное поле (TextCtrl):"), 0, wx.LEFT | wx.TOP, 10)
        self.multi_text = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        self.multi_text.SetValue("Многострочное поле\nс русским контекстным меню")
        sizer.Add(self.multi_text, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        
        # Поле с паролем
        sizer.Add(wx.StaticText(panel, label="Поле с паролем (TextCtrl):"), 0, wx.LEFT | wx.TOP, 10)
        self.password_text = wx.TextCtrl(panel, style=wx.TE_PASSWORD)
        self.password_text.SetValue("secret_password")
        sizer.Add(self.password_text, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        
        # Выпадающий список
        sizer.Add(wx.StaticText(panel, label="Выпадающий список (ComboBox):"), 0, wx.LEFT | wx.TOP, 10)
        self.combo = wx.ComboBox(panel, choices=["Пункт 1", "Пункт 2", "Пункт 3", "Пункт 4"])
        self.combo.SetValue("Выберите пункт")
        sizer.Add(self.combo, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        
        panel.SetSizer(sizer)
        
        # Применяем конфигурацию
        config = RusMenuConfig()
        config.font_family = "Segoe UI"
        config.font_size = 11
        config.bg_color = "#f5f5f5"
        config.hover_bg = "#4a90d9"
        config.hover_fg = "#ffffff"
        
        # Создаем меню для каждого виджета
        menu1 = RusContextMenu(self.text_ctrl, config=config)
        menu2 = RusContextMenu(self.multi_text, config=config)
        menu3 = RusContextMenu(self.password_text, config=config)
        menu4 = RusContextMenu(self.combo, config=config)
        
        # Добавляем кастомные пункты
        
        # Для text_ctrl
        def show_info():
            wx.MessageBox(f"Текст: {self.text_ctrl.GetValue()}", "Информация")
        menu1.add_command("ℹ️ Информация", show_info, shortcut="Ctrl+I")
        
        # Для multi_text
        def count_words():
            text = self.multi_text.GetValue()
            words = len(text.split())
            wx.MessageBox(f"Количество слов: {words}", "Статистика")
        menu2.add_command("📊 Статистика", count_words, shortcut="Ctrl+Shift+W")
        
        # Для password_text
        def toggle_password():
            style = self.password_text.GetWindowStyle()
            if style & wx.TE_PASSWORD:
                self.password_text.SetWindowStyle(style & ~wx.TE_PASSWORD)
            else:
                self.password_text.SetWindowStyle(style | wx.TE_PASSWORD)
        menu3.add_command("👁️ Показать пароль", toggle_password, shortcut="Ctrl+P")
        
        # Для combo
        def show_selection():
            wx.MessageBox(f"Выбрано: {self.combo.GetValue()}", "Выбор")
        menu4.add_command("ℹ️ Показать выбор", show_selection, shortcut="Ctrl+Shift+S")


class MyApp(wx.App):
    def OnInit(self):
        frame = MainFrame()
        frame.Show()
        return True


def main():
    app = MyApp()
    app.MainLoop()


if __name__ == "__main__":
    main()