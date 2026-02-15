from PySide6.QtWidgets import QWidget, QVBoxLayout
from qfluentwidgets import TitleLabel, BodyLabel

class ConnectPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("pageConnect")

        v = QVBoxLayout(self)
        v.setContentsMargins(24, 24, 24, 24)
        v.setSpacing(12)
        v.addWidget(TitleLabel("设备连接"))
        v.addWidget(BodyLabel("这里后面接扫描/连接逻辑"))
        v.addStretch(1)
