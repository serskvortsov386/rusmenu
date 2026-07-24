"""
Пример использования RusMenu со всеми фреймворками
"""

import sys

def demo_tkinter():
    try:
        import tkinter as tk
        from rusmenu import RusContextMenu
        
        root = tk.Tk()
        root.title("Tkinter Demo")
        root.geometry("300x100")
        
        entry = tk.Entry(root)
        entry.pack(pady=30)
        entry.insert(0, "Tkinter поле")
        
        RusContextMenu(entry)
        
        root.mainloop()
    except Exception as e:
        print(f"Tkinter demo error: {e}")

def demo_qt():
    try:
        from PyQt5 import QtWidgets
        from rusmenu import RusContextMenu
        
        app = QtWidgets.QApplication([])
        window = QtWidgets.QMainWindow()
        window.setWindowTitle("Qt Demo")
        
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(widget)
        
        text = QtWidgets.QLineEdit()
        text.setText("Qt поле")
        layout.addWidget(text)
        
        window.setCentralWidget(widget)
        window.resize(300, 100)
        
        RusContextMenu(text)
        
        window.show()
        app.exec()
    except Exception as e:
        print(f"Qt demo error: {e}")

def demo_wx():
    try:
        import wx
        from rusmenu import RusContextMenu
        
        app = wx.App()
        frame = wx.Frame(None, title="wxPython Demo", size=(300, 100))
        
        text = wx.TextCtrl(frame)
        text.SetValue("wxPython поле")
        
        RusContextMenu(text)
        
        frame.Show()
        app.MainLoop()
    except Exception as e:
        print(f"wxPython demo error: {e}")

def demo_dpg():
    try:
        import dearpygui.dearpygui as dpg
        from rusmenu import RusContextMenu
        
        dpg.create_context()
        
        with dpg.window(label="Dear PyGui Demo", width=300, height=100):
            input_text = dpg.add_input_text(default_value="DPG поле")
            RusContextMenu(input_text)
        
        dpg.create_viewport(title="DPG Demo")
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()
    except Exception as e:
        print(f"Dear PyGui demo error: {e}")

if __name__ == "__main__":
    print("Выберите фреймворк для демонстрации:")
    print("1. Tkinter")
    print("2. PyQt5")
    print("3. wxPython")
    print("4. Dear PyGui")
    
    choice = input("Ваш выбор (1-4): ").strip()
    
    if choice == "1":
        demo_tkinter()
    elif choice == "2":
        demo_qt()
    elif choice == "3":
        demo_wx()
    elif choice == "4":
        demo_dpg()
    else:
        print("Неверный выбор")