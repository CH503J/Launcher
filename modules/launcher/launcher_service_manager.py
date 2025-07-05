#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :launcher_service_manager.py
# @Time      :2025/7/4 15:15
# @Author    :CH503J


import json
import os
import subprocess

from modules.settings.settings_manager import get_app_config_path

SETTINGS_FILE = get_app_config_path()


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


def start_server():
    global server_process
    settings = load_settings()
    server_path = settings.get("SERVER_INFO", {}).get("SERVER_PATH", "")
    if not server_path or not os.path.isfile(server_path):
        return None

    server_dir = os.path.dirname(server_path)

    try:
        process = subprocess.Popen(
            [server_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            bufsize=1,
            cwd=server_dir
        )
        server_process = process
        return process
    except Exception as e:
        print(f"[错误] 启动失败: {e}")
        return None

def stop_server():
    global server_process

    if server_process and server_process.poll() is None:
        try:
            server_process.terminate()
            server_process.wait(timeout=5)
            print("[停止成功] Server 已终止")
        except Exception as e:
            print(f"[停止失败] 尝试终止 server 进程时出错: {e}")
            try:
                server_process.kill()
                print("[强制终止] Server 已被 kill")
            except Exception as ke:
                print(f"[严重错误] kill 失败：{ke}")
    else:
        print("[提示] Server 当前未在运行或已结束")

    server_process = None  # 清空引用