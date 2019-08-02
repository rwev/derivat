import PyQt4.QtCore as Qt
import PyQt4.QtGui as QtGui

from ..libs import VisualizationUtils as VIS_UTILS
from ..libs.Constants import constants as CONSTANTS


class OptionValuesTable(QtGui.QTableWidget):
    def __init__(self, parent=None):
        QtGui.QTableWidget.__init__(self, parent)

        self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.setFocusPolicy(Qt.Qt.NoFocus)
        self.setSelectionMode(QtGui.QAbstractItemView.NoSelection)

        self.verticalHeader().setDefaultSectionSize(
            CONSTANTS.window.table.content.cell.size
        )
        self.verticalHeader().setResizeMode(QtGui.QHeaderView.Fixed)

        self.horizontalHeader().setDefaultSectionSize(
            CONSTANTS.window.table.content.cell.size
        )
        self.horizontalHeader().setResizeMode(QtGui.QHeaderView.Fixed)

    def _getFormattedContentitem(self, value):
        value_str = str(value)[: CONSTANTS.window.table.content.characters]
        item = QtGui.QTableWidgetItem(value_str)
        item.setTextAlignment(Qt.Qt.AlignCenter)
        item.setTextColor(QtGui.QColor(*VIS_UTILS.gray))
        return item

    def setStrikeColumns(self, strike_list):
        self.setColumnCount(len(strike_list))
        self.setHorizontalHeaderLabels([str(l) for l in strike_list])
        self.clearContents()

    def clearStrikeColumns(self):
        self.setColumnCount(0)
        self.setHorizontalHeaderLabels([])
        self.clearContents()

    def setExpirationRows(self, expiration_list):
        self.setRowCount(len(expiration_list))
        self.setVerticalHeaderLabels([str(l) for l in expiration_list])
        self.clearContents()

    def clearExpirationRows(self):
        self.setRowCount(0)
        self.setVerticalHeaderLabels([])
        self.clearContents()

    def updateValue(self, (strike_index, expiration_index, value)):
        column_index = strike_index
        row_index = expiration_index
        item = self._getFormattedContentitem(value)
        self.setItem(row_index, column_index, item)

    def makeHeated(self, (min_value, max_value)):
        for row in range(self.rowCount()):
            for column in range(self.columnCount()):
                item = self.item(row, column)
                value = float(item.text())
                color = VIS_UTILS.colormap(
                    VIS_UTILS.mapValueToRange(min_value, max_value, 0, 1, value)
                )
                item.setTextColor(QtGui.QColor(*(255 * i for i in color)))
