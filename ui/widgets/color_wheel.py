import math
from PySide6.QtCore import (Qt, Signal, QPoint)
from PySide6.QtGui import (QColor, QPainter, QImage, QPen, QConicalGradient, QRadialGradient, QBrush)
from PySide6.QtWidgets import QWidget

def _clamp(v: int, lo: int, hi: int) -> int:
    # 将数值限制在 [lo, hi] 区间
    return lo if v < lo else hi if v > hi else v

class ColorWheel(QWidget):
    hsPreview = Signal(int, int)
    hsCommit = Signal(int, int)


    def __init__(self, parent=None):
        super().__init__(parent)
        self._pressed = False
        self.setMinimumSize(240, 240)

        self._h = 0
        self._s = 255

        self._img: QImage | None = None
        self._center = QPoint(0, 0)
        self._radius = 1

        self.setMouseTracking(True) # 鼠标跟踪

    # 鼠标点击事件
    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self._pressed = True
            self._pick(e.position().toPoint(), commit=False) 

    # 鼠标松手事件
    def mouseReleaseEvent(self, e):
        self._pressed = False
        self._pick(e.position().toPoint(), commit=True)

    # 鼠标拖动事件
    def mouseMoveEvent(self, e):
        if e.buttons() & Qt.MouseButton.LeftButton:
            self._pick(e.position().toPoint(), commit=False)

    def hs(self) -> tuple[int, int]:
        return self._h, self._s
    
    # 设置HS
    def setHS(self, h: int, s: int, commit: bool = False):
        h = _clamp(int(h), 0, 359)
        s = _clamp(int(s), 0, 255)

        changed = (h, s) != (self._h, self._s)
        self._h, self._s = h, s

        # 拖动时只要变化就发预览
        if changed and not commit:
            self.hsPreview.emit(self._h, self._s)

        # 松手提交
        if commit:
            self.hsCommit.emit(self._h, self._s)

        if changed or commit:
            self.update()
    
    # 鼠标滴管
    def _pick(self, pos: QPoint, commit:bool=False):
        # 鼠标坐标转HS
        dx = pos.x() - self._center.x()
        dy = pos.y() - self._center.y()

        r = math.hypot(dx, dy)

        if r > self._radius and r != 0:
            scale = self._radius / r
            dx *= scale
            dy *= scale
            r = self._radius

        # 角度转 Hue
        ang = math.degrees(math.atan2(-dy, dx))
        if ang < 0:
            ang += 360.0

        h = int(ang) % 360

        # 半径转 Saturation
        s = int(_clamp(int(r / self._radius * 255), 0, 255))

        self.setHS(h, s, commit)

    # 渲染色盘
    def _drawPalette(self):
        w, h = max(1, self.width()), max(1, self.height())
        size = min(w, h)

        self._radius = max(1, (size // 2) - 2)
        self._center = QPoint(w // 2, h // 2)

        img = QImage(w, h, QImage.Format.Format_ARGB32_Premultiplied)
        img.fill(Qt.GlobalColor.transparent)

        p = QPainter(img)
        p.setRenderHint(QPainter.RenderHint.Antialiasing, True)

        conical = QConicalGradient(self._center, 0)

        conical.setColorAt(0.0, QColor(255, 0, 0))
        conical.setColorAt(1/6, QColor(255, 255, 0))
        conical.setColorAt(2/6, QColor(0, 255, 0))
        conical.setColorAt(3/6, QColor(0, 255, 255))
        conical.setColorAt(4/6, QColor(0, 0, 255))
        conical.setColorAt(5/6, QColor(255, 0, 255))
        conical.setColorAt(1.0, QColor(255, 0, 0))

        p.setBrush(QBrush(conical))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawEllipse(self._center, self._radius, self._radius)

        radial = QRadialGradient(self._center, self._radius)

        radial.setColorAt(0.0, QColor(255, 255, 255))
        radial.setColorAt(1.0, QColor(255, 255, 255, 0))

        p.setBrush(QBrush(radial))
        p.drawEllipse(self._center, self._radius, self._radius)

        p.end()

        self._img = img
        self.update()

    # 选中点画图事件
    def paintEvent(self, e):
        p = QPainter(self)

        try:
            p.setRenderHint(QPainter.RenderHint.Antialiasing, True)

            img = self._img
            if img is None:
                self._drawPalette()
                img = self._img
            if img is None :
                return

            p.drawImage(QPoint(0, 0), img)

            p.setPen(QPen(Qt.GlobalColor.black, 1))
            p.drawEllipse(self._center, self._radius, self._radius)


            # ---------- 画当前选中点 ----------

            r = (self._s / 255.0) * self._radius    # 半径比
            theta = math.radians(self._h)           # 角度转弧度 

            # 极坐标 -> 平面直角坐标
            x = int(self._center.x() + r * math.cos(theta))
            y = int(self._center.y() - r * math.sin(theta))

            pt = QPoint(x, y)

            # 根据按压状态决定大小
            base_r = 8
            draw_r = 12 if self._pressed else base_r

            # 阴影
            p.setPen(Qt.PenStyle.NoPen)
            p.setBrush(QColor(0, 0, 0, 30))
            p.drawEllipse(QPoint(pt.x() + 2, pt.y() + 2), draw_r, draw_r)

            # 主体
            c = QColor()
            c.setHsv(self._h, self._s, 255)
            p.setBrush(c)
            p.drawEllipse(pt, draw_r - 1, draw_r - 1)

            # 白描边
            p.setPen(QPen(QColor(255, 255, 255, 220), 2))
            p.setBrush(Qt.BrushStyle.NoBrush)
            p.drawEllipse(pt, draw_r - 1, draw_r - 1)

        finally:
            p.end()
