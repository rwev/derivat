
import PyQt4.QtCore as Qt
import PyQt4.QtGui as QtGui

class CustomComboBox(QtGui.QComboBox):
    changedSignal = Qt.pyqtSignal(object)
    def __init__(self, default_choices, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.choices = default_choices
        self.addItems(default_choices)
        self.currentIndexChanged.connect(self.emit)
    def emit(self, index):
        self.changedSignal.emit(self.choices[index])
    def getValueIfDefined(self):
        index = self.currentIndex()
        if index > 0:
            return self.choices[index]