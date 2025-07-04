#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :config_manager.py.py
# @Time      :2025/7/4 15:31
# @Author    :CH503J


import os
import json

SETTINGS_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "config", "settings.json")


def load_settings():
    """
    读取设置文件
    尝试加载指定路径的JSON配置文件，若文件不存在或解析失败则返回空字典
    返回: dict: 从配置文件加载的数据，失败时返回空字典
    """
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"[配置加载失败] JSON 解析错误：{e}")
    return {}


def save_settings(settings: dict):
    """
    保存设置文件
    将提供的字典数据写入指定路径的JSON配置文件，若写入过程中发生异常则打印错误信息
    参数: settings (dict): 要写入配置文件的数据字典
    返回: None
    """
    try:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"[保存配置失败] 原因：{e}")


def get_game_root_path(settings: dict) -> str:
    """
    获取配置中的游戏根目录路径
    参数: settings (dict): 包含配置项的字典对象
    返回: str: 配置文件中 "GAME_ROOT_PATH" 对应的值，如果不存在则返回空字符串
    """
    return settings.get("GAME_ROOT_PATH", "")


def get_app_info(settings: dict) -> dict:
    """
    获取配置中的应用程序信息(APP_INFO)
    参数: settings (dict): 包含配置项的字典对象
    返回: dict: 配置文件中 "APP_INFO" 对应的值，如果不存在则返回空字典
    """
    return settings.get("APP_INFO", {})


def get_server_path(settings: dict) -> str:
    """
    获取游戏根目录下的 server.exe 路径。
    如果存在，则将其保存到 SERVER_INFO 中，并返回该路径。

    参数:
        settings (dict): 当前配置项

    返回:
        str: server.exe 的绝对路径；未找到则返回空字符串
    """
    game_root = settings.get("GAME_ROOT_PATH", "")
    if not game_root or not os.path.isdir(game_root):
        print("[提示] 无效的游戏根目录")
        return ""

    server_path = os.path.join(game_root, "SPT.Server.exe")
    if os.path.isfile(server_path):
        # 初始化 SERVER_INFO 结构
        server_info = settings.get("SERVER_INFO", {})
        server_info["SERVER_PATH"] = os.path.abspath(server_path)
        server_info["SERVER_NAME"] = "SPT.Server"
        server_info.setdefault("SERVER_VERSION", "")

        settings["SERVER_INFO"] = server_info
        save_settings(settings)

        print(f"[发现] server.exe 路径：{server_path}")
        return server_path
    else:
        print("[提示] server.exe 不存在于指定根目录")
        return ""

def get_fika_server_path(settings: dict) -> str:
    """
    查找游戏根目录下的 FIKA PowerShell 服务脚本 (.ps1)
    找到后将其路径与文件名写入 FIKA_SERVER_INFO 并保存配置
    参数:
        settings (dict): 当前配置项
    返回:
        str: 找到的 .ps1 文件的绝对路径，未找到则返回空字符串
    """
    game_root = settings.get("GAME_ROOT_PATH", "")
    if not game_root or not os.path.isdir(game_root):
        print("[提示] 无效的游戏根目录")
        return ""

    for file in os.listdir(game_root):
        if file.lower().endswith(".ps1"):
            full_path = os.path.abspath(os.path.join(game_root, file))
            fika_info = settings.get("FIKA_SERVER_INFO", {})
            fika_info["FIKA_SERVER_PATH"] = full_path
            fika_info["FIKA_SERVER_NAME"] = os.path.splitext(file)[0]
            fika_info.setdefault("FIKA_SERVER_VERSION", "")

            settings["FIKA_SERVER_INFO"] = fika_info
            save_settings(settings)

            print(f"[发现] FIKA 脚本路径：{full_path}")
            return full_path

    print("[提示] 根目录未找到任何 .ps1 脚本")
    return ""