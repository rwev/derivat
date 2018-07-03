
import PyQt4.QtCore as Qt
import PyQt4.QtGui as QtGui

from ..lib import PyQtShared as PYQT_SHARED

import LineEdit as LINE_EDIT

class ParameterSelectionWidget(QtGui.QWidget):
    changedSignal = Qt.pyqtSignal(object)
    def __init__(self, group_name = None, display_only = False, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.display_only = display_only
        self.param_name_to_editable_dict = {}
        self.content_layout = QtGui.QFormLayout()
        self.main_layout = PYQT_SHARED.getGroupFormLayout(self.content_layout, group_name)
        self.setLayout(self.main_layout)
        Qt.QCoreApplication.processEvents()
        
    def displayParameters(self, param_name_type_default_tuples):
        self.param_name_to_editable_dict = {}
        for (name, typ, default) in param_name_type_default_tuples:
            label = self.getLabel(name, typ)
            editable = self.getEditable(typ, default)
            self.param_name_to_editable_dict[name] = editable
            self.content_layout.addRow(label, editable)
            Qt.QCoreApplication.processEvents()

    def getLabel(self, name, typ):
        label = QtGui.QLabel()
        label.setAlignment(Qt.Qt.AlignLeft)
        if typ == int:
            label.setText(Qt.QString((name + ' (int)')))
        elif typ == float:
            label.setText(Qt.QString((name + ' (float)')))
        else:
            label.setText(Qt.QString((name)))
        return label

    def getEditable(self, typ, default):
        if self.display_only:
            editable = QtGui.QLabel()
            editable.setAlignment(Qt.Qt.AlignLeft)
            if not default:
                editable.setText(Qt.QString((str(typ)))) 
            else:
                editable.setText(Qt.QString((str(default))))  
                
            return editable
        if typ == int or typ == float:
            editable = LINE_EDIT.AutoNumeralLineEdit(default)
        elif typ == str:
            editable = LINE_EDIT.AutoUpperLineEdit(default)
        elif typ == list:
            editable = LINE_EDIT.ListNumeralsLineEdit(default)
        elif typ == tuple: 
            editable = QtGui.QComboBox()
            editable.addItems(default)

        editable.changedSignal.connect(self.emitChangedSignal)
        return editable
    def emitChangedSignal(self):
        self.changedSignal.emit(self.getParametersNameValueDict())
            
    def getParametersNameValueDict(self):
        param_name_value_dict = {}
        for param_name in self.param_name_to_editable_dict.keys():
            editable = self.param_name_to_editable_dict[param_name]
            if isinstance(editable, QtGui.QComboBox):
                value = str(editable.currentText())
            elif isinstance(editable, LINE_EDIT.AutoNumeralLineEdit):
                value = float(editable.text())
            elif isinstance(editable, LINE_EDIT.AutoUpperLineEdit):
                value = str(editable.text())
            elif isinstance(editable, FilePathLineEdit):
                value = str(editable.text())
            param_name_value_dict[param_name] = value
        return param_name_value_dict


            
class Line(QtGui.QFrame):
    def __init__(self, orientation = 'Horizontal' , parent = None):
        QtGui.QFrame.__init__(self, parent)
        if orientation == 'Horizontal': 
            self.setFrameStyle(QtGui.QFrame.HLine)
        elif orientation == 'Vertical':
            self.setFrameStyle(QtGui.QFrame.VLine)
        self.setFixedHeight(5)
        self.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)





