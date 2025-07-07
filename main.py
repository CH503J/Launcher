#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :main
# @Time      :2025/7/4 20:16
# @Author    :CH503J
import sys

from PyQt6.QtWidgets import QApplication

from modules.mainui.main_ui import MainWindow


# 获取项目结构命令   tree /F > structure.txt
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())