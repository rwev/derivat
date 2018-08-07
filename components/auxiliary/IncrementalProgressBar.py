
import PyQt4.QtCore as Qt
import PyQt4.QtGui as QtGui

class IncrementalProgressBar(QtGui.QProgressBar):
    def __init__(self, parent = None):
        QtGui.QProgressBar.__init__(self, parent)
        self.to_increment = 0

    def resetToIncrement(self):
        self.to_increment = 0

    def increment(self):
        self.to_increment += 1
        self.setValue(self.to_increment)

    def setMaximumIncrements(self, max_incs):
        self.setValue(0)
        self.setMinimum(0)
        self.setMaximum(max_incs)