from core import config
from core.database.Models import Local
from core.fixture import get_fixture_yield, is_online

from udpsocket import UDPSignals

from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel, QHBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView

'''
#   Class: MainWindow
#   Desc: Main fixture panel to show fixture tests table, fixture yield and fixture online status.
'''
class MainWindow(QMainWindow):
    status_style = '''
        font-size: 40px; 
        font-weight: bold;
    '''
    
    '''
    #   Function: __init__
    #   Desc: Main window constructor.
    #   Arguments:
    #       signals      | type:UDPSignals | Siganals & Events to comunicate the Panel and UDP Server
    '''
    def __init__(self, signals: UDPSignals):
        super().__init__()
        self.signals = signals

        # ~ Define panel style        
        self.setWindowTitle("JPanel - ICT")
        self.setFixedSize(900, 500)
        
        # ~ Executes functions to setup widgets
        self.setup_header_container()
        self.setup_tests_table()
        self.update_tests_table()
        
        # ~ Generate new layout to add containers
        layout = QVBoxLayout()
        layout.addWidget(self.header_container)
        layout.addWidget(self.table_container)

        # ~ Add main layout to main container.
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # ~ Add update function to update signal to executes it when will be activated.
        self.signals.update_ui.connect(self.update_ui)
    
    
    '''
    #   Function: setup_header_container
    #   Desc: Setup the header container wich contains Yield and Fixture status.
    '''
    def setup_header_container(self):
        self.header_container = QWidget()
        header_layout = QHBoxLayout(self.header_container)
        
        # ~ Yield widgets ------------------------------------------------------------
        self.yield_label = QLabel('Yield:')
        self.yield_label.setStyleSheet("font-size: 30px;")
        
        self.yield_percent = QLabel(f'{int(get_fixture_yield())}%')
        self.yield_percent.setStyleSheet("font-size: 40px; font-weight: bold;")
        
        # ~ Status widgets -----------------------------------------------------------
        self.status_label = QLabel('Status:')
        self.status_label.setStyleSheet("font-size: 30px;")
        
        self.status_value = QLabel(
            f'Online' if is_online(get_status_from_db=True) else 'Offline'
        )
        self.status_value.setStyleSheet(f'''
            {self.status_style}
            color: {
                'green' if is_online(get_status_from_db=True) else 'gray'
            };
        ''')
        
        # ~ Add widgets to layout
        header_layout.addWidget(self.yield_label)
        header_layout.addWidget(self.yield_percent)
        header_layout.addWidget(self.status_label)
        header_layout.addWidget(self.status_value)
    
    
    '''
    #   Function: setup_tests_table
    #   Desc: Setup the table to show the latest N tests.
    '''
    def setup_tests_table(self):
        self.table_container = QTableWidget()
        
        self.table_container.setRowCount(config.gey_yield_calc_qty() + 1)
        self.table_container.setColumnCount(7)
        
        self.table_container.horizontalHeader().setStretchLastSection(True) 
        self.table_container.horizontalHeader().setSectionResizeMode( 
            QHeaderView.ResizeToContents
        )
        self.table_container.setStyleSheet("""
            QTableWidget::item {
                padding: 20px;           /* Espaciado interno */
                text-align: center;     /* Centrar el contenido */
            }
        """)
        
        self.table_container.setEditTriggers(QAbstractItemView.NoEditTriggers)


    '''
    #   Function: update_tests_table
    #   Desc: Updates table values with the latests N tests.
    '''
    def update_tests_table(self):
        # ~ First define table columns
        self.table_container.setItem(0, 0, QTableWidgetItem("Id"))
        self.table_container.setItem(0, 1, QTableWidgetItem("Serial"))
        self.table_container.setItem(0, 2, QTableWidgetItem("Result"))
        self.table_container.setItem(0, 3, QTableWidgetItem("Mode"))
        self.table_container.setItem(0, 4, QTableWidgetItem("Fail status"))
        self.table_container.setItem(0, 5, QTableWidgetItem("Board failed"))
        self.table_container.setItem(0, 6, QTableWidgetItem("Date"))

        tests = self.get_last_tests()

        # ~ If someone test add rows
        if tests:
            for i in range(1, ( len(list(tests)) + 1 )):
                self.table_container.setItem(i, 0, QTableWidgetItem(f'{tests[i - 1].id}'))
                self.table_container.setItem(i, 1, QTableWidgetItem(f'{tests[i - 1].serial}'))
                self.table_container.setItem(i, 2, QTableWidgetItem(f'{tests[i - 1].result}'))
                self.table_container.setItem(i, 3, QTableWidgetItem(f'{tests[i - 1].mode}'))
                self.table_container.setItem(i, 4, QTableWidgetItem(f'{tests[i - 1].fail_status}'))
                self.table_container.setItem(i, 5, QTableWidgetItem(f'{tests[i - 1].board_failed}'))
                self.table_container.setItem(i, 6, QTableWidgetItem(f'{tests[i - 1].date}'))


    '''
    #   Function: get_last_tests
    #   Desc: Get the latest N tests in the database.
    '''
    def get_last_tests(self):
        tests = Local.Test().select(
            Local.Test.id,
            Local.Test.serial,
            Local.Test.result,
            Local.Test.fail_status,
            Local.Test.board_failed,
            Local.Test.date,
            Local.Test.mode
        ).limit(config.gey_yield_calc_qty()).order_by(
            Local.Test.date.desc()
        )
        
        return tests


    '''
    #   Function: update_ui
    #   Desc: Executes update function and update labels values.
    '''
    def update_ui(self):
        self.yield_percent.setText(f'{int(get_fixture_yield())}%')
        
        
        print(f'Online' if is_online(get_status_from_db=True) else 'Offline')
        self.status_value.setText(
            f'Online' if is_online(get_status_from_db=True) else 'Offline'
        )
        self.status_value.setStyleSheet(f'''
            {self.status_style}
            color: {
                'green' if is_online(get_status_from_db=True) else 'gray'
            };
        ''')
        
        self.update_tests_table()


    '''
    #   Function: closeEvent
    #   Desc: Send signal to the UDPServer to stop it.
    '''
    def closeEvent(self, event):
        self.signals.stop_server.set()
        event.accept()