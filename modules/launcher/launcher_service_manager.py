#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :launcher_service_manager.py
# @Time      :2025/7/4 15:15
# @Author    :CH503J


import subprocess
import os
import json
import threading

SETTINGS_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "config", "settings.json")


def read_stdout(pipe, callback):
    """不断读取pipe中的内容，回调返回读取的字符串"""
    while True:
        line = pipe.readline()
        if not line:
            break
        callback(line.rstrip())

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# 进程句柄（全局变量，后面方便停止）
server_process = None

def start_server(log_callback):
    global server_process, stdout_thread
    settings = load_settings()
    server_info = settings.get("SERVER_INFO", {})
    server_path = server_info.get("SERVER_PATH", "")

    if not server_path or not os.path.isfile(server_path):
        log_callback("[启动失败] 未找到有效的 server 可执行文件路径")
        return False

    # 重点：服务启动目录
    server_dir = os.path.dirname(server_path)

    try:
        server_process = subprocess.Popen(
            [server_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=1,
            universal_newlines=True,
            encoding="utf-8",  # 👈 关键：防止 UnicodeDecodeError
            cwd=server_dir
        )

        stdout_thread = threading.Thread(target=read_stdout, args=(server_process.stdout, log_callback))
        stdout_thread.daemon = True
        stdout_thread.start()

        log_callback("[启动成功] Server 已启动")
        return True
    except Exception as e:
        log_callback(f"[启动异常] 启动 Server 失败: {e}")
        return False