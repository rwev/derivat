
import PyQt4.QtCore as Qt
import yaml

from ..libs import MBD
from ..libs.Constants import derivat_constants as CONSTANTS

class SaveYAMLThread(Qt.QThread):
    resultsSignal = Qt.pyqtSignal(object)
    def __init__(self, parent = None):
        Qt.QThread.__init__(self, parent)
    def run(self, settingsMBD): 
        settings_dict = MBD.convertMBDtoDict()
        print(settings_dict)
        with open(CONSTANTS.backend.serialization.settings_path, 'w+') as stream:
            yaml.dump(settings_dict, stream)
        self.resultsSignal.emit()

class LoadYAMLThread(Qt.QThread):
    resultsSignal = Qt.pyqtSignal(object)
    def __init__(self, parent = None):
        Qt.QThread.__init__(self, parent)
    def run(self): 
        with open(CONSTANTS.backend.serialization.settings_path, 'r') as stream:
            settings_dict = yaml.load(stream)
        print(settings_dict)
        settingsMBD = MDB.convertDictToMBD(settings_dict)
        self.resultsSignal.emit(settingsMBD)
