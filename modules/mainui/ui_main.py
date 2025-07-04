#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :ui_main.py
# @Time      :2025/7/4 15:16
# @Author    :CH503J


from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QLabel, QTabWidget
)
import sys
from modules.settings.settings_ui import AboutTab
from modules.launcher.launcher_ui import LauncherTab



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Launcher 主界面")
        self.setGeometry(100, 100, 800, 600)

        # 创建标签页控件
        tabs = QTabWidget()
        tabs.addTab(LauncherTab(), "启停")
        tabs.addTab(AboutTab(), "关于")

        # 设置中央窗口部件
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(tabs)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)


# 仅当直接运行此文件时，启动窗口（用于测试）
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())