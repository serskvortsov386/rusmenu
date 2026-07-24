import tkinter as tk
from rusmenu import RusContextMenu, RusMenuConfig

def main():
    root = tk.Tk()
    root.title("RusMenu - Tkinter Example")
    root.geometry("400x300")
    
    # Создаем поле ввода
    label = tk.Label(root, text="Кликни правой кнопкой:")
    label.pack(pady=10)
    
    entry = tk.Entry(root, width=40)
    entry.pack(pady=5)
    entry.insert(0, "Пример текста для тестирования")
    
    # Многострочное поле
    text = tk.Text(root, height=5, width=40)
    text.pack(pady=10)
    text.insert("1.0", "Многострочное поле\nс русским меню")
    
    # Применяем меню с кастомной конфигурацией
    config = RusMenuConfig()
    config.font_family = "Arial"
    config.font_size = 11
    config.bg_color = "#f5f5f5"
    config.hover_bg = "#4a90d9"
    
    menu1 = RusContextMenu(entry, config=config)
    menu2 = RusContextMenu(text, config=config)
    
    # Добавляем кастомный пункт
    def show_info():
        print("Текст в поле:", entry.get())
    
    menu1.add_command("ℹ️ Информация", show_info, shortcut="Ctrl+I")
    
    def clear_text():
        text.delete("1.0", tk.END)
    
    menu2.add_command("🗑️ Очистить", clear_text, shortcut="Ctrl+Shift+C")
    
    root.mainloop()

if __name__ == "__main__":
    main()