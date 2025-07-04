#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :launcher_ui.py
# @Time      :2025/7/4 15:01
# @Author    :CH503J


from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QLabel, QTabWidget
)


class LauncherTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel("这是服务启停页面!!!!!!!!!!!!!!")
        layout.addWidget(label)
        self.setLayout(layout)
