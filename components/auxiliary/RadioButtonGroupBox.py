import PyQt4.QtCore as Qt
import PyQt4.QtGui as QtGui

from ..libs import PyQtShared as PYQT_SHARED

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
        main_layout.addWidget(group_box)

    def addOptions(self, radio_button_options_tuple):
        for radio_button_option in radio_button_options_tuple:
            radio_button = QtGui.QRadioButton(radio_button_option)
            self.button_group.addButton(radio_button)
            self.content_layout.addWidget(radio_button)
