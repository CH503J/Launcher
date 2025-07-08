#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :log_reader.py
# @Time      :2025/7/4 20:41
# @Author    :CH503J

from PyQt6.QtCore import QThread, pyqtSignal


class LogReaderThread(QThread):
    """
    子进程日志读取线程类
    - 读取子进程输出流 stdout 的每一行
    - 可根据 show_all 参数决定是否仅输出错误日志
    - 使用信号机制将日志实时传递给 UI 控件
    """

    # 信号：接收到日志行时触发
    log_received = pyqtSignal(str)

    def __init__(self, process, show_all: bool = False):
        """
        初始化线程
        :param process: 被监控的子进程（Popen 对象）
        :param show_all: 是否输出所有日志（False 表示仅输出错误/异常行）
        """
        super().__init__()
        self.process = process
        self.show_all = show_all

    def run(self):
        """
        线程执行逻辑
        - 持续读取子进程 stdout 流
        - 根据规则筛选后通过信号发出
        """
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
        """
        判断是否为错误日志行（用于筛选）
        :param line: 日志行内容
        :return: 若包含常见错误关键字则返回 True
        """
        keywords = ["error", "exception", "failed", "fatal", "critical"]
        return any(kw in line.lower() for kw in keywords)
