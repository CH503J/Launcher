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
    QTextEdit,
    QCheckBox
)

from modules.launcher.launcher_service_manager import start_server, stop_server
from modules.launcher.log_reader import LogReaderThread


class LauncherTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.log_all_enabled = False  # 标记是否输出所有日志
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.status_label = QLabel("服务状态：未启动")

        # 日志输出框，设置只读
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setPlaceholderText("服务启动日志会显示在这里...")

        # 勾选框：是否输出所有日志
        self.log_all_checkbox = QCheckBox("是否输出全部日志")
        self.log_all_checkbox.setChecked(False)  # 默认只输出错误信息
        self.log_all_checkbox.setToolTip("勾选后将输出所有日志，包括 info/debug")

        # 启停按钮
        self.start_button = QPushButton("启动服务")
        self.stop_button = QPushButton("停止服务")

        # 横向按钮布局
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.log_all_checkbox)  # 勾选框放在最左侧
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)

        # 总体布局
        layout.addWidget(self.status_label)
        layout.addWidget(self.log_output)
        layout.addLayout(button_layout)
        self.setLayout(layout)

        self.start_button.clicked.connect(self.start_service)
        self.stop_button.clicked.connect(self.stop_service)

    def start_service(self):
        self.log_all_enabled = self.log_all_checkbox.isChecked()
        self.log_all_checkbox.setEnabled(False)  # 禁用勾选框，避免中途更改
        self.append_log(f"[提示] 启动服务，日志模式：{'全部' if self.log_all_enabled else '错误日志'}")

        self.process = start_server()
        if not self.process:
            self.status_label.setText("服务状态：启动失败")
            self.append_log("服务启动失败")
            if self.main_window:
                self.main_window.show_toast("服务启动失败")
            return

        self.status_label.setText("服务状态：已启动")
        self.append_log("服务启动中。。。")
        if self.main_window:
            self.main_window.show_toast("服务已成功启动")

        # 创建并启动日志线程
        self.log_thread = LogReaderThread(self.process, self.log_all_enabled)
        self.log_thread.log_received.connect(self.append_log)
        self.log_thread.start()

    def stop_service(self):
        stop_server()
        self.status_label.setText("服务状态：已停止")
        self.append_log("服务已停止。")
        if self.main_window:
            self.main_window.show_toast("服务已停止")

        # 重新启用勾选框
        self.log_all_checkbox.setEnabled(True)

    def append_log(self, text):
        self.log_output.append(text)
        self.log_output.verticalScrollBar().setValue(self.log_output.verticalScrollBar().maximum())
