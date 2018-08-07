import PyQt4.QtCore as Qt
import PyQt4.QtGui as QtGui

class PushButtonGroupBox(QtGui.QWidget):
    changedSignal = Qt.pyqtSignal(object)
    def __init__(self, row_dimension, column_dimension, group_name = None, display_only = False, parent = None):
        QtGui.QWidget.__init__(self, parent)
        
        self.row_dimension = row_dimension
        self.column_dimension = column_dimension
        self.row_index_to_add = 0
        self.column_index_to_add = 0
        
        main_layout = QtGui.QVBoxLayout()
        self.setLayout(main_layout)
        group_box = QtGui.QGroupBox(group_name)
        self.content_layout = QtGui.QGridLayout()

        group_box.setLayout(self.content_layout)
        self.button_group = QtGui.QButtonGroup()
        self.button_group.buttonClicked.connect(self.emitChangedSignal)
        main_layout.addWidget(group_box)
        self.actions = ()

    def addActions(self, push_button_actions_tuple):
        self.actions = push_button_actions_tuple
        action_id = 0
        for push_button_action in push_button_actions_tuple:
            push_button = QtGui.QPushButton(push_button_action)

            self.button_group.addButton(push_button)
            self.button_group.setId(push_button, action_id)

            action_id += 1

            self.content_layout.addWidget(push_button, self.row_index_to_add, self.column_index_to_add )
            self.getNextPositionToAdd()

    def getNextPositionToAdd(self):
        if self.column_index_to_add >= self.column_dimension - 1:
            self.column_index_to_add = 0
            self.row_index_to_add += 1
        else:
            self.column_index_to_add += 1
        return self.row_index_to_add, self.column_index_to_add

    def emitChangedSignal(self):
        value = self.getValueIfDefined()
        if value:
            self.changedSignal.emit(value)
            Qt.QCoreApplication.processEvents()

    def getValueIfDefined(self):
        checked_id = self.button_group.checkedId()
        if checked_id >= 0:
            return self.actions[checked_id]
        return False
