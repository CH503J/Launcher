#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :search_ui.py
# @Time      :2025/7/9 14:34
# @Author    :CH503J
import json

from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QComboBox,
    QWidget,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem
)

from modules.search.search_controller import search_language_info

SEARCHABLE_FIELDS_MAP = {
    "item_id": "物品ID",
    "name": "物品全名",
    "short_name": "物品短名",
    "description": "描述",
    "other": "其他"
}


class SearchTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # --- 搜索区域 ---
        search_layout = QHBoxLayout()
        self.key_selector = QComboBox()
        # self.key_selector.addItems(SEARCHABLE_FIELDS)
        for key, label in SEARCHABLE_FIELDS_MAP.items():
            self.key_selector.addItem(label, key)

        self.input_value = QLineEdit()
        self.input_value.setPlaceholderText("请输入搜索关键词（仅支持单字段）")

        self.search_btn = QPushButton("搜索")
        self.search_btn.clicked.connect(self.do_search)

        search_layout.addWidget(QLabel("字段："))
        search_layout.addWidget(self.key_selector)
        search_layout.addWidget(self.input_value)
        search_layout.addWidget(self.search_btn)

        # --- 结果展示区域 ---
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(0)
        self.result_table.setRowCount(0)
        self.result_table.setAlternatingRowColors(True)
        self.result_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        self.result_count_label = QLabel("")  # 查询条数统计

        # --- 布局添加 ---
        layout.addLayout(search_layout)
        layout.addWidget(self.result_table)
        layout.addWidget(self.result_count_label)  # 显示结果数量

        self.setLayout(layout)

    def do_search(self):
        key = self.key_selector.currentData()
        value = self.input_value.text().strip()

        self.result_table.clearContents()
        self.result_table.setRowCount(0)
        self.result_count_label.clear()

        if not value:
            self.result_count_label.setText("[提示] 请输入搜索值")
            return

        try:
            results = search_language_info(value, key)
            if not results:
                self.result_count_label.setText("无匹配结果")
                return

            # 表头字段来自第一条记录的 key
            headers = [key for key in results[0].keys() if key != "id"]
            self.result_table.setColumnCount(len(headers))
            self.result_table.setHorizontalHeaderLabels(headers)
            self.result_table.setRowCount(len(results))

            # 填充表格数据
            for row_idx, row_data in enumerate(results):
                for col_idx, field in enumerate(headers):
                    value = str(row_data.get(field, ""))
                    self.result_table.setItem(row_idx, col_idx, QTableWidgetItem(value))

            self.result_count_label.setText(f"查询结果：{len(results)} 条")

        except Exception as e:
            self.result_count_label.setText(f"[错误] 查询失败: {e}")
