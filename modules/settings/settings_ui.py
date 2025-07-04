#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :settings_ui.py
# @Time      :2025/7/4 15:32
# @Author    :CH503J


import json
import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QGroupBox, QFormLayout,
    QLineEdit, QPushButton, QHBoxLayout, QFileDialog
)

SETTINGS_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "config", "settings.json")

class AboutTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # 关于信息区域
        about_group = QGroupBox("关于软件")
        about_layout = QVBoxLayout()
        about_layout.addWidget(QLabel("软件名称：Launcher"))
        about_layout.addWidget(QLabel("版本号：v1.0.0"))
        about_layout.addWidget(QLabel("开发者：你自己 😄"))
        about_group.setLayout(about_layout)

        # 设置项区域
        settings_group = QGroupBox("软件设置")
        settings_layout = QFormLayout()

        # 服务路径输入框和选择按钮
        path_layout = QHBoxLayout()
        self.service_path_input = QLineEdit()
        self.service_path_input.setPlaceholderText("例如：C:/Games/MyGame")
        self.select_path_button = QPushButton("选择路径")
        self.select_path_button.clicked.connect(self.select_path)
        path_layout.addWidget(self.service_path_input)
        path_layout.addWidget(self.select_path_button)

        settings_layout.addRow("游戏根目录：", path_layout)

        # 保存按钮
        self.save_button = QPushButton("保存设置")
        self.save_button.clicked.connect(self.save_settings)
        settings_layout.addRow(self.save_button)

        settings_group.setLayout(settings_layout)

        # 添加到主布局
        layout.addWidget(about_group)
        layout.addWidget(settings_group)
        layout.addStretch()
        self.setLayout(layout)

        # 初始化时加载路径
        self.load_settings()

    def select_path(self):
        folder = QFileDialog.getExistingDirectory(self, "选择游戏根目录")
        if folder:
            self.service_path_input.setText(folder)

    def save_settings(self):
        service_path = self.service_path_input.text()
        if not service_path:
            print("路径为空，未保存")
            return

        # 读取原始配置
        settings = {}
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                settings = json.load(f)

        # 更新配置
        settings["GAME_ROOT_PATH"] = service_path

        # 保存配置
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=4, ensure_ascii=False)

        print(f"保存成功：{service_path}")

    def load_settings(self):
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                settings = json.load(f)
                game_path = settings.get("GAME_ROOT_PATH", "")
                self.service_path_input.setText(game_path)

