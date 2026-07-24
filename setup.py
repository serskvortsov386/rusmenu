"""
Setup file for rusmenu library
Автор: Скворцов Сергей Александрович (Чебоксары)
Email: ser.skvortsov.386@gmail.com
"""

from setuptools import setup, find_packages
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().splitlines()
    requirements = [r for r in requirements if r and not r.startswith("#")]

setup(
    name="rusmenu",
    version="4.0.0",
    author="Скворцов Сергей Александрович",
    author_email="ser.skvortsov.386@gmail.com",
    description="Русское контекстное меню для Python GUI (Tkinter, PyQt5, wxPython, Dear PyGui)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/serskvortsov386/rusmenu",
    project_urls={
        "Bug Reports": "https://github.com/serskvortsov386/rusmenu/issues",
        "Source": "https://github.com/serskvortsov386/rusmenu",
        "Documentation": "https://github.com/serskvortsov386/rusmenu#readme",
    },
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Desktop Environment",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
    ],
    python_requires=">=3.7",
    install_requires=[],
    extras_require={
        "qt": ["PyQt5>=5.15.0"],
        "qt6": ["PySide6>=6.0.0"],
        "wx": ["wxPython>=4.2.0"],
        "dpg": ["dearpygui>=1.10.0"],
        "all": [
            "PyQt5>=5.15.0",
            "wxPython>=4.2.0",
            "dearpygui>=1.10.0",
        ],
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=6.0.0",
            "build>=0.10.0",
            "twine>=4.0.0",
        ],
    },
    keywords="gui tkinter pyqt pyside wxpython dearpygui context-menu russian",
    license="Proprietary - Commercial with Free Use",
    include_package_data=True,
    zip_safe=False,
)