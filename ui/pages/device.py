from PySide6.QtWidgets import QWidget, QVBoxLayout
from qfluentwidgets import TitleLabel, BodyLabel

class DevicePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("pageDevice")

        v = QVBoxLayout(self)
        v.setContentsMargins(24, 24, 24, 24)
        v.setSpacing(12)
        v.addWidget(TitleLabel("设备信息"))
        v.addWidget(BodyLabel("占位"))
        v.addStretch(1)
