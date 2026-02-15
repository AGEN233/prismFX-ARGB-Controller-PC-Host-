from PySide6.QtWidgets import QWidget, QVBoxLayout
from qfluentwidgets import TitleLabel, BodyLabel

class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("pageHome")

        v = QVBoxLayout(self)
        v.setContentsMargins(24, 24, 24, 24)
        v.setSpacing(12)
        v.addWidget(TitleLabel("主页"))
        v.addWidget(BodyLabel("这里放快捷入口/概览信息（先占位）"))
        v.addStretch(1)
