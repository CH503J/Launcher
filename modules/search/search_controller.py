#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :search_controller.py
# @Time      :2025/7/9 14:34
# @Author    :CH503J


import sqlite3

from modules.common.path_utils import get_db_path, get_sql_path
from modules.database.sql_loader import load_sql_queries

SQL_QUERIES = load_sql_queries(get_sql_path("language_info.sql"))

SEARCHABLE_FIELDS = [
    "item_id", "name", "short_name", "description", "other"
]

OTHER_FIELDS = [
    "fail_message", "success_message",
    "accept_player_message", "decline_player_message",
    "complete_player_message", "other_value"
]


def search_language_info(value: str, type_filter: str = "ALL") -> list[dict]:
    db_path = get_db_path("app.db")

    try:
        with sqlite3.connect(db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            sql_key = "search_data_all" if type_filter == "ALL" else "search_data_by_type"
            sql = SQL_QUERIES.get(sql_key)
            if not sql:
                print(f"[错误] SQL 未找到：{sql_key}")
                return []

            kw = f"%{value}%"
            if type_filter == "ALL":
                cursor.execute(sql, {"kw": kw})
            else:
                cursor.execute(sql, {"kw": kw, "type": type_filter})

            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    except Exception as e:
        print(f"[错误] 模糊搜索失败: {e}")
        return []