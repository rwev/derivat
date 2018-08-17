import PyQt4.QtCore as Qt
import PyQt4.QtGui as QtGui

class PushButtonGroupBox(QtGui.QWidget):
    actionSignal = Qt.pyqtSignal(object)
    def __init__(self, row_dimension, column_dimension, group_name = None, display_only = False, parent = None):
        QtGui.QWidget.__init__(self, parent)
        
        self.row_dimension = row_dimension
        self.column_dimension = column_dimension
        self.row_index_to_add = 0
        self.column_index_to_add = 0
        
        self.main_layout = QtGui.QVBoxLayout()
        
        self.group_box = QtGui.QGroupBox(group_name)
        self.content_layout = QtGui.QGridLayout()
        self.group_box.setLayout(self.content_layout)

        self.main_layout.addWidget(self.group_box)
        self.setLayout(self.main_layout)

        self.button_group = QtGui.QButtonGroup()
        self.button_group.buttonClicked[int].connect(self.emitChangedSignal)

        self.actions = ()

    def _getNextPositionToAdd(self):
        if self.column_index_to_add >= self.column_dimension - 1:
            self.column_index_to_add = 0
            self.row_index_to_add += 1
        else:
            self.column_index_to_add += 1
        return self.row_index_to_add, self.column_index_to_add

    def addActions(self, push_button_actions_tuple):
        self.actions = push_button_actions_tuple
        action_id = 0
        for push_button_action in push_button_actions_tuple:

            push_button = QtGui.QPushButton(push_button_action)

            self.button_group.addButton(push_button)
            self.button_group.setId(push_button, action_id)

            action_id += 1

            self.content_layout.addWidget(push_button, self.row_index_to_add, self.column_index_to_add )
            self._getNextPositionToAdd()

    def setValidity(self, is_valid):
        PYQT_SHARED.setGroupBoxValidity(self.group_box, is_valid)

    def emitChangedSignal(self, index):
        value = self.getValueIfDefined(index)
        if value:
            self.actionSignal.emit(value)
            Qt.QCoreApplication.processEvents()

    def getValueIfDefined(self, index):
        if index >= 0:
            return self.actions[index]
        return False
