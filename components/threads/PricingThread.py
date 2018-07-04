
import PyQt4.QtCore as Qt
from ..libs import BAW

ROUNDDIG = 5

class PricingThread(Qt.QThread):
    resultsSignal = Qt.pyqtSignal(object)
    def __init__(self, parent = None):
        Qt.QThread.__init__(self, parent)
    def run(self, inputs, dimensions): 
        self.resultsSignal.emit(getattr(self, self.calc_function_name)(self.field))

        