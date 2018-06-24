# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 11:39:53 2016

@author: Ryan
"""

import PyQt4.QtCore as Qt
import PyQt4.QtGui as QtGui

import lineEdit

class ParameterNumericListWidget(QtGui.QWidget):
    changedSignal = Qt.pyqtSignal(object)
    def __init__(self, group_name = None, display_only = False, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.display_only = display_only
        self.param_name_to_editable_dict = {}
        self.main_layout = QtGui.QVBoxLayout()
        self.addGroupNameLabel(self.main_layout, group_name)
        self.setLayout(self.main_layout)
        Qt.QCoreApplication.processEvents()

    def addGroupNameLabel(self, layout, group_name):
        if group_name is not None:
            label = QtGui.QLabel(group_name)
            label.setAlignment(Qt.Qt.AlignHCenter)
            layout.addWidget(label)
        
    def displayParameters(self, param_name_default_tuples):
        self.param_name_to_editable_dict = {}
        for (name, default) in param_name_default_tuples:
            label = self.getLabel(name)
            editable = self.getEditable(default)
            self.main_layout.addWidget(label)
            self.main_layout.addWidget(editable)
            self.param_name_to_editable_dict[name] = editable
            Qt.QCoreApplication.processEvents()

    def getLabel(self, name):
        label = QtGui.QLabel()
        label.setAlignment(Qt.Qt.AlignLeft)
        label.setText(Qt.QString((name)))
        return label

    def getEditable(self, default):
        editable = lineEdit.ListNumeralsLineEdit(default)
        editable.changedSignal.connect(self.emitChangedSignal)
        return editable

    def emitChangedSignal(self):
        print 'emitChangedSignal'
        self.changedSignal.emit(self.getParametersNameValueDict())
            
    def getParametersNameValueDict(self):
        param_name_value_dict = {}
        for param_name in self.param_name_to_editable_dict.keys():
            editable = self.param_name_to_editable_dict[param_name]
            values = str(editable.value())
            param_name_value_dict[param_name] = values
        return param_name_value_dict

class ParameterSelectionWidget(QtGui.QWidget):
    changedSignal = Qt.pyqtSignal(object)
    def __init__(self, group_name = None, display_only = False, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.display_only = display_only
        self.param_name_to_editable_dict = {}
        self.main_layout = QtGui.QFormLayout()
        self.addGroupNameLabel(self.main_layout, group_name)
        self.setLayout(self.main_layout)
        Qt.QCoreApplication.processEvents()

    def addGroupNameLabel(self, layout, group_name):
        if group_name is not None:
            label = QtGui.QLabel(group_name)
            label.setAlignment(Qt.Qt.AlignHCenter)
            layout.addRow(label)
        
    def displayParameters(self, param_name_type_default_tuples):
        self.param_name_to_editable_dict = {}
        for (name, typ, default) in param_name_type_default_tuples:
            label = self.getLabel(name, type)
            editable = self.getEditable(typ, default)
            self.param_name_to_editable_dict[name] = editable
            self.main_layout.addRow(label, editable)
            Qt.QCoreApplication.processEvents()

    def getLabel(self, name, typ):
        label = QtGui.QLabel()
        label.setAlignment(Qt.Qt.AlignLeft)
        if isinstance(typ, int):
            label.setText(Qt.QString((name + ' (int)')))
        elif isinstance(typ, float):
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
            editable = lineEdit.AutoNumeralLineEdit(default)
        elif typ == str:
            editable = lineEdit.AutoUpperLineEdit(default)
        elif typ == file:
            editable = FilePathLineEdit(default)
        # TODO: handle tuple type
        # elif isinstance(typ, tuple):
        #     editable = QComboBox()
        #     if typ == () and isinstance(default_combo, tuple): # if empty, check if default combo was passed
        #         editable.addItems(default_combo)
        #     elif len(typ) > 0:
        #         editable.addItems(typ)
        #     if default:
        #         editable.setCurrentIndex(list(typ).index(default))
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
            elif isinstance(editable, lineEdit.AutoNumeralLineEdit):
                value = float(editable.text())
            elif isinstance(editable, lineEdit.AutoUpperLineEdit):
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

# TODO: refactor ItemSelectionDialog
class ItemSelectionDialog(QtGui.QMainWindow):
    selectionDoneSignal = Qt.pyqtSignal(object) # emits list of selected fields
    def __init__(self, items = [], max_num_choices = None, parent = None):
        QtGui.QMainWindow.__init__(self, parent)
        self.items = items          # list of strings
        self.list_widget_items = [] # list of QListWidgetItems
        
        self.list_widget = QtGui.QListWidget()
        self.list_widget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        for item in self.items:
            list_widget_item = QtGui.QListWidgetItem(item)
            self.list_widget_items.append(list_widget_item)
            self.list_widget.addItem(list_widget_item)
            
        self.list_widget.setFixedSize(225, 450)
        
        self.done_button = QtGui.QPushButton('OK')
        self.done_button.clicked.connect(self.emitSelection)
        self.done_button.setFixedSize(112,20)
        self.filler_label = QtGui.QLabel('')
        self.filler_label.setFixedSize(112,20)
        
        self.main_layout = QtGui.QFormLayout()
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(10,10,10,10)
        self.main_layout.addRow(self.list_widget)
        self.main_layout.addRow(self.filler_label, self.done_button)
        
        self.frame = QtGui.QWidget()
        self.frame.setLayout(self.main_layout)
        self.setCentralWidget(self.frame)
        
        self.setFixedSize(245, 490)
        if max_num_choices is None:
            self.setWindowTitle('Item Selection')
        else:
            self.max_num_choices = max_num_choices
            self.setWindowTitle('Item Selection (Max ' + str(max_num_choices) + ' choices)' )
            self.list_widget.itemSelectionChanged.connect(self.manageMaxSelection)
        self.show()
        self.activateWindow()
        Qt.QCoreApplication.processEvents()
    def emitSelection(self):
        # generates list of selected fields
        # emits in signal
        # kills self
        selected_idxs = [x.row() for x in self.list_widget.selectedIndexes()]
        selected_items = [self.items[idx] for idx in selected_idxs]
        self.selectionDoneSignal.emit(selected_items)
        self.close() # close after selection emitted.
    def manageMaxSelection(self):
        # if too many items have been selected, reset by deselecting all.
        selected_idxs = [x.row() for x in self.list_widget.selectedIndexes()]
        if len(selected_idxs) > self.max_num_choices:
            for list_widget_item in self.list_widget_items:
                list_widget_item.setSelected(False)

# TODO: refactor FilePathLineEdit        
class FilePathLineEdit(QtGui.QLineEdit):
    def __init__(self, default_path = None, parent=None):
        super(FilePathLineEdit, self).__init__()
        self.button = QtGui.QToolButton()
        self.button.setIcon(QtGui.QIcon('folder_icon.ico'))
        self.button.setStyleSheet("background: transparent; border: none;")
        self.button.setFixedSize(20, 20)
        self.button.clicked.connect(self.selectFolder)
        
        layout = QtGui.QHBoxLayout()
        layout.setAlignment(Qt.Qt.AlignRight)
        layout.addWidget(self.button)
        layout.setSpacing(0)
        layout.setContentsMargins(0,0,0,0)
        self.setLayout(layout)
        Qt.QCoreApplication.processEvents()
        
    def selectFolder(self):
        filepath = str(QtGui.QFileDialog.getOpenFileName())
        if filepath:
            self.setText(filepath)


