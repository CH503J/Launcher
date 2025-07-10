#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :data_extraction_utils.py
# @Time      :2025/7/9 11:17
# @Author    :CH503J


import os
import json
from collections import defaultdict
import sqlite3
from modules.common.path_utils import get_db_path, get_sql_path
from modules.common.sql_loader import load_sql_queries
from modules.settings.settings_controller import get_game_info

SQL_QUERIES = load_sql_queries(get_sql_path("language_info.sql"))


def get_language_data() -> list[dict]:
    json_path = os.path.join(get_game_info("game_root_path"),
                             "SPT_Data", "Server", "database", "locales", "global", "ch.json")

    if not os.path.exists(json_path):
        print(f"[错误] 文件不存在：{json_path}")
        return []

    with open(json_path, "r", encoding="utf-8") as f:
        try:
            raw_data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"[错误] JSON 解析失败: {e}")
            return []

    # ITEM 类型（大驼峰命名）
    item_suffix_map = {
        "Name": "name",
        "ShortName": "short_name",
        "Description": "description"
    }

    # QUEST 类型（小驼峰命名）
    quest_suffix_map = {
        "name": "name",
        "description": "description",
        "failMessageText": "fail_message",
        "successMessageText": "success_message",
        "acceptPlayerMessage": "accept_player_message",
        "declinePlayerMessage": "decline_player_message",
        "completePlayerMessage": "complete_player_message"
    }

    grouped_data = defaultdict(lambda: {
        "item_id": None,
        "name": None,
        "short_name": None,
        "description": None,
        "fail_message": None,
        "success_message": None,
        "accept_player_message": None,
        "decline_player_message": None,
        "complete_player_message": None,
        "other_value": "",
        "type": "OTHER"
    })

    for key, value in raw_data.items():
        parts = key.strip().rsplit(" ", 1)
        if len(parts) == 2:
            entity_id, suffix = parts
            if suffix in item_suffix_map:
                field = item_suffix_map[suffix]
                grouped_data[entity_id][field] = value
                grouped_data[entity_id]["type"] = "ITEM"
            elif suffix in quest_suffix_map:
                field = quest_suffix_map[suffix]
                grouped_data[entity_id][field] = value
                grouped_data[entity_id]["type"] = "QUEST"
            else:
                grouped_data[entity_id]["other_value"] += f"{key}: {value}\n"
        else:
            entity_id = key
            grouped_data[entity_id]["other_value"] += f"{key}: {value}\n"

        grouped_data[entity_id]["item_id"] = entity_id

    return list(grouped_data.values())


def save_language_data(data_list: list[dict]) -> None:
    """
    将语言数据写入 language_info 表中。
    要求 data_list 中每个 dict 包含 type 字段（ITEM / QUEST / OTHER）。
    """
    db_path = get_db_path("app.db")
    if not data_list:
        print("[警告] 无语言数据可保存")
        return

    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            # 清空旧数据，避免重复插入
            cursor.execute(SQL_QUERIES.get("delete_language_info"))

            # 插入新数据（需包含 type 字段）
            cursor.executemany(SQL_QUERIES.get("get_language_info"), data_list)
            conn.commit()
            print(f"[成功] 共插入 {len(data_list)} 条语言数据")

    except Exception as e:
        print(f"[错误] 插入 language_info 数据失败: {e}")


def search_language_info(keyword: str) -> list[dict]:
    db_path = get_db_path("app.db")
    sql = SQL_QUERIES.get("search_data")
    if not sql:
        print("[错误] SQL 未找到：search_language_info")
        return []

    try:
        with sqlite3.connect(db_path) as conn:
            conn.row_factory = sqlite3.Row  # 支持 dict 结果
            cursor = conn.cursor()
            params = [keyword] * 10  # 每个字段都 LIKE 一次
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    except Exception as e:
        print(f"[错误] 模糊搜索失败: {e}")
        return []


if __name__ == '__main__':
    save_language_data(get_language_data())