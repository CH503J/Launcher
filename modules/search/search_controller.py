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


def search_language_info(value: str, key: str = None) -> list[dict]:
    db_path = get_db_path("app.db")

    try:
        with sqlite3.connect(db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            if key is None:
                # 全字段模糊匹配（search_data）
                sql = SQL_QUERIES.get("search_data")
                if not sql:
                    print("[错误] SQL 未找到：search_data")
                    return []
                cursor.execute(sql, [value] * 10)

            elif key == "other":
                # 构造临时 SQL 拼接 OTHER_FIELDS
                conditions = [f"{field} LIKE ?" for field in OTHER_FIELDS]
                sql = f"SELECT * FROM language_info WHERE {' OR '.join(conditions)}"
                cursor.execute(sql, [f"%{value}%"] * len(OTHER_FIELDS))

            elif key in SEARCHABLE_FIELDS and key != "other":
                # 使用 search_data_by_field 模板
                raw_sql = SQL_QUERIES.get("search_data_by_field")
                if not raw_sql:
                    print("[错误] SQL 未找到：search_data_by_field")
                    return []
                sql = raw_sql.format(key=key)
                cursor.execute(sql, (f"%{value}%",))

            else:
                print(f"[警告] 非法字段名：{key}")
                return []

            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    except Exception as e:
        print(f"[错误] 模糊搜索失败: {e}")
        return []
