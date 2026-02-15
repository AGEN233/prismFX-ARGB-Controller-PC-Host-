from PySide6.QtCore import Qt
from PySide6.QtGui import QGuiApplication
from qfluentwidgets import (
    FluentWindow,
    FluentIcon,
    NavigationItemPosition,
    PushButton,
    BodyLabel,
)

from ui.pages.home import HomePage
from ui.pages.static import StaticPage
from ui.pages.dynamic import DynamicPage
from ui.pages.gif import GifPage
from ui.pages.connect import ConnectPage
from ui.pages.device import DevicePage
from ui.pages.setting import SettingPage
from qfluentwidgets import MSFluentWindow

class MainWindow(MSFluentWindow):
    def __init__(self):
        super().__init__()
        self.pageHome = HomePage()
        self.pageStatic = StaticPage()
        self.pageDynamic = DynamicPage()
        self.pageGif = GifPage()
        self.pageConnect = ConnectPage()
        self.pageDevice = DevicePage()
        self.pageSetting = SettingPage()
        self.initWindow()
        self.initNavigation()

    
    def initWindow(self): 
        self.setWindowTitle("PrismFX ARGB Connter")
        self.resize(1120, 780)

        screen = QGuiApplication.primaryScreen()
        geometry = screen.availableGeometry()
        width = geometry.width()
        height = geometry.height()
        self.move(((width //2) - (self.width()//2)), ((height//2) - (self.height()//2)))
        

    def initNavigation(self):

        self.addSubInterface(self.pageHome, FluentIcon.HOME, "主页", FluentIcon.HOME_FILL)
        self.addSubInterface(self.pageStatic, FluentIcon.PALETTE, "静态")
        self.addSubInterface(self.pageDynamic, FluentIcon.MOVIE, "动态")
        self.addSubInterface(self.pageGif, FluentIcon.PHOTO, "GIF")
        self.addSubInterface(self.pageDevice, FluentIcon.DEVELOPER_TOOLS, "设备")

        self.addSubInterface(self.pageConnect, FluentIcon.BLUETOOTH, "连接", None, NavigationItemPosition.BOTTOM)
        self.addSubInterface(self.pageSetting, FluentIcon.SETTING, "设置", None, NavigationItemPosition.BOTTOM)
        

        self.stackedWidget.setCurrentWidget(self.pageHome)

