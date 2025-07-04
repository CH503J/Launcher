#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :main_ui.py
# @Time      :2025/7/4 15:16
# @Author    :CH503J


import sys

from PyQt6.QtCore import (
    Qt,
    QTimer,
    QPoint
)
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
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Launcher 主界面")
        self.setGeometry(100, 100, 1200, 600)

        # 创建标签页控件
        tabs = QTabWidget()
        self.launcher_tab = LauncherTab(parent=self)
        tabs.addTab(self.launcher_tab, "启停")
        tabs.addTab(AboutTab(), "关于")

        # 设置中央窗口部件
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(tabs)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def show_toast(self, message: str, position: str = "top-right"):
        # todo 后期可将这个气泡位置的参数改为用户自定义
        """
        在主窗口中弹出一个提示气泡
        position中额参数可填 top-left、top-right、bottom-left、bottom-right、center
        """
        ToastNotification(self, message, duration=3000, position=position)


class ToastNotification(QLabel):
    def __init__(self, parent, message: str, duration=3000, position="top-left"):
        super().__init__(parent)
        self.setText(message)
        # todo 气泡样式现在只能显示文字而没有气泡效果
        self.setStyleSheet("""
            QLabel {
                background-color: #222;        /* 深灰背景，适合黑色UI */
                color: #fff;                   /* 白色文字 */
                padding: 10px 20px;
                border-radius: 8px;
                font-size: 14px;
                border: 1px solid #555;        /* 细边框，略微区分背景 */
            }
        """)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.ToolTip)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.adjustSize()
        self.position = position
        self.bubble_position()  # 自动定位
        self.show()

        # 自动关闭
        QTimer.singleShot(duration, self.close)

    def bubble_position(self):
        """将气泡定位到窗口内部指定位置"""
        if not self.parent():
            return

        # 获取父窗口在屏幕上的位置和大小
        parent_geo = self.parent().geometry()
        x0 = parent_geo.x()
        y0 = parent_geo.y()
        w = parent_geo.width()
        h = parent_geo.height()
        bubble_w = self.width()
        bubble_h = self.height()
        margin = 20

        # 各种位置的偏移计算
        if self.position == "top-left":
            x = x0 + margin
            y = y0 + margin
        elif self.position == "top-right":
            x = x0 + w - bubble_w - margin
            y = y0 + margin
        elif self.position == "bottom-left":
            x = x0 + margin
            y = y0 + h - bubble_h - margin
        elif self.position == "bottom-right":
            x = x0 + w - bubble_w - margin
            y = y0 + h - bubble_h - margin
        elif self.position == "center":
            x = x0 + (w - bubble_w) // 2
            y = y0 + (h - bubble_h) // 2
        else:
            x = x0 + w - bubble_w - margin
            y = y0 + margin

        self.move(x, y)


# 仅当直接运行此文件时，启动窗口（用于测试）
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
