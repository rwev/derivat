"""
Implements short extensions of standard PyQt Objects
"""


import PyQt4.QtCore as Qt
import PyQt4.QtGui as QtGui


class Line(QtGui.QFrame):
    def __init__(self, orientation="Horizontal", parent=None):
        QtGui.QFrame.__init__(self, parent)
        if orientation == "Horizontal":
            self.setFrameStyle(QtGui.QFrame.HLine)
        elif orientation == "Vertical":
            self.setFrameStyle(QtGui.QFrame.VLine)
        self.setFixedHeight(5)
        self.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
