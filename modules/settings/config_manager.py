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
    
    返回:
        dict: 从配置文件加载的数据，失败时返回空字典
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

    参数:
        settings (dict): 要写入配置文件的数据字典

    返回:
        None
    """
    try:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"[保存配置失败] 原因：{e}")


def get_game_root_path(settings: dict) -> str:
    """
    获取配置中的游戏根目录路径

    参数:
        settings (dict): 包含配置项的字典对象

    返回:
        str: 配置文件中 "GAME_ROOT_PATH" 对应的值，如果不存在则返回空字符串
    """
    return settings.get("GAME_ROOT_PATH", "")


def get_app_info(settings: dict) -> dict:
    """
    获取配置中的应用程序信息(APP_INFO)

    参数:
        settings (dict): 包含配置项的字典对象

    返回:
        dict: 配置文件中 "APP_INFO" 对应的值，如果不存在则返回空字典
    """
    return settings.get("APP_INFO", {})
