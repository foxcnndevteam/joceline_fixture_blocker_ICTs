from gui.assets import get_asset

from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton

class Panel:
    TestPanelIndex = 0
    ConfigPanelIndex = 1

class NavComponent(QWidget):
    def __init__(self, change_panel, parent=None):
        super().__init__(parent)
        
        self.change_panel = change_panel
        
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet("""
            border-radius: 5px;
            background-color: #cccccc;
        """)
        # self.setFixedSize(QSize(50, 50))  # Para que se vea el fondo
        
        self.setup_component()

    def setup_component(self):
        nav_layout = QHBoxLayout()
        nav_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        nav_layout.setContentsMargins(5, 5, 5, 5)
        
        home_button = QPushButton()
        home_button.setIcon(QIcon(get_asset("icons/home_icon.png")))
        home_button.setIconSize(QSize(35, 35))
        home_button.setCursor(Qt.CursorShape.PointingHandCursor)
        home_button.setStyleSheet("""
            QPushButton {
                border: none;
                padding: 5px;
            }
            
            QPushButton:hover {
                background-color: #dfdfdf;
            }
        """)
        home_button.clicked.connect(self.change_panel_to_home)

        config_button = QPushButton()
        config_button.setIcon(QIcon(get_asset("icons/config_icon.png")))
        config_button.setIconSize(QSize(35, 35))
        config_button.setCursor(Qt.CursorShape.PointingHandCursor)
        config_button.setStyleSheet("""
            QPushButton {
                border: none;
                padding: 5px;
            }
            
            QPushButton:hover {
                background-color: #dfdfdf;
            }
        """)
        config_button.clicked.connect(self.change_panel_to_config)

        nav_layout.addWidget(home_button)
        nav_layout.addWidget(config_button)
        self.setLayout(nav_layout)
        
    def change_panel_to_config(self):
        self.change_panel(Panel.ConfigPanelIndex)
        
    def change_panel_to_home(self):
        self.change_panel(Panel.TestPanelIndex)