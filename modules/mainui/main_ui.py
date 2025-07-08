#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :main_ui.py
# @Time      :2025/7/4 15:16
# @Author    :CH503J

import sys
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QTabWidget
)

from modules.launcher.launcher_ui import LauncherTab
from modules.settings.settings_ui import AboutTab


class MainWindow(QMainWindow):
    """
    应用程序主窗口
    - 包含多标签页界面（启停页、关于页）
    - 提供气泡提示弹窗（toast）
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Launcher 主界面")
        self.setGeometry(100, 100, 1200, 600)

        # 创建主标签页控件（tab widget）
        tabs = QTabWidget()
        self.launcher_tab = LauncherTab(parent=self)  # 启停服务页面（会传入 main_window 用于调用 toast）
        tabs.addTab(self.launcher_tab, "启停")

        # 关于页面（软件信息展示、路径设置）
        tabs.addTab(AboutTab(), "关于")

        # 设置主界面中央部件布局
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(tabs)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def show_toast(self, message: str, position: str = "top-right"):
        """
        显示气泡提示（默认右上角）
        支持的位置参数有：
        - top-left, top-right, bottom-left, bottom-right, center
        """
        ToastNotification(self, message, duration=3000, position=position)


class ToastNotification(QLabel):
    """
    浮动气泡提示组件（无边框 QLabel）
    自动定位 + 定时消失
    """

    def __init__(self, parent, message: str, duration=3000, position="top-left"):
        super().__init__(parent)
        self.setText(message)

        # 设置样式（深色浮窗）
        self.setStyleSheet("""
            QLabel {
                background-color: #222;  /* 深灰背景 */
                color: #fff;             /* 白色文字 */
                padding: 10px 20px;
                border-radius: 8px;
                font-size: 14px;
                border: 1px solid #555;
            }
        """)

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.ToolTip)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.adjustSize()

        self.position = position
        self.bubble_position()
        self.show()

        # 延迟关闭
        QTimer.singleShot(duration, self.close)

    def bubble_position(self):
        """计算气泡在主窗口中的浮动位置"""
        if not self.parent():
            return

        parent_geo = self.parent().geometry()
        x0, y0 = parent_geo.x(), parent_geo.y()
        w, h = parent_geo.width(), parent_geo.height()
        bubble_w, bubble_h = self.width(), self.height()
        margin = 20

        if self.position == "top-left":
            x, y = x0 + margin, y0 + margin
        elif self.position == "top-right":
            x, y = x0 + w - bubble_w - margin, y0 + margin
        elif self.position == "bottom-left":
            x, y = x0 + margin, y0 + h - bubble_h - margin
        elif self.position == "bottom-right":
            x, y = x0 + w - bubble_w - margin, y0 + h - bubble_h - margin
        elif self.position == "center":
            x, y = x0 + (w - bubble_w) // 2, y0 + (h - bubble_h) // 2
        else:
            x, y = x0 + w - bubble_w - margin, y0 + margin  # 默认 top-right

        self.move(x, y)
