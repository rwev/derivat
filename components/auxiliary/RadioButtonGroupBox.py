import PyQt4.QtCore as Qt
import PyQt4.QtGui as QtGui

import Globals as GLOBALS

class RadioButtonGroupBox(QtGui.QWidget):
    changedSignal = Qt.pyqtSignal(object)
    def __init__(self, group_name = None, display_only = False, parent = None):
        QtGui.QWidget.__init__(self, parent)
        main_layout = QtGui.QVBoxLayout()
        self.setLayout(main_layout)
        group_box = QtGui.QGroupBox(group_name)
        self.content_layout = QtGui.QHBoxLayout()
        group_box.setLayout(self.content_layout)
        self.button_group = QtGui.QButtonGroup()
        self.button_group.buttonClicked.connect(self.emitChangedSignal)
        main_layout.addWidget(group_box)
        self.options = ()

    def addOptions(self, radio_button_options_tuple):
        self.options = radio_button_options_tuple
        option_id = 0
        for radio_button_option in radio_button_options_tuple:

            radio_button = QtGui.QRadioButton(radio_button_option)

            self.button_group.addButton(radio_button)
            self.button_group.setId(radio_button, option_id)
            option_id += 1

            self.content_layout.addWidget(radio_button)

    def loadSelectedOption(self, setting_serialization_path):
        temp = GLOBALS.settings
        for attr in setting_serialization_path.split('.'):
            temp = temp[attr]
        self.setCheckedOption(temp)

    def setCheckedOption(self, option):
        self.clearSelection()
        id_to_check = self.options.index(option)
        if id_to_check >= 0:
            button_to_check = self.button_group.button(id_to_check)
            button_to_check.setChecked(True)        
        return

    def emitChangedSignal(self):
        value = self.getValueIfDefined()
        if value:
            self.changedSignal.emit(value)
            Qt.QCoreApplication.processEvents()

    def getValueIfDefined(self):
        checked_id = self.button_group.checkedId()
        if checked_id >= 0:
            return self.options[checked_id]
        return False


    def clearSelection(self):
        checked_id = self.button_group.checkedId()
        if checked_id >= 0:
            
            self.button_group.setExclusive(False)

            checked_button = self.button_group.checkedButton()
            checked_button.setChecked(False)

            self.button_group.setExclusive(True)

