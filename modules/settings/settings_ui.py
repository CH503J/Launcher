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

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"[配置加载失败] JSON 解析错误：{e}")
    return {}

def save_settings_to_file(settings: dict):
    try:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"[保存配置失败] 原因：{e}")


class AboutTab(QWidget):
    def __init__(self):
        super().__init__()
        self.settings = {}
        self.init_ui()
        self.load_ui_settings()

    def init_ui(self):
        layout = QVBoxLayout()

        # 关于软件信息区域
        self.about_group = QGroupBox("关于软件")
        about_layout = QVBoxLayout()
        self.app_name_label = QLabel()
        self.app_version_label = QLabel()
        self.app_author_label = QLabel()
        about_layout.addWidget(self.app_name_label)
        about_layout.addWidget(self.app_version_label)
        about_layout.addWidget(self.app_author_label)
        self.about_group.setLayout(about_layout)

        # 游戏根目录设置区域
        settings_group = QGroupBox("软件设置")
        settings_layout = QFormLayout()

        self.service_path_input = QLineEdit()
        self.service_path_input.setPlaceholderText("例如：C:/Games/MyGame")

        self.select_path_button = QPushButton("选择路径")
        self.select_path_button.clicked.connect(self.select_path)

        path_layout = QHBoxLayout()
        path_layout.addWidget(self.service_path_input)
        path_layout.addWidget(self.select_path_button)

        settings_layout.addRow("游戏根目录：", path_layout)

        # 保存按钮
        self.save_button = QPushButton("保存设置")
        self.save_button.clicked.connect(self.save_settings)
        settings_layout.addRow(self.save_button)

        settings_group.setLayout(settings_layout)

        # 布局整合
        layout.addWidget(self.about_group)
        layout.addWidget(settings_group)
        layout.addStretch()
        self.setLayout(layout)

    def load_ui_settings(self):
        self.settings = load_settings()
        game_path = self.settings.get("GAME_ROOT_PATH", "")
        self.service_path_input.setText(game_path)

        app_info = self.settings.get("APP_INFO", {})
        self.app_name_label.setText(f"软件名称：{app_info.get('APP_NAME', '未知软件')}")
        self.app_version_label.setText(f"版本号：{app_info.get('APP_VERSION', '未知版本')}")
        self.app_author_label.setText(f"开发者：{app_info.get('APP_AUTHOR', '未知作者')}")

    def select_path(self):
        current_path = self.service_path_input.text().strip() or os.path.expanduser("~")
        folder = QFileDialog.getExistingDirectory(self, "选择游戏根目录", current_path)
        if folder:
            self.service_path_input.setText(folder)

    def save_settings(self):
        service_path = self.service_path_input.text().strip()
        if not service_path:
            print("[提示] 路径为空，未保存")
            return

        self.settings["GAME_ROOT_PATH"] = service_path
        save_settings_to_file(self.settings)
        print(f"[保存成功] 路径：{service_path}")
        self.load_ui_settings()
