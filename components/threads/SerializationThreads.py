
import PyQt4.QtCore as Qt
import yaml

from ..libs import MBD
from ..libs.Constants import constants as CONSTANTS

from ..auxiliary import Globals as GLOBALS

class SaveYAMLThread(Qt.QThread):
    resultsSignal = Qt.pyqtSignal(object)
    def __init__(self, parent = None):
        Qt.QThread.__init__(self, parent)
    def run(self): 
        settings_dict = MBD.convertMBDtoDict(GLOBALS.settings)
        with open(CONSTANTS.backend.serialization.path.file, 'w+') as stream:
            yaml.dump(settings_dict, stream)
        self.resultsSignal.emit(GLOBALS.settings)

class LoadYAMLThread(Qt.QThread):
    resultsSignal = Qt.pyqtSignal(object)
    def __init__(self, parent = None):
        Qt.QThread.__init__(self, parent)
    def run(self): 
        with open(CONSTANTS.backend.serialization.path.file, 'r') as stream:
            settings_dict = yaml.load(stream)
        settingsMBD = MBD.convertDictToMBD(settings_dict)
        self.resultsSignal.emit(settingsMBD)
