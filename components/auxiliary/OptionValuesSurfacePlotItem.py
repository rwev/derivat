
import pyqtgraph.opengl as gl
import numpy as np

class OptionValuesSurfacePlotItem(gl.GLSurfacePlotItem):
    def __init__(self, parent = None):
        gl.GLSurfacePlotItem.__init__(self, parent, computeNormals = False, smooth = True)
        self.setShader('heightColor')
        self.reset()

    def reset(self):

        self.last_x_translate = 0
        self.last_y_translate = 0

        self.x_strikes_1D = None
        self.y_expirations_1D = None
        self.z_values_2D = None
        
        self.resetVisibility()

    def resetStrikeList(self):
        self.x_strikes_1D = None
        self.resetVisibility()
    def setStrikeList(self, strike_list):
        self.x_strikes_1D = np.array(strike_list)
        self.resetVisibility()

    def resetExpirationList(self):
        self.y_expirations_1D = None
        self.resetVisibility()
    def setExpirationList(self, expiration_list):
        self.y_expirations_1D = np.array(expiration_list)
        self.resetVisibility()

    def updateValue(self, (strike_index, expiration_index, value)):
        self.z_values_2D[strike_index][expiration_index] = value

    def initializeValues(self):
        self.z_values_2D = np.array([[0.0] * len(self.y_expirations_1D)] * len(self.x_strikes_1D))
    def translateOnRanges(self):
        self.translate(-self.last_x_translate, -self.last_y_translate, 0)
        self.last_x_translate = -self.x_strikes_1D[0]
        self.last_y_translate = -self.y_expirations_1D[0]
        self.translate(self.last_x_translate, self.last_y_translate, 0)

    def resetVisibility(self):
        are_strikes_defined = isinstance(self.x_strikes_1D, np.ndarray) and self.x_strikes_1D.all()
        are_expirations_defined = isinstance(self.y_expirations_1D, np.ndarray) and self.y_expirations_1D.all()

        if are_strikes_defined and are_expirations_defined:
            self.initializeValues()
            self.translateOnRanges()
        self.setVisible(False)

    def makeVisible(self):
        self.transformData()
        self.setData(x = self.x_strikes_1D, y = self.y_expirations_1D, z = self.z_values_2D)
        self.setVisible(True)

    def transformData(self):
        min_ = np.amin(self.z_values_2D)
        max_ = np.amax(self.z_values_2D)
        self.z_values_2D = map2DArray(lambda z : mapValueToRange(min_, max_, -1, 1, z), self.z_values_2D)

def map2DArray(func, arr):
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            arr[i][j] = func(arr[i][j])
    return arr  

def mapValueToRange(old_min, old_max, new_min, new_max, value):
    old_range = old_max - old_min
    new_range = new_max - new_min
    scaled_value = float(value - old_min) / float(old_range)
    return new_min + (scaled_value * new_range)
    


