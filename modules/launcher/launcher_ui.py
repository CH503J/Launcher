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
    """
    启动器页面 UI 类
    包含服务启动控制按钮、日志输出框、状态标签
    """

    def __init__(self, parent=None):
        """
        :param parent: 主窗口 MainWindow，用于传入控制器做弹窗提示
        """
        super().__init__(parent)
        self.main_window = parent
        self.controller = None
        self.init_ui()
        self.init_controller()

    def init_ui(self):
        """初始化 UI 控件与布局"""
        layout = QVBoxLayout()

        self.status_label = QLabel("服务状态：未启动")

        # 上层日志：程序日志 + Fika 日志
        self.program_log_output = QTextEdit()
        self.program_log_output.setReadOnly(True)
        self.program_log_output.setFixedHeight(80)
        self.program_log_output.setPlaceholderText("程序运行日志...")

        self.fika_server_log_output = QTextEdit()
        self.fika_server_log_output.setReadOnly(True)
        self.fika_server_log_output.setFixedHeight(80)
        self.fika_server_log_output.setPlaceholderText("Fika.Server 日志...")

        # 下层日志：SPT 日志 + Headless（预留）
        self.server_log_output = QTextEdit()
        self.server_log_output.setReadOnly(True)
        self.server_log_output.setPlaceholderText("SPT.Server 日志...")

        self.headless_log_output = QTextEdit()
        self.headless_log_output.setReadOnly(True)
        self.headless_log_output.setPlaceholderText("Fika.Headless 日志...")

        # 横向分布两行日志窗口
        top_log_row = QHBoxLayout()
        top_log_row.addWidget(self.program_log_output)
        top_log_row.addWidget(self.fika_server_log_output)

        bottom_log_row = QHBoxLayout()
        bottom_log_row.addWidget(self.server_log_output)
        bottom_log_row.addWidget(self.headless_log_output)

        # 控制按钮区
        self.log_all_checkbox = QCheckBox("全部日志")
        self.log_all_checkbox.setChecked(False)
        self.log_all_checkbox.setToolTip("勾选后将输出所有日志，包括 info/debug")

        self.start_button = QPushButton("启动服务")
        self.stop_button = QPushButton("停止服务")

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.log_all_checkbox)
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)

        # 页面整体布局组装
        layout.addWidget(self.status_label)
        layout.addLayout(top_log_row)
        layout.addLayout(bottom_log_row)
        layout.addLayout(button_layout)
        self.setLayout(layout)

        # 信号连接
        self.start_button.clicked.connect(self.start)
        self.stop_button.clicked.connect(self.stop)

    def init_controller(self):
        """初始化启动器控制器"""
        self.controller = LauncherController(self, self.main_window)

    def start(self):
        """启动服务（由控制器控制）"""
        self.controller.start_services()

    def stop(self):
        """停止服务（由控制器控制）"""
        self.controller.stop_services()

    def append_log(self, text, source="server"):
        """
        追加日志到对应日志窗口
        :param text: 日志内容
        :param source: 日志来源，支持 "program" / "fika" / "server"
        """
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
