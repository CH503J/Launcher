#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :log_reader.py
# @Time      :2025/7/4 20:41
# @Author    :CH503J

from PyQt6.QtCore import QThread, pyqtSignal


class LogReaderThread(QThread):
    log_received = pyqtSignal(str)  # 定义信号，用于向主线程发送读取到的日志

    def __init__(self, process):
        """
        初始化线程实例
        :param process: 需要监控的子进程对象
        """
        super().__init__()
        self.process = process  # 存储传入的子进程对象，以便后续操作

    def run(self):
        """
        线程执行函数，持续读取子进程的标准输出并发射日志信号
        当检测到输出结束时退出循环
        """
        while True:
            line = self.process.stdout.readline()  # 按行读取子进程的输出
            if not line:  # 如果没有读取到内容，表示输出结束
                break
            self.log_received.emit(line.rstrip())  # 发射信号，传递处理后的日志行
