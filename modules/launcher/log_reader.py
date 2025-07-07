#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :log_reader.py
# @Time      :2025/7/4 20:41
# @Author    :CH503J

from PyQt6.QtCore import QThread, pyqtSignal


class LogReaderThread(QThread):
    log_received = pyqtSignal(str)

    def __init__(self, process, show_all: bool = False):
        """
        初始化线程
        :param process: 需要监控的子进程对象
        :param show_all: 是否输出所有日志（True 输出全部，否则只输出错误日志）
        """
        super().__init__()
        self.process = process
        self.show_all = show_all

    def run(self):
        if not self.process or not self.process.stdout:
            return

        while True:
            line = self.process.stdout.readline()
            if not line:
                break
            line = line.rstrip()

            if self.show_all or self.is_error_line(line):
                self.log_received.emit(line)

    def is_error_line(self, line: str) -> bool:
        keywords = ["error", "exception", "failed", "fatal", "critical"]
        return any(kw in line.lower() for kw in keywords)