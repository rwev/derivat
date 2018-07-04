'''
Defines functions to routinely process
PyQt components (layouts, widgets, etc.) 
and apply consistent settings / configurations
'''

import PyQt4.QtCore as Qt
import PyQt4.QtGui as QtGui

def setEqualRowHeight(form_layout, row_height):
    for i in range(0, form_layout.rowCount()):
        layout_item = form_layout.itemAt(i, QtGui.QFormLayout.FieldRole)
        if (layout_item and layout_item.widget()):
            layout_item.widget().setFixedHeight(row_height)

def applyFormLayoutSettings(content_layout):
    content_layout.setAlignment(Qt.Qt.AlignTop)
    content_layout.setLabelAlignment(Qt.Qt.AlignLeft)
    content_layout.setFormAlignment(Qt.Qt.AlignHCenter)
    content_layout.setRowWrapPolicy(QtGui.QFormLayout.DontWrapRows)
    content_layout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)  

def getGroupFormLayout(central_layout, group_name):
    outer_layout = QtGui.QVBoxLayout()
    group_box_widget = QtGui.QGroupBox(group_name) 
    content_layout = QtGui.QFormLayout()
    group_box_widget.setLayout(central_layout)
    outer_layout.addWidget(group_box_widget)
    return outer_layout 

def getIcon(source_filepath):
    # applies to all child windows     
    app_icon = QtGui.QIcon()
    app_icon.addFile(source_filepath, Qt.QSize(16,16))
    app_icon.addFile(source_filepath, Qt.QSize(24,24))
    app_icon.addFile(source_filepath, Qt.QSize(32,32))
    app_icon.addFile(source_filepath, Qt.QSize(48,48))
    app_icon.addFile(source_filepath, Qt.QSize(256,256))
    return app_icon