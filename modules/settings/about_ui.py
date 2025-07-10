#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :about_ui.py
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
    QFileDialog,
    QGridLayout
)
from modules.settings.settings_controller import (
    update_game_info_value,
    get_server_info,
    get_fika_server_info, get_game_info,
)
from modules.settings.about_controller import get_app_info, get_gift_code


def copy_to_clipboard(text: str):
    """点击即复制"""
    from PyQt6.QtGui import QGuiApplication
    QGuiApplication.clipboard().setText(text)
    print(f"[复制成功] {text}")


class AboutTab(QWidget):
    def __init__(self):
        super().__init__()
        self.label_name = None
        self.label_version = None
        self.label_author = None
        self.github_label = None
        self.input_path = None
        self.gift_list = None
        self.gift_layout = None
        self.app_info = get_app_info()
        self.init_ui()
        self.load_info()

    def init_ui(self):
        layout = QVBoxLayout()

        # --- 软件信息区域 ---
        about_group = QGroupBox("关于软件")
        about_layout = QVBoxLayout()

        self.label_name = QLabel()
        self.label_version = QLabel()
        self.label_author = QLabel()

        about_layout.addWidget(self.label_name)
        about_layout.addWidget(self.label_version)
        about_layout.addWidget(self.label_author)

        self.github_label = QLabel(
            f'<a href="{self.app_info.get("github_link", "https://example.com")}">🌐 GitHub 主页</a>'
        )
        self.github_label.setOpenExternalLinks(True)
        self.github_label.setStyleSheet("QLabel { color: #1e90ff; font-size: 14px; }")
        about_layout.addWidget(self.github_label)

        about_group.setLayout(about_layout)

        # --- 设置区域 ---
        settings_group = QGroupBox("软件设置")
        form_layout = QFormLayout()

        self.input_path = QLineEdit()
        self.input_path.setPlaceholderText(self.app_info.get("example_path", "请输入路径"))

        btn_select = QPushButton("选择路径")
        btn_select.clicked.connect(self.select_path)

        path_layout = QHBoxLayout()
        path_layout.addWidget(self.input_path)
        path_layout.addWidget(btn_select)

        btn_save = QPushButton("保存设置")
        btn_save.clicked.connect(self.save_path)

        form_layout.addRow("游戏根目录：", path_layout)
        form_layout.addRow(btn_save)

        settings_group.setLayout(form_layout)

        # --- 复制按钮区域 ---
        self.gift_list = get_gift_code()
        gift_group = QGroupBox(f"礼包码（{len(self.gift_list)}）")
        gift_group.setToolTip("点击礼包码即可复制")
        self.gift_layout = QGridLayout()
        gift_group.setLayout(self.gift_layout)

        # --- 主布局 ---
        layout.addWidget(about_group)
        layout.addWidget(settings_group)
        layout.addWidget(gift_group)
        layout.addStretch()
        self.setLayout(layout)

    def load_info(self):
        # 设置软件信息
        self.label_name.setText(f"软件名称：{self.app_info.get('app_name', '未知')}")
        self.label_version.setText(f"版本号：{self.app_info.get('version', '未知')}")
        self.label_author.setText(f"开发者：{self.app_info.get('author', '未知')}")

        # 显示游戏路径
        self.input_path.setText(get_game_info("game_root_path"))

        # 自动扫描服务端
        get_server_info()
        get_fika_server_info()

        # 动态添加按钮到 grid
        for i, code in enumerate(self.gift_list):
            btn = QPushButton(code)
            btn.clicked.connect(lambda _, v=code: copy_to_clipboard(v))
            row, col = divmod(i, 5)  # 每行放7个按钮
            self.gift_layout.addWidget(btn, row, col)

    def select_path(self):
        current = self.input_path.text().strip() or os.path.expanduser("~")
        folder = QFileDialog.getExistingDirectory(self, "选择游戏根目录", current)
        if folder:
            self.input_path.setText(folder)

    def save_path(self):
        path = self.input_path.text().strip()
        if not path:
            print("[提示] 路径为空，未保存")
            return
        update_game_info_value("game_root_path", path)
        print(f"[保存成功] 路径：{path}")
        self.load_info()
