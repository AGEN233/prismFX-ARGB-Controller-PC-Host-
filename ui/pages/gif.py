from PySide6.QtWidgets import QWidget, QVBoxLayout
from qfluentwidgets import TitleLabel, BodyLabel

class GifPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("pageGif")

        v = QVBoxLayout(self)
        v.setContentsMargins(24, 24, 24, 24)
        v.setSpacing(12)
        v.addWidget(TitleLabel("GIF 模式（预留）"))
        v.addWidget(BodyLabel("占位"))
        v.addStretch(1)
