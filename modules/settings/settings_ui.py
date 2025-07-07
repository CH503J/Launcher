#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :settings_ui.py
# @Time      :2025/7/4 15:32
# @Author    :CH503J

import os
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QGroupBox,
    QFormLayout,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QFileDialog
)
from modules.settings.settings_manager import (
    load_settings,
    save_settings,
    get_game_root_path,
    get_app_info,
    get_server_info,
    get_fika_server_info
)


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

        # GitHub 项目链接
        self.github_link_label = QLabel('<a href="https://github.com/CH503J/Launcher">🌐 GitHub 项目主页</a>')
        self.github_link_label.setOpenExternalLinks(True)
        self.github_link_label.setStyleSheet("QLabel { color: #1e90ff; font-size: 14px; }")
        about_layout.addWidget(self.github_link_label)

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
        # 获取服务器信息
        get_server_info(self.settings)
        # 获取 FIKA 服务信息
        get_fika_server_info(self.settings)
        game_path = get_game_root_path(self.settings)
        self.service_path_input.setText(game_path)

        app_info = get_app_info(self.settings)
        # self.app_name_label.setText(f"软件名称：{app_info.get('APP_NAME', '未知软件')}")
        # self.app_version_label.setText(f"版本号：{app_info.get('APP_VERSION', '未知版本')}")
        # self.app_author_label.setText(f"开发者：{app_info.get('APP_AUTHOR', '未知作者')}")
        self.app_name_label.setText(f"软件名称：SPT-Fika launcher")
        self.app_version_label.setText(f"版本号：v 0.1")
        self.app_author_label.setText(f"开发者：CH503J")

    def select_path(self):
        current_path = self.service_path_input.text().strip() or os.path.expanduser("~")
        folder = QFileDialog.getExistingDirectory(self, "选择游戏根目录", current_path)
        if folder:
            self.service_path_input.setText(folder)

    def save_settings(self):
        """
        保存用户设置，将界面上的游戏根目录路径保存到配置文件中。
        如果输入路径为空，则打印提示信息并返回。
        保存成功后会更新界面显示的设置信息。
        """
        service_path = self.service_path_input.text().strip()
        if not service_path:
            print("[提示] 路径为空，未保存")
            return

        self.settings["GAME_ROOT_PATH"] = service_path
        save_settings(self.settings)
        print(f"[保存成功] 路径：{service_path}")
        self.load_ui_settings()
