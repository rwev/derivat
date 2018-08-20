
import PyQt4.QtCore as Qt
import PyQt4.QtGui as QtGui

from ..libs.Constants import constants as CONSTANTS

class OptionValuesTable(QtGui.QTableWidget):
    def __init__(self, parent = None):
        QtGui.QTableWidget.__init__(self, parent)

        self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.setFocusPolicy(Qt.Qt.NoFocus)
        self.setSelectionMode(QtGui.QAbstractItemView.NoSelection)

        font = QtGui.QFont()
        font.setPointSize(CONSTANTS.window.table.content.font.size)
        self.setFont(font)

    def _getFormattedContentCell(self, value):
        value_str = str(value)[:CONSTANTS.window.table.content.characters]
        cell = QtGui.QTableWidgetItem(value_str)
        cell.setTextAlignment(Qt.Qt.AlignCenter)
        return cell

    def setStrikeColumns(self, strike_list):
        self.setColumnCount(len(strike_list))
        self.setHorizontalHeaderLabels([str(l) for l in strike_list])

    def clearStrikeColumns(self):
        self.setColumnCount(0)
        self.setHorizontalHeaderLabels([])
        
    def setExpirationRows(self, expiration_list):
        self.setRowCount(len(expiration_list))
        self.setVerticalHeaderLabels([str(l) for l in expiration_list])

    def clearExpirationRows(self):
        self.setRowCount(0)
        self.setVerticalHeaderLabels([])

    def updateValue(self, (strike_index, expiration_index, value)):
        column_index = strike_index
        row_index = expiration_index
        cell = self._getFormattedContentCell(value)
        self.setItem(row_index, column_index, cell)



