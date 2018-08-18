
import PyQt4.QtCore as Qt
import PyQt4.QtGui as QtGui

from ..libs import PyQtShared as PYQT_SHARED

import Globals as GLOBALS

import LineEdit as LINE_EDIT

class NumericInputWidget(QtGui.QWidget):
    changedSignal = Qt.pyqtSignal(object)
    def __init__(self, group_name = None, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.param_name_to_editable_dict = {}
        
        self.main_layout = QtGui.QVBoxLayout()
        
        self.group_box = QtGui.QGroupBox(group_name)
        self.content_layout = QtGui.QFormLayout()
        self.group_box.setLayout(self.content_layout)

        self.main_layout.addWidget(self.group_box)
        self.setLayout(self.main_layout)

    def _getLabel(self, name, typ):
        label = QtGui.QLabel()
        label.setText(Qt.QString(name))
        return label

    def _getEditable(self, typ, default):
        if typ == int: 
            editable = LINE_EDIT.AutoIntegerLineEdit(default)
        elif typ == float:
            editable = LINE_EDIT.AutoDoubleLineEdit(default)
        editable.changedSignal.connect(self.emitChangedSignal)
        return editable

    def loadValues(self, param_name_serialization_path_tuples):
        for (name, path) in param_name_serialization_path_tuples:
            temp = GLOBALS.settings
            for attr in path.split('.'):
                temp = temp[attr]
            self.param_name_to_editable_dict[name].setText(str(temp))
        self.emitChangedSignal()

    def setValidity(self, is_valid):
        PYQT_SHARED.setGroupBoxValidity(self.group_box, is_valid)

    def emitChangedSignal(self):
        self.changedSignal.emit(self.getParametersNameValueDict())
        
    def displayParameters(self, param_name_type_default_tuples):
        self.param_name_to_editable_dict = {}
        for (name, typ, default) in param_name_type_default_tuples:
            label = self._getLabel(name, typ)
            editable = self._getEditable(typ, default)
            self.param_name_to_editable_dict[name] = editable
            self.content_layout.addRow(label, editable)

    def getParametersNameValueDict(self):
        param_name_value_dict = {}
        for name in self.param_name_to_editable_dict.keys():
            editable = self.param_name_to_editable_dict[name]
            value = editable.getValueIfDefined()
            param_name_value_dict[name] = value
        return param_name_value_dict

    def clearForm(self):
        for name in self.param_name_to_editable_dict.keys():
            editable = self.param_name_to_editable_dict[name]
            editable.clear()
        self.emitChangedSignal()



