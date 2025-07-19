import requests
import os
def resource_path(relative_path):
    """PyInstaller兼容的资源文件路径获取方式"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QTextEdit, QHBoxLayout, QFrame, QSizePolicy, QSpacerItem, QComboBox
)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
import sys

class SubmitApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('人大研学中心智能预约助手')
        self.resize(620, 940)
        # 图标，可选
        self.setWindowIcon(QIcon(resource_path("ruc_logo.png")))


        self.setStyleSheet("""
            QWidget {
                background: #f5f7fb;
                font-family: "HarmonyOS Sans", "微软雅黑", Arial, sans-serif;
                font-size: 15px;
            }
            QLineEdit, QComboBox {
                border: 2px solid #e6eaf0;
                border-radius: 12px;
                padding: 10px 14px;
                background: #fff;
                font-size: 16px;
                margin-bottom: 10px;
                box-shadow: 0 1px 8px #ecf0fa;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 2px solid #3570e7;
                background: #f3f6ff;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3570e7, stop:1 #2f64d8);
                color: white;
                font-size: 18px;
                border-radius: 16px;
                padding: 13px 0;
                margin-top: 15px;
                font-weight: 700;
                letter-spacing: 2px;
                box-shadow: 0 2px 16px #dde6fd;
                transition: all 0.2s;
            }
            QPushButton:hover {
                background-color: #20469f;
                letter-spacing: 4px;
            }
            QTextEdit {
                border-radius: 12px;
                background: #f9fafb;
                padding: 10px;
                min-height: 66px;
                border: 1.5px solid #e6eaf0;
                font-size: 15px;
                color: #333;
                box-shadow: 0 2px 8px #f2f3f8;
            }
            QLabel#titleLabel {
                font-size: 23px;
                font-weight: bold;
                color: #2747a6;
                margin-bottom: 8px;
                letter-spacing: 1px;
            }
            QFrame#line {
                background: #e2e6f3;
                min-height: 1px;
                max-height: 1px;
                margin-bottom: 15px;
                margin-top: 6px;
            }
        """)

        self.initUI()
        self.center()

    def initUI(self):
        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(40, 25, 40, 25)
        mainLayout.setSpacing(7)

        # 顶部LOGO和名字
        logoLayout = QHBoxLayout()
        logoLayout.setAlignment(Qt.AlignHCenter)
        
        logo = QLabel()
        logo.setPixmap(QPixmap(resource_path("ruc_logo.png")).scaled(298, 298, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        logo.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        logoLayout.addWidget(logo)
        
        mainLayout.addLayout(logoLayout)

        # 大标题
        title = QLabel("研学中心智能预约助手")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignCenter)
        mainLayout.addWidget(title)

        # 分割线
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setObjectName("line")
        mainLayout.addWidget(line)

        # 输入区域
        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText("学工号 / 统一身份认证账号")
        self.password_edit = QLineEdit()
        self.password_edit.setPlaceholderText("密码")
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.layer_edit = QComboBox()
        self.layer_edit.addItems(["14", "15"])
        self.layer_edit.setEditable(False)
        self.layer_edit.setStyleSheet("margin-bottom:10px;")  # 保持风格统一

        self.seat_edit = QLineEdit()
        self.seat_edit.setPlaceholderText("座位号（1-249，或251）")

        mainLayout.addWidget(self.username_edit)
        mainLayout.addWidget(self.password_edit)
        mainLayout.addWidget(self.layer_edit)
        mainLayout.addWidget(self.seat_edit)

        # 按钮
        self.submitBtn = QPushButton("提交预约信息")
        self.submitBtn.setCursor(Qt.PointingHandCursor)
        self.submitBtn.clicked.connect(self.submit)
        mainLayout.addWidget(self.submitBtn)

        # 日志输出
        self.status = QTextEdit()
        self.status.setReadOnly(True)
        self.status.setPlaceholderText("结果、提示将显示在这里…")
        mainLayout.addWidget(self.status)

        # 留白
        mainLayout.addSpacerItem(QSpacerItem(20, 18, QSizePolicy.Minimum, QSizePolicy.Expanding))
                # GitHub 链接（底部）
        github_link = QLabel()
        github_link.setText(
            "<a href='https://github.com/DuanYi516/RUC-Seat-Select' style='color:#3570e7;font-size:15px;'>"
            "GitHub地址：RUC-Seat-Select"
            "</a>"
        )
        github_link.setOpenExternalLinks(True)
        github_link.setAlignment(Qt.AlignCenter)
        github_link.setStyleSheet("margin-top:15px; margin-bottom:2px;")
        mainLayout.addWidget(github_link)

        self.setLayout(mainLayout)

    def center(self):
        qr = self.frameGeometry()
        cp = QApplication.desktop().screen().rect().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def seat_valid(self, seat_text):
        """校验座位号"""
        try:
            seat = int(seat_text)
            if (1 <= seat <= 249) or seat == 251:
                return True
            else:
                return False
        except:
            return False

    def submit(self):
        username = self.username_edit.text().strip()
        password = self.password_edit.text().strip()
        layer = self.layer_edit.currentText()
        seat = self.seat_edit.text().strip()

        if not (username and password and layer and seat):
            self.status.append("⚠️ <b>请完整填写所有内容</b>")
            return

        if not self.seat_valid(seat):
            self.status.append("❌ <b>座位号只能是1~249或251</b>")
            return

        info = {
            "username": username,
            "password": password,
            "layer": layer,
            "seat": seat
        }

        self.status.append("<span style='color:#3952b3;'>⏳ 正在提交…</span>")
        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            # === 这里请改成你的服务器公网IP ===
            r = requests.post("http://47.94.3.39:8800//submit", json=info, timeout=7)
            if r.status_code == 200:
                self.status.append("<b style='color:#267400;'>✅ 提交成功！请耐心等待系统自动预约。</b>")
            else:
                self.status.append(f"<span style='color:#d9534f;'>❌ 提交失败，状态码：{r.status_code}</span>")
        except Exception as e:
            self.status.append(f"<span style='color:#d9534f;'>🚨 网络错误：{e}</span>")
        QApplication.restoreOverrideCursor()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # 极简/现代风
    window = SubmitApp()
    window.show()
    sys.exit(app.exec_())
