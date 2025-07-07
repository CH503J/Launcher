#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :launcher_controller.py
# @Time      :2025/7/7 13:12
# @Author    :CH503J


from PyQt6.QtCore import QTimer
from modules.launcher.launcher_service import (
    start_server,
    stop_server,
    start_fika_server,
    stop_fika_server,
)
from modules.launcher.log_reader import LogReaderThread


class LauncherController:
    def __init__(self, ui, main_window=None):
        self.ui = ui  # 传入 LauncherTab 实例（用于 UI 回调）
        self.main_window = main_window
        self.log_all_enabled = False
        self.server_process = None
        self.fika_process = None
        self.server_log_thread = None
        self.fika_log_thread = None

    def start_services(self):
        self.start_server()
        QTimer.singleShot(3000, self.start_fika_server)

    def stop_services(self):
        self.stop_server()
        self.stop_fika_server()

    def start_server(self):
        self.log_all_enabled = self.ui.log_all_checkbox.isChecked()
        self.ui.log_all_checkbox.setEnabled(False)
        self.ui.append_log(f"[提示] 启动服务，日志模式：{'全部' if self.log_all_enabled else '错误日志'}", "program")

        self.server_process = start_server()
        if not self.server_process:
            self.ui.append_log("SPT.Server 启动失败", "program")
            if self.main_window:
                self.main_window.show_toast("SPT.Server 启动失败")
            return

        self.ui.status_label.setText("SPT.Server 服务状态：已启动")
        self.ui.append_log("SPT.Server 服务启动中。。。", "program")
        if self.main_window:
            self.main_window.show_toast("SPT.Server 服务已成功启动")

        self.server_log_thread = LogReaderThread(self.server_process, self.log_all_enabled)
        self.server_log_thread.log_received.connect(lambda text: self.ui.append_log(text, "server"))
        self.server_log_thread.start()

    def start_fika_server(self):
        self.fika_process = start_fika_server()
        if not self.fika_process:
            self.ui.append_log("[错误] Fika.Server 启动失败", "program")
            if self.main_window:
                self.main_window.show_toast("Fika.Server 启动失败")
            return

        self.ui.append_log("[启动成功] Fika.Server 已启动", "program")
        if self.main_window:
            self.main_window.show_toast("Fika.Server 启动成功")

        self.fika_log_thread = LogReaderThread(self.fika_process, self.log_all_enabled)
        self.fika_log_thread.log_received.connect(lambda text: self.ui.append_log(text, "fika"))
        self.fika_log_thread.start()

    def stop_server(self):
        stop_server()
        self.ui.append_log("SPT.Server 服务已停止。", "program")
        if self.main_window:
            self.main_window.show_toast("SPT.Server 服务已停止")

        self.ui.status_label.setText("SPT.Server 服务状态：已停止")
        self.ui.log_all_checkbox.setEnabled(True)

    def stop_fika_server(self):
        stop_fika_server()
        self.ui.append_log("Fika.Server 已停止", "program")
        if self.main_window:
            self.main_window.show_toast("Fika.Server 已停止")
