#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :launcher_service.py
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
fika_process = None


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


def start_fika_server():
    """
    启动 Fika Server（PowerShell 脚本）
    从配置文件中读取 FIKA_SERVER_INFO，使用 powershell 启动 ps1 脚本
    :return: Popen 进程对象（启动失败返回 None）
    """
    global fika_process
    settings = load_settings()
    fika_path = settings.get("FIKA_SERVER_INFO", {}).get("FIKA_SERVER_PATH", "")
    if not fika_path or not os.path.isfile(fika_path):
        print("[错误] FIKA 启动脚本未找到")
        return None

    fika_dir = os.path.dirname(fika_path)

    try:
        process = subprocess.Popen(
            ["powershell", "-ExecutionPolicy", "Bypass", "-NoLogo", "-NoProfile", "-File", fika_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=1,
            cwd=fika_dir,
            text=True
        )
        fika_process = process
        print(f"[启动成功] 已启动 FIKA 脚本：{fika_path}")
        return process
    except Exception as e:
        print(f"[错误] 启动 FIKA 脚本失败: {e}")
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


def stop_fika_server():
    global fika_process

    if fika_process and fika_process.poll() is None:
        try:
            fika_process.terminate()
            fika_process.wait(timeout=5)
            print("[停止成功] FIKA Server 已终止")
        except Exception as e:
            print(f"[停止失败] 尝试终止 FIKA 进程时出错: {e}")
            try:
                fika_process.kill()
                print("[强制终止] FIKA Server 已被 kill")
            except Exception as ke:
                print(f"[严重错误] kill FIKA 失败：{ke}")
    else:
        print("[提示] FIKA Server 当前未在运行或已结束")

    fika_process = None  # 清空引用
