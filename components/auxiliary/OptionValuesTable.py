
import PyQt4.QtCore as Qt
import PyQt4.QtGui as QtGui

class OptionValuesTable(QtGui.QTableWidget):
    def __init__(self, parent = None):
        QtGui.QTableWidget.__init__(self, parent)

    def updateStrikeColumns(self, strike_list):
        self.strike_list = strike_list
        self.setColumnCount(len(strike_list))
        self.setHorizontalHeaderLabels([str(l) for l in strike_list])
        
    def updateExpirationRows(self, expiration_list):
        self.expiration_list = expiration_list
        self.setRowCount(len(expiration_list))
        self.setVerticalHeaderLabels([str(l) for l in expiration_list])

    def updateValue(self, (strike, expiration, price)):
        column_index = self.strike_list.index(strike)
        row_index = self.expiration_list.index(expiration)
        self.setItem(row_index, column_index, QtGui.QTableWidgetItem(str(price)))




