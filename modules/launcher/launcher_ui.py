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
from modules.launcher.log_reader import LogReaderThread


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
        layout.addWidget(self.log_output)  # 日志框放中间
        layout.addLayout(button_layout)  # 按钮横排放最底部

        self.setLayout(layout)

        self.start_button.clicked.connect(self.start_service)
        self.stop_button.clicked.connect(self.stop_service)

    def start_service(self):
        self.process = start_server()
        if not self.process:
            self.status_label.setText("服务状态：启动失败")
            self.append_log("服务启动失败")
            return

        self.status_label.setText("服务状态：已启动")
        self.append_log("服务启动中...")

        # 创建并启动日志线程
        self.log_thread = LogReaderThread(self.process)
        self.log_thread.log_received.connect(self.append_log)  # 线程安全更新UI
        self.log_thread.start()

    def stop_service(self):
        # 这里写停止服务逻辑
        self.status_label.setText("服务状态：已停止")
        self.append_log("服务已停止...")

    def append_log(self, text):
        """向日志框追加内容并自动滚动到底部"""
        self.log_output.append(text)
        self.log_output.verticalScrollBar().setValue(self.log_output.verticalScrollBar().maximum())
