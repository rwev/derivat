
import PyQt4.QtCore as Qt
import PyQt4.QtGui as QtGui

class NumericLineEdit(QtGui.QLineEdit):
    changedSignal = Qt.pyqtSignal(object)
    def __init__(self, default_text, parent = None):
        QtGui.QWidget.__init__(self, parent)
    def emitValue(self):
        value = self.getValueIfDefined()
        self.changedSignal.emit(value)

class AutoDoubleLineEdit(NumericLineEdit):
    def __init__(self, default_text = ''):
        super(AutoDoubleLineEdit, self).__init__(default_text)
        self.setValidator(QtGui.QDoubleValidator())
        self.link()
    def link(self):
        self.textChanged.connect(self.emitValue)
    def getValueIfDefined(self):
        value = self.text()
        try:
            return float(value)
        except ValueError:
            return False

class AutoIntegerLineEdit(NumericLineEdit):
    def __init__(self, default_text = ''):
        super(AutoIntegerLineEdit, self).__init__(default_text)
        self.setValidator(QtGui.QIntValidator())
        self.link()
    def link(self):
        self.textChanged.connect(self.emitValue)
    def getValueIfDefined(self):
        value = self.text()
        try:
            return int(value)
        except ValueError:
            return False
