from Manager.ConfigManager import ConfigManager
from BinaryMode import BinaryMode as BinaryMode
from ApiMode import ApiMode as ApiMode
from LogMode import LogMode as LogMode


modes = {
    0: LogMode,
    1: BinaryMode,
    2: ApiMode
}

class Switcher:

    def __init__(self):
        try:
            cm = ConfigManager()
            self.sfc_mode = modes[cm.getSFCMode()]
        except KeyError:
            print("El modo no se encuentra entre los modos conocidos")

    def uploadSFC(sefl):
        pass
