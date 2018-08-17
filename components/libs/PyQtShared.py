'''
Defines functions to routinely process
PyQt components (layouts, widgets, etc.) 
and apply consistent settings / configurations
'''

import PyQt4.QtCore as Qt
import PyQt4.QtGui as QtGui

def setGroupBoxValidity(group_box_widget, is_valid):
    if is_valid:
        group_box_widget.setStyleSheet('::title { color: green; }')
    elif not is_valid:
        group_box_widget.setStyleSheet('::title { color: red; }')

def getIcon(source_filepath):
    # applies to all child windows     
    app_icon = QtGui.QIcon()
    app_icon.addFile(source_filepath, Qt.QSize(16,16))
    app_icon.addFile(source_filepath, Qt.QSize(24,24))
    app_icon.addFile(source_filepath, Qt.QSize(32,32))
    app_icon.addFile(source_filepath, Qt.QSize(48,48))
    app_icon.addFile(source_filepath, Qt.QSize(256,256))
    return app_icon