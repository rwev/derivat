
import pyqtgraph.opengl as gl
import numpy as np

class OptionValuesSurfacePlotItem(gl.GLSurfacePlotItem):
    def __init__(self, parent = None):
        gl.GLSurfacePlotItem.__init__(self, parent)
        self.reset()

    def reset(self):
        self.x_strikes_1D = None
        self.y_expirations_1D = None
        self.z_values_2D = None
        self.updateVisibility()

    def resetStrikeList(self):
        self.x_strikes_1D = None
        self.updateVisibility()
    def setStrikeList(self, strike_list):
        self.x_strikes_1D = np.array(strike_list)
        self.updateVisibility()

    def resetExpirationList(self):
        self.y_expirations_1D = None
        self.updateVisibility()
    def setExpirationList(self, expiration_list):
        self.y_expirations_1D = np.array(expiration_list)
        self.updateVisibility()

    def updateValue(self, (strike_index, expiration_index, value)):
        self.z_values_2D[expiration_index][strike_index] = value
        self.setData(x = self.y_expirations_1D, y = self.x_strikes_1D, z = self.z_values_2D)

    def initializeValues(self):
        self.z_values_2D = np.array([[0.0] * len(self.x_strikes_1D)] * len(self.y_expirations_1D))

    def updateVisibility(self):
        are_strikes_defined = isinstance(self.x_strikes_1D, np.ndarray) and self.x_strikes_1D.all()
        are_expirations_defined = isinstance(self.y_expirations_1D, np.ndarray) and self.y_expirations_1D.all()

        is_visible = are_strikes_defined and are_expirations_defined

        if is_visible:
            self.initializeValues()

        self.setVisible(is_visible)

    


