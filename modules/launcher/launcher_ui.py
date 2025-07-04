#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :launcher_ui.py
# @Time      :2025/7/4 15:01
# @Author    :CH503J


from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QTextEdit
)

from modules.launcher.launcher_service_manager import start_server


class LauncherTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.status_label = QLabel("服务状态：未启动")

        # 日志输出框，设置只读
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setPlaceholderText("服务启动日志会显示在这里...")

        self.start_button = QPushButton("启动服务")
        self.stop_button = QPushButton("停止服务")

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)

        layout.addWidget(self.status_label)
        layout.addWidget(self.log_output)       # 日志框放中间
        layout.addLayout(button_layout)          # 按钮横排放最底部

        self.setLayout(layout)

        self.start_button.clicked.connect(self.start_service)
        self.stop_button.clicked.connect(self.stop_service)

    def start_service(self):
        # 这里写启动服务逻辑，比如调用 launcher_service_manager.py
        self.status_label.setText("服务状态：已启动")
        self.append_log("服务已启动...")

        def log_callback(text):
            self.append_log(text)
        success = start_server(log_callback)
        if success:
            self.status_label.setText("服务状态：已启动")
        else:
            self.status_label.setText("服务状态：启动失败")

    def stop_service(self):
        # 这里写停止服务逻辑
        self.status_label.setText("服务状态：已停止")
        self.append_log("服务已停止...")

    def append_log(self, text):
        """向日志框追加内容并自动滚动到底部"""
        self.log_output.append(text)
        self.log_output.verticalScrollBar().setValue(self.log_output.verticalScrollBar().maximum())

