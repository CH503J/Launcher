#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :search_ui.py
# @Time      :2025/7/9 14:34
# @Author    :CH503J

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class SearchTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("这是搜索标签页（待实现搜索功能）"))
        self.setLayout(layout)