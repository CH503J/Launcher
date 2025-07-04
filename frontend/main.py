import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt + Flask DEMO")
        self.setGeometry(200, 200, 300, 150)

        self.label = QLabel("点击按钮获取后端数据")
        self.button = QPushButton("调用后端 API")
        self.button.clicked.connect(self.call_api)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def call_api(self):
        try:
            res = requests.get("http://127.0.0.1:5000/api/hello")
            self.label.setText(res.json()["message"])
        except Exception as e:
            self.label.setText("后端服务未响应")

def run_gui():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())