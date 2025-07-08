#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :path_utils.py
# @Time      :2025/7/8 09:58
# @Author    :CH503J


import os
import sys


def get_db_path(db_file_name: str = "app.db") -> str:
    """
    获取指定数据库文件的路径
    - 开发阶段：使用项目内路径 ./config/database/{db_file_name}
    - 打包后：使用安装目录下的 ./config/{db_file_name}
    :param db_file_name: 数据库文件名（默认为 app.db）
    :return: 完整路径
    """
    if getattr(sys, 'frozen', False):
        # 打包后的运行路径
        base_dir = os.path.dirname(sys.executable)
        return os.path.join(base_dir, "config", db_file_name)
    else:
        # 开发阶段路径
        base_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "config", "database")
        )
        return os.path.join(base_dir, db_file_name)


def get_sql_path(sql_file_name: str = "about_info.sql") -> str:
    """
    获取 SQL 文件的完整路径
    - 开发环境：使用项目根目录下的 ./sql/{file_name}
    - 打包环境：使用安装根目录下的 ./sql/{file_name}
    :param sql_file_name: SQL 文件名，默认为 about_info.sql
    :return: SQL 文件的绝对路径
    """
    if getattr(sys, 'frozen', False):
        # PyInstaller 打包运行时
        base_dir = os.path.dirname(sys.executable)
    else:
        # 开发环境
        base_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..")
        )
    return os.path.join(base_dir, "sql", sql_file_name)
