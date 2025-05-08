from env import VERSION_PROGRAM

from core import config
from core.database.Models import Local
from core.fixture import get_fixture_yield, is_online

from gui.views.components.TestPanel import TestPanel
from gui.views.components.ConfigPanel import ConfigPanel
from gui.views.components.NavComponent import NavComponent

from udpsocket import UDPSignals

from PyQt5.QtWidgets import (
    QMainWindow, 
    QVBoxLayout, 
    QWidget, 
    QLabel, 
    QHBoxLayout, 
    QTableWidget, 
    QTableWidgetItem,
    QHeaderView, 
    QAbstractItemView, 
    QBoxLayout,
    QStackedWidget
)

class MainWindow(QMainWindow):
    '''
    #   Class: MainWindow
    #   Desc: Main fixture panel to show fixture tests table, fixture yield and fixture online status.
    '''
    
    panel_layouts = {
        "TestPanel": TestPanel,
        "ConfigPanel": ConfigPanel
    }
    
    def __init__(self, signals: UDPSignals):
        '''
        #   Function: __init__
        #   Desc: Main window constructor.
        #   Arguments:
        #       signals      | type:UDPSignals | Siganals & Events to comunicate the Panel and UDP Server
        '''
        
        super().__init__()
        self.signals = signals

        # ~ Define panel style        
        self.setWindowTitle(f"JPanel - ICT v{VERSION_PROGRAM}")
        self.setFixedSize(1000, 600)
        self.setup_main_panel()
        
        # ~ Generate new layout to add containers
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 5, 10, 5)
        layout.addWidget(NavComponent(self.change_panel))
        
        # ~ Update an show panel
        # self.change_panel("TestPanel")
        layout.addWidget(self.main_panel)
        
        # ~ Add main layout to main container.
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # ~ Add update function to update signal to executes it when will be activated.
        self.signals.update_ui.connect(self.update_main_panel)
        
    def setup_main_panel(self):
        self.main_panel = QWidget()
        self.panels = QStackedWidget()

        layout = QVBoxLayout(self.main_panel)
        layout.setContentsMargins(0, 0, 0, 0)

        test_panel = TestPanel()
        config_panel = ConfigPanel()

        self.panel_layouts['TestPanel'] = test_panel
        self.panel_layouts['ConfigPanel'] = config_panel

        self.panels.addWidget(test_panel)
        self.panels.addWidget(config_panel)
        layout.addWidget(self.panels)
    
    def update_main_panel(self):
        self.panel_layouts['TestPanel'].update_ui()
        # self.panel_layouts['ConfigPanel'].update_ui()
    
    def change_panel(self, panel_index: int):
        self.panels.setCurrentIndex(panel_index)
        if panel_index == 0:
            self.panel_layouts['TestPanel'].update_ui()
    
    def closeEvent(self, event):
        self.signals.stop_server.set()
        event.accept()