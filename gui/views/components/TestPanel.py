from typing import Literal
import json
from core import config
from core.database.Models import Local
from core.fixture import get_fixture_yield, get_fixture_state
from core.config import get_fixture_id
from gui.assets import get_asset
from gui.views.dialogs.LogViewWindow import LogDialog
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QLabel, QHBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView

errors: dict[str, str]

def load_errors_names():
    global errors
    errors_names_dir = get_asset("data/errors.json")
    with open(errors_names_dir) as fie:
        errors = json.load(fie)

def get_error_name(error_code: int) -> str:
    global errors
    error_name = errors.get(str(error_code))
    if error_name == None:
        return 'undocumented'
    return error_name


class TestPanel(QWidget):

    status_style = '''
        font-size: 40px; 
        font-weight: bold;
    '''

    __logs_files: dict[str, str] = {}

    def __show_log(self, item):
        fila = item.row()
        columna = item.column()
        if columna != 1 or fila < 1:
            return
        log_file = self.__logs_files.get(fila)
        if log_file != None:
            dialog_log = LogDialog(log_name=log_file)
            dialog_log.exec_()
    
    def __get_text_color(self, fixture_state: Literal['Blocked', 'Offline', 'Online']) -> Literal['green', 'gray', 'green']:
        color = 'green'

        if fixture_state == 'Offline':
            color = 'gray'

        if fixture_state == 'Blocked':
            color = 'red'

        return color

    def __init__(self, parent=None):
        super().__init__(parent)
        load_errors_names()
        # ~ Executes functions to setup widgets
        self.setup_header_container()
        self.setup_tests_table()
        self.update_tests_table()
        
        layout = QVBoxLayout(self)
        
        layout.addWidget(self.header_container)
        layout.addWidget(self.table_container)
        layout.setContentsMargins(0, 0, 0, 0)
                
    def setup_header_container(self):
        '''
        #   Function: setup_header_container
        #   Desc: Setup the header container wich contains Yield and Fixture status.
        '''
        self.header_container = QWidget()
        self.header_container.setObjectName("HeaderContainer")
        self.header_container.setStyleSheet("""
            #HeaderContainer {
                background-color: #dfdfdf;
                border-radius: 5px;
            }
        """)
        
        header_layout = QHBoxLayout(self.header_container)
        
        # ~ Yield widgets ------------------------------------------------------------
        self.yield_label = QLabel('Yield:')
        self.yield_label.setStyleSheet("font-size: 30px;")
        
        self.yield_percent = QLabel(f'{int(get_fixture_yield())}%')
        self.yield_percent.setStyleSheet("font-size: 40px; font-weight: bold;")
        
        # ~ Status widgets -----------------------------------------------------------
        self.status_label = QLabel('Status:')
        self.status_label.setStyleSheet("font-size: 30px;")
        
        fixture_state = get_fixture_state(False)

        self.status_value = QLabel(
            fixture_state
        )
        self.status_value.setStyleSheet(f'''
            {self.status_style}
            color: {
                self.__get_text_color(fixture_state)
            };
        ''')
        
        self.header_container.setLayout(header_layout)
        
        # ~ Add widgets to layout
        header_layout.addWidget(self.yield_label)
        header_layout.addWidget(self.yield_percent)
        header_layout.addWidget(self.status_label)
        header_layout.addWidget(self.status_value)
        
    def setup_tests_table(self):
        '''
        #   Function: setup_tests_table
        #   Desc: Setup the table to show the latest N tests.
        '''
        self.table_container = QTableWidget()

        self.table_container.setRowCount(config.gey_yield_calc_qty() + 1)
        self.table_container.setColumnCount(8)
        
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
        
        self.table_container.itemClicked.connect(self.__show_log)

    def update_tests_table(self):
        '''
        #   Function: update_tests_table
        #   Desc: Updates table values with the latests N tests.
        '''
        # ~ First define table columns
        self.table_container.setItem(0, 0, QTableWidgetItem("Id"))
        self.table_container.setItem(0, 1, QTableWidgetItem("Serial"))
        self.table_container.setItem(0, 2, QTableWidgetItem("Result"))
        self.table_container.setItem(0, 3, QTableWidgetItem("Mode"))
        self.table_container.setItem(0, 4, QTableWidgetItem("Fail status"))
        self.table_container.setItem(0, 5, QTableWidgetItem("Fail name"))
        self.table_container.setItem(0, 6, QTableWidgetItem("Board failed"))
        self.table_container.setItem(0, 7, QTableWidgetItem("Date"))

        tests = self.get_last_tests()

        self.__logs_files = {}

        # ~ If someone test add rows
        if tests:
            for i in range(1, ( len(list(tests)) + 1 )):
                self.table_container.setItem(i, 0, QTableWidgetItem(f'{tests[i - 1].id}'))
                self.table_container.setItem(i, 1, QTableWidgetItem(f'{tests[i - 1].serial}'))
                self.table_container.setItem(i, 2, QTableWidgetItem(f'{tests[i - 1].result}'))
                self.table_container.setItem(i, 3, QTableWidgetItem(f'{tests[i - 1].mode}'))
                self.table_container.setItem(i, 4, QTableWidgetItem(f'{tests[i - 1].fail_status}'))
                self.table_container.setItem(i, 5, QTableWidgetItem(f'{get_error_name(tests[i - 1].fail_status)}'))
                self.table_container.setItem(i, 6, QTableWidgetItem(f'{tests[i - 1].board_failed}'))
                self.table_container.setItem(i, 7, QTableWidgetItem(f'{tests[i - 1].date}'))

                if tests[i - 1].result == 'FAIL':
                    # date format
                    formated_date = tests[i - 1].date.strftime('%Y-%m-%dT%H-%M-%S') 
                    # end date format
                    self.__logs_files[i] = f'LOG_REPORT_{formated_date}-{tests[i - 1].serial}-{tests[i - 1].result}-{get_fixture_id()}_B{tests[i - 1].board_failed}.txt'

    def get_last_tests(self):
        '''
        #   Function: get_last_tests
        #   Desc: Get the latest N tests in the database.
        '''
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

    def update_ui(self):
        '''
        #   Function: update_ui
        #   Desc: Executes update function and update labels values.
        '''
        self.yield_percent.setText(f'{int(get_fixture_yield())}%')

        fixture_state = get_fixture_state(False)

        self.status_value.setText(
            fixture_state
        )
        self.status_value.setStyleSheet(f'''
            {self.status_style}
            color: {
                self.__get_text_color(fixture_state)
            };
        ''')
        
        self.update_tests_table()