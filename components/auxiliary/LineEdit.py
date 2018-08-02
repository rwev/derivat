
import PyQt4.QtCore as Qt
import PyQt4.QtGui as QtGui

class CustomLineEdit(QtGui.QLineEdit):
    changedSignal = Qt.pyqtSignal(object)
    def __init__(self, default_text, parent = None):
        QtGui.QWidget.__init__(self, parent)
    def emitValueIfDefined(self):
        value = self.getValueIfDefined()
        if value:
            self.changedSignal.emit(value)
            Qt.QCoreApplication.processEvents()

class AutoDoubleLineEdit(CustomLineEdit):
    def __init__(self, default_text = ''):
        super(AutoDoubleLineEdit, self).__init__(default_text)
        self.setValidator(QtGui.QDoubleValidator())
        self.link()
    def link(self):
        self.textChanged.connect(self.emitValueIfDefined)
    def getValueIfDefined(self):
        value = self.text()
        if value:
            return float(value)
        return False

class AutoIntegerLineEdit(CustomLineEdit):
    def __init__(self, default_text = ''):
        super(AutoIntegerLineEdit, self).__init__(default_text)
        self.setValidator(QtGui.QIntValidator())
        self.link()
    def link(self):
        self.textChanged.connect(self.emitValueIfDefined)
    def getValueIfDefined(self):
        value = self.text()
        if value:
            return int(value)
        return False
