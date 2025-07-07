#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :sql_manager.py
# @Time      :2025/7/7 17:53
# @Author    :CH503J


def load_sql_queries(file_path: str) -> dict:
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
        if current_key:
            queries[current_key] = ''.join(buffer).strip()
    return queries