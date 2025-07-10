#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :about_controller.py
# @Time      :2025/7/8
# @Author    :CH503J

import os
import sqlite3
from modules.common.path_utils import get_db_path, get_sql_path
from modules.common.sql_loader import load_sql_queries

# 加载 SQL 查询语句
SQL_QUERIES = load_sql_queries(get_sql_path("about_info.sql"))


def get_app_info() -> dict:
    """
    从 about_info 表中读取应用程序信息，包括名称、版本号、作者、GitHub链接等。
    :return: 字典形式的应用信息（字段名为键），读取失败时返回空字典。
    """
    db_path = get_db_path("app.db")
    if not os.path.exists(db_path):
        print("[错误] 找不到数据库文件")
        return {}

    sql = SQL_QUERIES.get("get_app_info")
    if not sql:
        print("[错误] 缺少 SQL 语句：get_app_info")
        return {}

    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            row = cursor.fetchone()
            if row:
                return dict(zip([desc[0] for desc in cursor.description], row))
    except Exception as e:
        print(f"[错误] 读取 about_info 失败: {e}")

    return {}
