"""
Тесты для библиотеки RusMenu
"""

import unittest
import sys
import os

# Добавляем путь к библиотеке
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rusmenu import RusContextMenu, RusMenuConfig


class TestRusMenuConfig(unittest.TestCase):
    """Тесты для класса конфигурации"""
    
    def test_default_config(self):
        """Проверка конфигурации по умолчанию"""
        config = RusMenuConfig()
        
        self.assertEqual(config.font_family, "Segoe UI")
        self.assertEqual(config.font_size, 10)
        self.assertEqual(config.bg_color, "#f0f0f0")
        self.assertIn("copy", config.translations)
        self.assertIn("paste", config.shortcuts)
    
    def test_update_translation(self):
        """Проверка обновления переводов"""
        config = RusMenuConfig()
        config.update_translation("copy", "Копировать текст")
        self.assertEqual(config.translations["copy"], "Копировать текст")
    
    def test_update_shortcut(self):
        """Проверка обновления горячих клавиш"""
        config = RusMenuConfig()
        config.update_shortcut("copy", "Ctrl+Shift+C")
        self.assertEqual(config.shortcuts["copy"], "Ctrl+Shift+C")
    
    def test_theme_dark(self):
        """Проверка темной темы"""
        config = RusMenuConfig()
        config.set_theme_dark()
        self.assertEqual(config.bg_color, "#2d2d2d")
        self.assertEqual(config.fg_color, "#ffffff")
    
    def test_theme_light(self):
        """Проверка светлой темы"""
        config = RusMenuConfig()
        config.set_theme_light()
        self.assertEqual(config.bg_color, "#f0f0f0")
        self.assertEqual(config.fg_color, "#000000")
    
    def test_set_font(self):
        """Проверка установки шрифта"""
        config = RusMenuConfig()
        config.set_font("Arial", 14, "bold")
        self.assertEqual(config.font_family, "Arial")
        self.assertEqual(config.font_size, 14)
        self.assertEqual(config.font_weight, "bold")


class TestRusMenuImport(unittest.TestCase):
    """Тесты для импорта библиотеки"""
    
    def test_import(self):
        """Проверка импорта"""
        try:
            from rusmenu import RusContextMenu, RusMenuConfig
            self.assertTrue(True)
        except ImportError:
            self.fail("Не удалось импортировать RusMenu")
    
    def test_version(self):
        """Проверка версии"""
        import rusmenu
        self.assertTrue(hasattr(rusmenu, "__version__"))
        self.assertIsInstance(rusmenu.__version__, str)


# Пропускаем тесты с GUI, если они не нужны
class TestTkinterBackend(unittest.TestCase):
    """Тесты для Tkinter бэкенда"""
    
    @unittest.skipIf(not hasattr(sys, 'ps1'), "Не в интерактивном режиме")
    def test_tkinter_import(self):
        """Проверка импорта Tkinter"""
        try:
            import tkinter as tk
            self.assertTrue(True)
        except ImportError:
            self.skipTest("Tkinter не доступен")


if __name__ == "__main__":
    unittest.main()