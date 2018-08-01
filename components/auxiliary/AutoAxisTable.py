
import PyQt4.QtCore as Qt
import PyQt4.QtGui as QtGui

class AutoAxisTable(QtGui.QTableWidget):
    def __init__(self, parent = None):
        QtGui.QTableWidget.__init__(self, parent)
        
    def updateRowLabels(self, labels):
        self.setRowCount(len(labels))
        self.setVerticalHeaderLabels([str(l) for l in labels])

    def updateColumnLabels(self, labels):
        self.setColumnCount(len(labels))
        self.setHorizontalHeaderLabels([str(l) for l in labels])





