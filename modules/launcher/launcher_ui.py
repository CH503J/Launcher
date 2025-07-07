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

from modules.launcher.launcher_controller import LauncherController


class LauncherTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.controller = None
        self.init_ui()
        self.init_controller()

    def init_ui(self):
        layout = QVBoxLayout()

        self.status_label = QLabel("服务状态：未启动")

        self.program_log_output = QTextEdit()
        self.program_log_output.setReadOnly(True)
        self.program_log_output.setFixedHeight(80)
        self.program_log_output.setPlaceholderText("程序运行日志...")

        self.fika_server_log_output = QTextEdit()
        self.fika_server_log_output.setReadOnly(True)
        self.fika_server_log_output.setFixedHeight(80)
        self.fika_server_log_output.setPlaceholderText("Fika.Server 日志...")

        self.server_log_output = QTextEdit()
        self.server_log_output.setReadOnly(True)
        self.server_log_output.setPlaceholderText("SPT.Server 日志...")

        self.headless_log_output = QTextEdit()
        self.headless_log_output.setReadOnly(True)
        self.headless_log_output.setPlaceholderText("Fika.Headless 日志...")

        top_log_row = QHBoxLayout()
        top_log_row.addWidget(self.program_log_output)
        top_log_row.addWidget(self.fika_server_log_output)

        bottom_log_row = QHBoxLayout()
        bottom_log_row.addWidget(self.server_log_output)
        bottom_log_row.addWidget(self.headless_log_output)

        self.log_all_checkbox = QCheckBox("全部日志")
        self.log_all_checkbox.setChecked(False)
        self.log_all_checkbox.setToolTip("勾选后将输出所有日志，包括 info/debug")

        self.start_button = QPushButton("启动服务")
        self.stop_button = QPushButton("停止服务")

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.log_all_checkbox)
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)

        layout.addWidget(self.status_label)
        layout.addLayout(top_log_row)
        layout.addLayout(bottom_log_row)
        layout.addLayout(button_layout)
        self.setLayout(layout)

        self.start_button.clicked.connect(self.start)
        self.stop_button.clicked.connect(self.stop)

    def init_controller(self):
        self.controller = LauncherController(self, self.main_window)

    def start(self):
        self.controller.start_services()

    def stop(self):
        self.controller.stop_services()

    def append_log(self, text, source="server"):
        if source == "fika":
            self.fika_server_log_output.append(text)
            self.fika_server_log_output.verticalScrollBar().setValue(
                self.fika_server_log_output.verticalScrollBar().maximum()
            )
        elif source == "program":
            self.program_log_output.append(text)
            self.program_log_output.verticalScrollBar().setValue(
                self.program_log_output.verticalScrollBar().maximum()
            )
        else:
            self.server_log_output.append(text)
            self.server_log_output.verticalScrollBar().setValue(
                self.server_log_output.verticalScrollBar().maximum()
            )
