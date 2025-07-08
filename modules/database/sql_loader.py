#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :sql_loader.py
# @Time      :2025/7/7 15:19
# @Author    :CH503J

def load_sql_queries(file_path: str) -> dict:
    """
    加载 SQL 文件中的命名查询语句
    支持的格式如下（通过注释 -- name: query_name 分隔）:
        -- name: get_app_info
        SELECT * FROM about_info;
        -- name: update_version
        UPDATE about_info SET version = ?;
    :param file_path: SQL 文件的路径（.sql 文件）
    :return: dict，key 为 SQL 名称，value 为对应的 SQL 字符串
    """
    queries = {}
    current_key = None
    buffer = []

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip().startswith('-- name:'):
                if current_key:
                    queries[current_key] = ''.join(buffer).strip()
                    buffer.clear()
                current_key = line.strip().split('-- name:')[1].strip()
            else:
                buffer.append(line)

        # 最后一段 SQL 添加进去
        if current_key:
            queries[current_key] = ''.join(buffer).strip()

    return queries
