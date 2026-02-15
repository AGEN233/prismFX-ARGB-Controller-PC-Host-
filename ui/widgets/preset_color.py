from PySide6.QtWidgets import QFrame
from PySide6.QtCore import Qt, Signal
from qfluentwidgets import BodyLabel

class PresetColorTile(QFrame):
    clicked = Signal(str)

    def __init__(self, hex_color: str, size: int = 44, parent=None):
        super().__init__(parent)
        self._hex = hex_color.upper()

        self.setFixedSize(size, size)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # 勾选角标
        self._check = BodyLabel("✓", self)
        self._check.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._check.setFixedSize(18, 18)
        self._check.move(size - 18 - 6, 6)
        self._check.hide()
        self._check.setStyleSheet(
            "border-radius:9px; background:rgba(0,0,0,0.72); color:white; font-weight:700;"
        )

        self.setStyleSheet(
            f"border-radius:6px; background:{self._hex}; border:1px solid rgba(0,0,0,0.10);"
        )

    def hex(self) -> str:
        return self._hex

    def setSelected(self, on: bool):
        self._check.setVisible(on)

    def mousePressEvent(self, e):
        self.clicked.emit(self._hex)
        super().mousePressEvent(e)
