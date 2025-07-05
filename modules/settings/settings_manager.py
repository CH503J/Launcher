#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :settings_manager.py
# @Time      :2025/7/4 15:31
# @Author    :CH503J


import os
import json
import sys


def get_app_config_path(app_name="SPTFikaTool") -> str:
    """
    获取配置文件的路径（用户目录下）
    兼容开发环境与 PyInstaller 打包后运行环境
    """
    if getattr(sys, 'frozen', False):
        # PyInstaller 打包后的路径（用户数据路径）
        base_dir = os.path.join(os.environ.get('APPDATA', os.path.expanduser("~")), app_name)
    else:
        # 源码开发环境中使用项目根目录下的 config
        base_dir = os.path.join(os.path.dirname(__file__), "..", "..", "config")

    os.makedirs(base_dir, exist_ok=True)
    return os.path.abspath(os.path.join(base_dir, "settings.json"))


SETTINGS_FILE = get_app_config_path()


def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                print(f"[配置加载成功] 配置文件路径: {SETTINGS_FILE}")
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"[配置加载失败] JSON 解析错误：{e}")
    return {}


def save_settings(settings: dict):
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


def get_server_info(settings: dict) -> dict:
    """
    收集并返回 SERVER_INFO，包括路径、名称、版本
    将其保存进 settings["SERVER_INFO"]
    """
    game_root = settings.get("GAME_ROOT_PATH", "")
    server_info = settings.get("SERVER_INFO", {})
    updated = False

    if not game_root or not os.path.isdir(game_root):
        print("[提示] 无效的游戏根目录")
        return server_info

    # 获取路径和名称
    exe_path = os.path.join(game_root, "SPT.Server.exe")
    if os.path.isfile(exe_path):
        server_info["SERVER_PATH"] = os.path.abspath(exe_path)
        server_info["SERVER_NAME"] = "SPT.Server"
        updated = True
        print(f"[发现] SPT Server 路径: {exe_path}")
    else:
        print("[提示] 未找到 SPT.Server.exe")

    # 获取版本号
    core_path = os.path.join(game_root, "SPT_Data", "Server", "configs", "core.json")
    if os.path.isfile(core_path):
        try:
            with open(core_path, "r", encoding="utf-8") as f:
                core = json.load(f)
                version = core.get("sptVersion", "")
                if version:
                    server_info["SERVER_VERSION"] = version
                    updated = True
                    print(f"[版本] SPT Server 版本: {version}")
        except Exception as e:
            print(f"[错误] 读取 core.json 失败: {e}")
    else:
        print("[提示] 未找到 core.json")

    if updated:
        settings["SERVER_INFO"] = server_info
        save_settings(settings)

    return server_info


def get_fika_server_info(settings: dict) -> dict:
    """
    收集并返回 FIKA_SERVER_INFO，包括路径、名称、版本
    将其保存进 settings["FIKA_SERVER_INFO"]
    """
    game_root = settings.get("GAME_ROOT_PATH", "")
    fika_info = settings.get("FIKA_SERVER_INFO", {})
    updated = False

    if not game_root or not os.path.isdir(game_root):
        print("[提示] 无效的游戏根目录")
        return fika_info

    # 查找 .ps1 脚本
    for file in os.listdir(game_root):
        if file.lower().endswith(".ps1"):
            full_path = os.path.abspath(os.path.join(game_root, file))
            fika_info["FIKA_SERVER_PATH"] = full_path
            fika_info["FIKA_SERVER_NAME"] = os.path.splitext(file)[0]
            updated = True
            print(f"[发现] FIKA 脚本路径: {full_path}")
            break
    else:
        print("[提示] 未找到 .ps1 文件")

    # 获取版本号
    pkg_path = os.path.join(game_root, "user", "mods", "fika-server", "package.json")
    if os.path.isfile(pkg_path):
        try:
            with open(pkg_path, "r", encoding="utf-8") as f:
                pkg = json.load(f)
                version = pkg.get("version", "")
                if version:
                    fika_info["FIKA_SERVER_VERSION"] = version
                    updated = True
                    print(f"[版本] FIKA Server 版本: {version}")
        except Exception as e:
            print(f"[错误] 读取 package.json 失败: {e}")
    else:
        print("[提示] 未找到 package.json")

    if updated:
        settings["FIKA_SERVER_INFO"] = fika_info
        save_settings(settings)

    return fika_info
