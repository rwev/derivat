
import PyQt4.QtCore as Qt
import PyQt4.QtGui as QtGui

class CustomLineEdit(QtGui.QLineEdit):
    changedSignal = Qt.pyqtSignal(object)
    def __init__(self, default_text, parent = None):
        QtGui.QWidget.__init__(self, parent)

class AutoUpperLineEdit(CustomLineEdit):
    def __init__(self, default_text):
        super(AutoUpperLineEdit, self).__init__(default_text)
    def link(self):
        self.line_edit.textChanged.connect(self.capitalize)
    def capitalize(self):
        self.line_edit.setText(str(self.line_edit.text()).upper())
        self.changedSignal.emit(self.text())
        Qt.QCoreApplication.processEvents()
    def text(self):
        return self.line_edit.text()
        
class AutoNumeralLineEdit(CustomLineEdit):
    def __init__(self, default_text = ''):
        super(AutoNumeralLineEdit, self).__init__(default_text)
    def link(self):
        self.line_edit.textChanged.connect(self.checkNumeral)
    def checkNumeral(self):
        self.line_edit.setText(filter( lambda x: x in '0123456789.+-', str(self.line_edit.text()) ))
        self.changedSignal.emit(self.value())
        Qt.QCoreApplication.processEvents()
    def value(self):
        return float(self.line_edit.text())
        
class ListNumeralsLineEdit(CustomLineEdit):
    def __init__(self, default_text = None):
        super(ListNumeralsLineEdit, self).__init__(default_text)
    def link(self):
        self.line_edit.textChanged.connect(self.checkNumericList)
    def checkNumericList(self):
        text = filter(lambda x: x in '0123456789.,', str(self.line_edit.text()))
        self.line_edit.setText(', '.join(text.split(',')))
        self.changedSignal.emit(self.value())
        Qt.QCoreApplication.processEvents()
    def value(self):
        ret = []
        for num in filter(lambda x: x in '0123456789.,', str(self.line_edit.text())).split(','):
            ret.append(num)
        return num

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