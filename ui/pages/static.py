from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFrame, QApplication, QGridLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont
from qfluentwidgets import (
    TitleLabel, BodyLabel, CaptionLabel, IconWidget,
    CardWidget, SwitchButton, Slider, Flyout, InfoBarIcon,
    TransparentToolButton, FluentIcon, HeaderCardWidget
)

from ui.widgets.color_wheel import ColorWheel
from ui.widgets.preset_color import PresetColorTile


class StaticPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("pageStatic")

        self._build_root()

        self.static_color_update(33, 255, source="external")
        self.static_brightness_update(80, source="external")

    # 色盘预览事件回调
    def _wheel_is_Preview_handle(self, h: int, s: int):
        self.static_color_update(h, s, source="wheel")

    # 当前颜色卡片更新（只用 HS；V 固定 255 用来显示纯色）
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

    # 亮度变化预览
    def _on_change_br_preview_handle(self, v_percent: int):
        self.static_brightness_update(v_percent, source="slider")
     
    # 亮度变化提交
    def _on_change_br_commit_handle(self):
        pass

    # 当前颜色复制事件
    def _current_color_copy_btn_click_handle(self):
        QApplication.clipboard().setText(self.hexLabel.text())

        Flyout.create(
            icon=InfoBarIcon.SUCCESS,
            title="复制成功",
            content=f'当前颜色 '
                    f'<span style="background:{self.hexLabel.text()}; color:white; '
                    f'padding:1px 6px; border-radius:4px; '
                    f'font-family:Consolas;">{self.hexLabel.text()}</span> '
                    f'已复制至粘贴板',
            isClosable=True,
            parent=self,
            target=self.copyBtn
        )

    # 预设颜色点击事件
    def _preset_color_btn_click_handle(self, hex_color: str):
        h, s = self._hex_to_hs(hex_color)
        if h is None:
            return
        self.static_color_update(h, s)

    def _hex_to_hs(self, hex_color: str):
        c = QColor((hex_color or "").upper())
        if not c.isValid():
            return (None, None)

        h, s, _v, _a = c.getHsv()
        if h < 0:
            h = 0
        return (h, s)

    # 统一更新接口
    def static_color_update(self, h: int, s: int, *, source: str | None = None):
        h = int(h) % 360
        s = int(max(0, min(255, int(s))))

        self._hs = (h, s)

        self._update_current_color_card_ui(h, s)

        if source != "wheel":
            self.wheel.blockSignals(True)
            self.wheel.setHS(h, s, False)
            self.wheel.blockSignals(False)

    # 统一亮度更新
    def static_brightness_update(self, br_percent: int, *, source: str | None = None):
        br_percent = int(max(0, min(100, int(br_percent))))

        self.brightValue.setText(f"{br_percent}%")

        if source != "slider":
            self.slider.blockSignals(True)
            self.slider.setValue(br_percent)
            self.slider.blockSignals(False)

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

        # 初始用 wheel 的当前位置刷新一次右侧色卡（不反写 wheel）
        h, s = self.wheel.hs()
        self.static_color_update(h, s, source="wheel")

    # 左布局
    def _build_left_panel(self):
        self.leftLay.addStretch()
        self._build_left_color_wheel()     # 模块1：色盘
        # self._build_left_presets()       # 模块2：预设（以后加）
        # self._build_left_favorites()     # 模块3：收藏（以后加）
        self.leftLay.addStretch(0)

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
        self.brightCard = self._build_right_brightness_card()
        self.presetColor = self._build_right_preset_color()

        self.rightLay.addWidget(self.powerCard)
        self.rightLay.addWidget(self.colorCard)
        self.rightLay.addWidget(self.brightCard)
        self.rightLay.addWidget(self.presetColor)

        self.rightLay.addStretch(1)

    ## 右开关卡
    def _build_right_power_card(self) -> CardWidget:
        card = CardWidget()
        card.setFixedHeight(73)

        lay = QHBoxLayout(card)
        lay.setContentsMargins(20, 11, 11, 11)
        lay.setSpacing(15)

        icon = IconWidget(FluentIcon.POWER_BUTTON)
        icon.setFixedSize(20, 20)

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

        lay.addWidget(icon, 0, Qt.AlignmentFlag.AlignVCenter)
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

        icon = IconWidget(FluentIcon.BACKGROUND_FILL)
        icon.setFixedSize(20, 20)

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

        self.copyBtn = TransparentToolButton(FluentIcon.COPY)
        self.copyBtn.setFixedSize(32, 32)
        self.copyBtn.clicked.connect(self._current_color_copy_btn_click_handle)

        lay.addWidget(icon, 0, Qt.AlignmentFlag.AlignVCenter)
        lay.addLayout(textLay)
        lay.addStretch(1)
        lay.addWidget(self.colorSwatch, 0, Qt.AlignmentFlag.AlignVCenter)
        lay.addWidget(self.hexLabel, 0, Qt.AlignmentFlag.AlignVCenter)
        lay.addWidget(self.copyBtn, 0, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        return card

    ## 右 亮度卡 
    def _build_right_brightness_card(self) -> CardWidget:
        card = CardWidget()
        card.setFixedHeight(73)

        lay = QHBoxLayout(card)
        lay.setContentsMargins(20, 12, 16, 12)
        lay.setSpacing(12)

        # 左侧图标
        icon = IconWidget(FluentIcon.BRIGHTNESS)
        icon.setFixedSize(20, 20)

        title = BodyLabel("亮度")
        desc = CaptionLabel("更改灯光亮度")
        desc.setTextColor("#606060", "#d2d2d2")

        textLay = QVBoxLayout()
        textLay.setContentsMargins(0, 0, 0, 0)
        textLay.setSpacing(2)
        textLay.addWidget(title)
        textLay.addWidget(desc)

        textWrap = QWidget()
        textWrap.setLayout(textLay)
        textWrap.setMinimumWidth(140)

        self.brightValue = BodyLabel("80%")
        self.brightValue.setMinimumWidth(44)
        self.brightValue.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.slider = Slider(Qt.Orientation.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.setValue(80)
        self.slider.setFixedWidth(280)

        self.slider.valueChanged.connect(self._on_change_br_preview_handle)
        self.slider.sliderReleased.connect(self._on_change_br_commit_handle)

        lay.addWidget(icon, 0, Qt.AlignmentFlag.AlignVCenter)
        lay.addWidget(textWrap, 0, Qt.AlignmentFlag.AlignVCenter)
        lay.addStretch(1)
        lay.addWidget(self.slider, 0, Qt.AlignmentFlag.AlignVCenter)
        lay.addWidget(self.brightValue, 0, Qt.AlignmentFlag.AlignVCenter)

        return card

    ## 右 预设颜色卡 
    def _build_right_preset_color(self) -> HeaderCardWidget:
        card = HeaderCardWidget("主题色", self)

        # 标题不加粗
        f = card.headerLabel.font()
        f.setWeight(QFont.Normal)
        card.headerLabel.setFont(f)

        # 左侧图标
        icon = IconWidget(FluentIcon.PALETTE, card)
        icon.setFixedSize(16, 16)
        card.headerLayout.insertWidget(0, icon)
        card.headerLayout.setSpacing(8)

        wrap = QWidget()
        v = QVBoxLayout(wrap)
        v.setContentsMargins(0, 0, 0, 0)
        v.setSpacing(10)

        gridWrap = QWidget()
        grid = QGridLayout(gridWrap)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setHorizontalSpacing(10)
        grid.setVerticalSpacing(10)

        self._preset_colors = [
            "#FFB900", "#FF8C00", "#F7630C", "#CA5010", "#DA3B01", "#EF6950", "#D13438", "#FF4343", "#E74856",
            "#E81123", "#EA005E", "#C30052", "#E3008C", "#BF0077", "#C239B3", "#9A0089", "#0078D4", "#0063B1",
            "#8E8CD8", "#6B69D6", "#8764B8", "#744DA9", "#B146C2", "#881798", "#00B7C3", "#038387", "#00B294",
            "#018574", "#00CC6A", "#10893E", "#7A7574", "#5D5A58", "#68768A", "#515C6B", "#567C73", "#486860",
            "#498205", "#107C10", "#767676", "#4C4A48", "#69797E", "#4A5459", "#647C64"
        ]

        self._preset_tiles = []
        cols = 9

        for i, hex_color in enumerate(self._preset_colors):
            r, c = divmod(i, cols)

            tile = PresetColorTile(hex_color, 44, gridWrap)
            tile.clicked.connect(self._preset_color_btn_click_handle)

            self._preset_tiles.append(tile)
            grid.addWidget(tile, r, c)

        v.addWidget(gridWrap)
        card.viewLayout.addWidget(wrap)

        return card
