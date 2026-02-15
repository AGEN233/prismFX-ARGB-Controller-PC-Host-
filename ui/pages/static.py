from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFrame
from PySide6.QtCore import Qt
from qfluentwidgets import (
    TitleLabel, BodyLabel, SubtitleLabel, CaptionLabel,
    CardWidget, SwitchButton, Slider,
    TransparentToolButton, FluentIcon as FIF
)
from PySide6.QtGui import QColor
from ui.widgets.color_wheel import ColorWheel


class StaticPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("pageStatic")

        self._build_root()

    # 色盘预览事件回调
    def _wheel_is_Preview_handle(self, h: int, s: int):
        self._update_current_color_card_ui(h, s)

    # 当前颜色卡片更新
    def _update_current_color_card_ui(self, h: int, s: int):
        color = QColor()
        color.setHsv((h % 360), max(0, min(255, s)), 255)

        color_hex = color.name(QColor.NameFormat.HexRgb).upper()
        self.hexLabel.setText(color_hex)

        self.colorSwatch.setStyleSheet(
            f"border-radius:8px; background:{color_hex}; border:1px solid rgba(0,0,0,0.08);"
        )

    # 更新开关卡片，但不触发发送
    def _update_power_card_ui(self, sw: bool):
        self.powerSwitch.blockSignals(True)
        self.powerSwitch.setChecked(sw)
        self.powerSwitch.blockSignals(False)

    def _on_change_br_preview_handle(self,  v: int):
        self.brightValue.setText(f"{v}%")

    def _on_change_br_commit_handle(self):
        pass

    # 根布局
    def _build_root(self):
        self.root = QVBoxLayout(self)
        self.root.setContentsMargins(24, 24, 24, 24)
        self.root.setSpacing(16)
        self.root.addWidget(TitleLabel("静态模式"))

        self._build_split()
        
    # 分栏容器
    def _build_split(self):
        self.content = QHBoxLayout()
        self.content.setSpacing(16)
        self.root.addLayout(self.content, 1)

        self.left = QWidget()
        self.right = QWidget()

        self.leftLay = QVBoxLayout(self.left)
        self.leftLay.setContentsMargins(0, 0, 0, 0)
        self.leftLay.setSpacing(12)

        self.rightLay = QVBoxLayout(self.right)
        self.rightLay.setContentsMargins(0, 0, 0, 0)
        self.rightLay.setSpacing(12)

        self.content.addWidget(self.left, 3)
        self.content.addWidget(self.right, 2)

        self._build_left_panel()
        self._build_right_panel()

    # 左布局
    def _build_left_panel(self):
        self.leftLay.addStretch()
        self._build_left_color_wheel()     # 模块1：色盘
        # self._build_left_presets()       # 模块2：预设（以后加）
        # self._build_left_favorites()     # 模块3：收藏（以后加）
        self.leftLay.addStretch()

    ## 色盘
    def _build_left_color_wheel(self):

        self.wheel = ColorWheel()
        self.wheel.setMinimumSize(360, 360)
        self.wheel.setMaximumSize(480, 480)
        self.leftLay.addWidget(self.wheel, 0, Qt.AlignmentFlag.AlignCenter)
        self.wheel.hsPreview.connect(self._wheel_is_Preview_handle)

    # 右布局
    def _build_right_panel(self):
        self.powerCard = self._build_right_power_card()
        self.colorCard = self._build_right_current_color_card()
        self.brightCard = self._build_brightness_card()

        self.rightLay.addWidget(self.powerCard)
        self.rightLay.addWidget(self.colorCard)
        self.rightLay.addWidget(self.brightCard)

        self.rightLay.addStretch(1)

    ## 右开关卡
    def _build_right_power_card(self) -> CardWidget:
        card = CardWidget()
        card.setFixedHeight(73)

        lay = QHBoxLayout(card)
        lay.setContentsMargins(20, 11, 11, 11)
        lay.setSpacing(15)

        title = BodyLabel("开关")
        desc = CaptionLabel("灯光电源")
        desc.setTextColor("#606060", "#d2d2d2")

        textLay = QVBoxLayout()
        textLay.setSpacing(0)
        textLay.addWidget(title)
        textLay.addWidget(desc)
        textLay.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self.powerSwitch = SwitchButton()
        self.powerSwitch.setChecked(False)
        self.powerSwitch.setOnText("开灯")
        self.powerSwitch.setOffText("关灯")

        lay.addLayout(textLay)
        lay.addStretch(1)
        lay.addWidget(self.powerSwitch, 0, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        return card

    ## 右 当前颜色卡
    def _build_right_current_color_card(self) -> CardWidget:
        card = CardWidget()
        card.setFixedHeight(73)

        lay = QHBoxLayout(card)
        lay.setContentsMargins(20, 11, 11, 11)
        lay.setSpacing(15)

        title = BodyLabel("当前颜色")
        desc = CaptionLabel("HEX")
        desc.setTextColor("#606060", "#d2d2d2")

        textLay = QVBoxLayout()
        textLay.setSpacing(0)
        textLay.addWidget(title)
        textLay.addWidget(desc)
        textLay.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self.colorSwatch = QFrame()
        self.colorSwatch.setFixedSize(28, 28)
        self.colorSwatch.setStyleSheet(
            "border-radius:8px; background:#FF8844; border:1px solid rgba(0,0,0,0.08);"
        )

        self.hexLabel = BodyLabel("#FFFFFF")

        self.copyBtn = TransparentToolButton(FIF.COPY)
        self.copyBtn.setFixedSize(32, 32)

        lay.addLayout(textLay)
        lay.addStretch(1)
        lay.addWidget(self.colorSwatch, 0, Qt.AlignmentFlag.AlignVCenter)
        lay.addWidget(self.hexLabel, 0, Qt.AlignmentFlag.AlignVCenter)
        lay.addWidget(self.copyBtn, 0, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        return card

   ## 右 亮度卡 
    def _build_brightness_card(self) -> CardWidget:
        card = CardWidget()
        card.setMinimumHeight(96)

        lay = QVBoxLayout(card)
        lay.setContentsMargins(20, 11, 11, 11)
        lay.setSpacing(6)

        topRow = QHBoxLayout()

        title = BodyLabel("亮度")
        desc = CaptionLabel("全局统一亮度")
        desc.setTextColor("#606060", "#d2d2d2")

        textLay = QVBoxLayout()
        textLay.setSpacing(0)
        textLay.addWidget(title)
        textLay.addWidget(desc)

        self.brightValue = BodyLabel("80%")

        topRow.addLayout(textLay)
        topRow.addStretch(1)
        topRow.addWidget(self.brightValue, 0, Qt.AlignmentFlag.AlignVCenter)

        self.slider = Slider(Qt.Orientation.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.setValue(80)

        self.slider.valueChanged.connect(self._on_change_br_preview_handle)
        self.slider.sliderReleased.connect(self._on_change_br_commit_handle)

        lay.addLayout(topRow)
        lay.addWidget(self.slider)

        return card

