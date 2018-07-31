
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

class AutoUpperLineEdit(CustomLineEdit):
    def __init__(self, default_text):
        super(AutoUpperLineEdit, self).__init__(default_text)
        self.link()
    def link(self):
        self.textChanged.connect(self.capitalize)
    def capitalize(self):
        self.setText(str(self.text()).upper())
        self.emitValueIfDefined()
    def getValueIfDefined(self):
        value = self.text()
        if value:
            return str(self.text())
        return False
        
class AutoNumeralLineEdit(CustomLineEdit):
    def __init__(self, default_text = ''):
        super(AutoNumeralLineEdit, self).__init__(default_text)
        self.link()
    def link(self):
        self.textChanged.connect(self.checkNumeral)
    def checkNumeral(self):
        self.setText(filter( lambda x: x in '0123456789.+-', str(self.text())))
        self.emitValueIfDefined()
    def getValueIfDefined(self):
        value = self.text()
        if value:
            return float(value)
        return False
        
# TODO: refactor FilePathLineEdit        
class FilePathLineEdit(QtGui.QLineEdit):
    def __init__(self, default_path = None, parent=None):
        super(FilePathLineEdit, self).__init__()
        self.button = QtGui.QToolButton()
        self.button.setIcon(QtGui.QIcon('folder_icon.ico'))
        self.button.setStyleSheet("background: transparent; border: none;")
        self.button.setFixedSize(20, 20)
        self.button.clicked.connect(self.selectFolder)
        
        layout = QtGui.QHBoxLayout()
        layout.setAlignment(Qt.Qt.AlignRight)
        layout.addWidget(self.button)
        layout.setSpacing(0)
        layout.setContentsMargins(0,0,0,0)
        self.setLayout(layout)
        Qt.QCoreApplication.processEvents()
        
    def selectFolder(self):
        filepath = str(QtGui.QFileDialog.getOpenFileName())
        if filepath:
            self.setText(filepath)