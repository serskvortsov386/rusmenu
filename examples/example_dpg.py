"""
Пример использования RusMenu с Dear PyGui
"""

import dearpygui.dearpygui as dpg
from rusmenu import RusContextMenu, RusMenuConfig


def main():
    # Инициализация DPG
    dpg.create_context()
    
    # Создаем окно
    with dpg.window(label="RusMenu - Dear PyGui Example", 
                    width=600, height=500, pos=(0, 0)):
        
        # Заголовок
        dpg.add_text("Кликни правой кнопкой на любом поле ввода", 
                     color=(100, 200, 100), indent=10)
        dpg.add_spacer(height=10)
        
        # Поле ввода
        dpg.add_text("Поле ввода (InputText):", indent=10)
        input_text = dpg.add_input_text(
            default_value="Пример текста для тестирования",
            width=580,
            indent=10
        )
        
        dpg.add_spacer(height=10)
        
        # Многострочное поле
        dpg.add_text("Многострочное поле (InputTextMultiline):", indent=10)
        multi_text = dpg.add_input_text(
            default_value="Многострочное поле\nс русским контекстным меню",
            multiline=True,
            height=80,
            width=580,
            indent=10
        )
        
        dpg.add_spacer(height=10)
        
        # Поле с паролем
        dpg.add_text("Поле с паролем (InputText):", indent=10)
        password_text = dpg.add_input_text(
            default_value="secret_password",
            password=True,
            width=580,
            indent=10
        )
        
        dpg.add_spacer(height=10)
        
        # Текстовый редактор
        dpg.add_text("Текстовый редактор (TextEditor):", indent=10)
        editor = dpg.add_text_editor(
            default_value="Расширенный текстовый редактор\nс поддержкой русского меню",
            width=580,
            height=120,
            indent=10
        )
        
        # Применяем конфигурацию
        config = RusMenuConfig()
        config.dpg_theme_color = (255, 255, 255, 255)
        config.dpg_bg_color = (40, 40, 40, 255)
        config.dpg_hover_color = (60, 100, 200, 255)
        
        # Создаем меню для каждого виджета
        menu1 = RusContextMenu(input_text, config=config)
        menu2 = RusContextMenu(multi_text, config=config)
        menu3 = RusContextMenu(password_text, config=config)
        menu4 = RusContextMenu(editor, config=config)
        
        # Добавляем кастомные пункты
        
        # Для input_text
        def show_info():
            text = dpg.get_value(input_text)
            dpg.set_value(info_text, f"Текст: {text[:30]}...")
        
        menu1.add_command("ℹ️ Информация", show_info, shortcut="Ctrl+I")
        
        # Для multi_text
        def count_words():
            text = dpg.get_value(multi_text)
            words = len(text.split())
            dpg.set_value(info_text, f"Количество слов: {words}")
        
        menu2.add_command("📊 Статистика", count_words, shortcut="Ctrl+Shift+W")
        
        # Для password_text
        def toggle_password():
            current_password = dpg.get_item_configuration(password_text)["password"]
            dpg.configure_item(password_text, password=not current_password)
        
        menu3.add_command("👁️ Показать пароль", toggle_password, shortcut="Ctrl+P")
        
        # Для editor
        def get_stats():
            text = dpg.get_value(editor)
            chars = len(text)
            words = len(text.split())
            lines = len(text.split('\n'))
            dpg.set_value(info_text, f"Символов: {chars} | Слов: {words} | Строк: {lines}")
        
        menu4.add_command("📊 Статистика текста", get_stats, shortcut="Ctrl+Shift+S")
        
        # Информационное поле
        dpg.add_spacer(height=10)
        info_text = dpg.add_text("Информация будет здесь", color=(100, 200, 100), indent=10)
    
    # Настройка и запуск
    dpg.create_viewport(title="RusMenu + Dear PyGui", width=620, height=550)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    main()