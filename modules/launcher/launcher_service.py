#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :launcher_service.py
# @Time      :2025/7/4 15:15
# @Author    :CH503J

import os
import subprocess
from modules.settings.settings_controller import get_game_info_value

# 全局进程句柄（用于服务控制）
server_process = None
fika_process = None


def read_stdout(pipe, callback):
    """
    持续读取子进程输出并通过回调处理
    :param pipe: 子进程的 stdout 管道
    :param callback: 每读取一行后触发的回调函数
    """
    while True:
        line = pipe.readline()
        if not line:
            break
        callback(line.rstrip())


def start_server():
    """
    启动 SPT.Server.exe 进程
    - 从数据库字段 'server_path' 获取路径
    - 启动成功后返回 Popen 对象
    """
    global server_process
    server_path = get_game_info_value("server_path")
    if not server_path or not os.path.isfile(server_path):
        print("[错误] 无效的 server_path")
        return None

    try:
        process = subprocess.Popen(
            [server_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            bufsize=1,
            cwd=os.path.dirname(server_path)
        )
        server_process = process
        print(f"[启动成功] Server 启动于：{server_path}")
        return process
    except Exception as e:
        print(f"[错误] 启动 SPT.Server 失败: {e}")
        return None


def start_fika_server():
    """
    启动 FIKA Server 脚本（.ps1）
    - 从数据库字段 'fika_server_path' 获取路径
    - 启动成功后返回 Popen 对象
    """
    global fika_process
    fika_path = get_game_info_value("fika_server_path")
    if not fika_path or not os.path.isfile(fika_path):
        print("[错误] 无效的 FIKA 脚本路径")
        return None

    try:
        process = subprocess.Popen(
            ["powershell", "-ExecutionPolicy", "Bypass", "-NoLogo", "-NoProfile", "-File", fika_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            cwd=os.path.dirname(fika_path)
        )
        fika_process = process
        print(f"[启动成功] FIKA 脚本：{fika_path}")
        return process
    except Exception as e:
        print(f"[错误] 启动 FIKA 脚本失败: {e}")
        return None


def stop_server():
    """
    停止 SPT.Server 进程，若无法正常终止则强制 kill
    """
    global server_process
    if server_process and server_process.poll() is None:
        try:
            server_process.terminate()
            server_process.wait(timeout=5)
            print("[停止成功] Server 已终止")
        except Exception as e:
            print(f"[停止失败] 尝试终止 Server 进程失败: {e}")
            try:
                server_process.kill()
                print("[强制终止] Server 被 kill")
            except Exception as ke:
                print(f"[严重错误] kill Server 失败: {ke}")
    else:
        print("[提示] Server 未在运行")

    server_process = None


def stop_fika_server():
    """
    停止 FIKA Server 脚本进程，若无法正常终止则强制 kill
    """
    global fika_process
    if fika_process and fika_process.poll() is None:
        try:
            fika_process.terminate()
            fika_process.wait(timeout=5)
            print("[停止成功] FIKA Server 已终止")
        except Exception as e:
            print(f"[停止失败] 尝试终止 FIKA 进程失败: {e}")
            try:
                fika_process.kill()
                print("[强制终止] FIKA Server 被 kill")
            except Exception as ke:
                print(f"[严重错误] kill FIKA 失败: {ke}")
    else:
        print("[提示] FIKA Server 未在运行")

    fika_process = None
