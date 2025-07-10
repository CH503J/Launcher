#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :settings_controller.py
# @Time      :2025/7/4 15:31
# @Author    :CH503J

import os
import sqlite3
import json
from modules.common.path_utils import get_db_path, get_sql_path
from modules.common.sql_loader import load_sql_queries

SQL_QUERIES = load_sql_queries(get_sql_path("game_info.sql"))


def get_game_info(key: str) -> str | None:
    """获取所有服务信息，包括根目录"""
    db_path = get_db_path("app.db")
    if not os.path.exists(db_path):
        print("[错误] 找不到数据库文件")
        return None

    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(SQL_QUERIES["get_game_info"])
            row = cursor.fetchone()
            if row:
                return dict(zip([desc[0] for desc in cursor.description], row)).get(key, "")
    except Exception as e:
        print(f"[错误] 读取 game_info 失败：{e}")


def update_game_info_value(key: str, value: str):
    """更新所有服务信息，包括根目录"""
    allowed_fields = {
        "game_root_path", "server_path", "server_name", "server_version",
        "fika_server_path", "fika_server_name", "fika_server_version"
    }

    if key not in allowed_fields:
        print(f"[警告] 不允许更新非法字段: {key}")
        return

    db_path = get_db_path("app.db")
    if not os.path.exists(db_path):
        print("[错误] 找不到数据库文件")
        return

    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(SQL_QUERIES["count_game_info"])
            if cursor.fetchone()[0] == 0:
                sql = SQL_QUERIES["insert_game_info_key"].format(key=key)
                cursor.execute(sql, (value,))
            else:
                sql = SQL_QUERIES["update_game_info_key"].format(key=key)
                cursor.execute(sql, (value,))
            conn.commit()
            print(f"[更新成功] {key} = {value}")
    except Exception as e:
        print(f"[更新失败] {e}")


def get_server_info() -> dict:
    """获取 spt-server 信息"""
    game_root = get_game_info("game_root_path")
    if not game_root or not os.path.isdir(game_root):
        print("[提示] 无效的游戏根目录")
        return {}

    server_info = {}
    exe_path = os.path.join(game_root, "SPT.Server.exe")
    if os.path.isfile(exe_path):
        abs_path = os.path.abspath(exe_path)
        server_info["server_path"] = abs_path
        server_info["server_name"] = "SPT.Server"
        update_game_info_value("server_path", abs_path)
        update_game_info_value("server_name", "SPT.Server")
        print(f"[发现] SPT Server 路径: {abs_path}")
    else:
        print("[提示] 未找到 SPT.Server.exe")

    core_path = os.path.join(game_root, "SPT_Data", "Server", "configs", "core.json")
    if os.path.isfile(core_path):
        try:
            with open(core_path, "r", encoding="utf-8") as f:
                core = json.load(f)
                version = core.get("sptVersion", "")
                if version:
                    server_info["server_version"] = version
                    update_game_info_value("server_version", version)
                    print(f"[版本] SPT Server 版本: {version}")
        except Exception as e:
            print(f"[错误] 读取 core.json 失败: {e}")
    else:
        print("[提示] 未找到 core.json")

    return server_info


def get_fika_server_info() -> dict:
    """获取 fika-server 信息"""
    game_root = get_game_info("game_root_path")
    if not game_root or not os.path.isdir(game_root):
        print("[提示] 无效的游戏根目录")
        return {}

    fika_info = {}

    # 查找 .ps1 脚本
    for file in os.listdir(game_root):
        if file.lower().endswith(".ps1"):
            abs_path = os.path.abspath(os.path.join(game_root, file))
            name = os.path.splitext(file)[0]
            fika_info["fika_server_path"] = abs_path
            fika_info["fika_server_name"] = name
            update_game_info_value("fika_server_path", abs_path)
            update_game_info_value("fika_server_name", name)
            print(f"[发现] FIKA 脚本路径: {abs_path}")
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
                    fika_info["fika_server_version"] = version
                    update_game_info_value("fika_server_version", version)
                    print(f"[版本] FIKA Server 版本: {version}")
        except Exception as e:
            print(f"[错误] 读取 package.json 失败: {e}")
    else:
        print("[提示] 未找到 package.json")

    return fika_info
