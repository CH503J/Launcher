#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :launcher_ui.py
# @Time      :2025/7/4 15:01
# @Author    :CH503J

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QTextEdit,
    QCheckBox
)

from modules.launcher.launcher_service_manager import (
    start_server,
    stop_server,
    start_fika_server,
    stop_fika_server
)
from modules.launcher.log_reader import LogReaderThread


class LauncherTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.log_all_enabled = False  # 标记是否输出所有日志
        self.process = None
        self.fika_process = None
        self.log_thread = None
        self.fika_log_thread = None  # 如果后续你接日志要用
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.status_label = QLabel("服务状态：未启动")

        # 新增顶部两个小日志框（程序日志 + 占位空白）
        self.program_log_output = QTextEdit()
        self.program_log_output.setReadOnly(True)
        self.program_log_output.setFixedHeight(80)  # 小框高度
        self.program_log_output.setPlaceholderText("程序运行日志...")

        self.fika_server_log_output = QTextEdit()
        self.fika_server_log_output.setReadOnly(True)
        self.fika_server_log_output.setFixedHeight(80)
        self.fika_server_log_output.setPlaceholderText("Fika.Server 日志...")

        # 下方的 server 和 fika 日志框
        self.server_log_output = QTextEdit()
        self.server_log_output.setReadOnly(True)
        self.server_log_output.setPlaceholderText("SPT.Server 日志...")

        self.headless_log_output = QTextEdit()
        self.headless_log_output.setReadOnly(True)
        self.headless_log_output.setPlaceholderText("Fika.Headless 日志...")

        # 上面一行两个小框（程序日志 + 占位）
        top_log_row = QHBoxLayout()
        top_log_row.addWidget(self.program_log_output)
        top_log_row.addWidget(self.fika_server_log_output)

        # 下面一行两个服务日志框
        bottom_log_row = QHBoxLayout()
        bottom_log_row.addWidget(self.server_log_output)
        bottom_log_row.addWidget(self.headless_log_output)

        # 勾选框：是否输出所有日志
        self.log_all_checkbox = QCheckBox("全部日志")
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

        # 加入主 layout
        layout.addWidget(self.status_label)
        layout.addLayout(top_log_row)
        layout.addLayout(bottom_log_row)
        layout.addLayout(button_layout)
        self.setLayout(layout)

        self.start_button.clicked.connect(self.start)
        self.stop_button.clicked.connect(self.stop)

    def start(self):
        self.start_spt_service()
        QTimer.singleShot(3000, self.start_fika_service)

    def stop(self):
        """停止所有服务"""
        self.stop_spt_service()
        self.stop_fika_service()

    def start_spt_service(self):
        self.log_all_enabled = self.log_all_checkbox.isChecked()
        self.log_all_checkbox.setEnabled(False)  # 禁用勾选框，避免中途更改
        self.append_log(f"[提示] 启动服务，日志模式：{'全部' if self.log_all_enabled else '错误日志'}", source="program")

        self.process = start_server()
        if not self.process:
            self.status_label.setText("SPT.Server 服务状态：启动失败")
            self.append_log("SPT.Server 服务启动失败", source="program")
            if self.main_window:
                self.main_window.show_toast("SPT.Server 服务启动失败")
            return

        self.status_label.setText("SPT.Server 服务状态：已启动")
        self.append_log("SPT.Server 服务启动中。。。", source="program")
        if self.main_window:
            self.main_window.show_toast("服务已成功启动")

        # 创建并启动日志线程
        self.log_thread = LogReaderThread(self.process, self.log_all_enabled)
        self.log_thread.log_received.connect(lambda text: self.append_log(text, source="server"))
        self.log_thread.start()

    def start_fika_service(self):
        self.fika_process = start_fika_server()
        if not self.fika_process:
            self.append_log("[错误] Fika.Server 启动失败", source="program")
            if self.main_window:
                self.main_window.show_toast("Fika.Server 启动失败")
        else:
            self.append_log("[启动成功] Fika.Server 已启动", source="program")
            if self.main_window:
                self.main_window.show_toast("Fika.Server 启动成功")

            # ✅ 创建并启动 Fika.Server 日志线程
            self.fika_log_thread = LogReaderThread(self.fika_process, self.log_all_enabled)
            self.fika_log_thread.log_received.connect(lambda text: self.append_log(text, source="fika"))
            self.fika_log_thread.start()

    def stop_spt_service(self):
        """停止主服务"""
        stop_server()
        self.append_log("SPT.Server 服务已停止。", source="program")
        if self.main_window:
            self.main_window.show_toast("SPT.Server 服务已停止")

        self.status_label.setText("SPT.Server 服务状态：已停止")
        self.log_all_checkbox.setEnabled(True) # 允许切换是否输出所有日志

    def stop_fika_service(self):
        """停止 Fika.Server"""
        stop_fika_server()
        self.append_log("Fika.Server 已停止", source="program")
        if self.main_window:
            self.main_window.show_toast("Fika.Server 已停止")

    def append_log(self, text, source="server"):
        if source == "fika":
            self.fika_server_log_output.append(text)  # ✅ 改为右上角 fika_server_log_output
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