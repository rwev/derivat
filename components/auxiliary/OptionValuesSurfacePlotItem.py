import pyqtgraph.opengl as gl
import numpy as np

from ..libs import VisualizationUtils as VIS_UTILS


class OptionValuesSurfacePlotItem(gl.GLSurfacePlotItem):
    def __init__(self, parent=None):
        gl.GLSurfacePlotItem.__init__(self, parent, computeNormals=False, smooth=True)
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
        self.z_values_2D = np.array(
            [[0.0] * len(self.y_expirations_1D)] * len(self.x_strikes_1D)
        )

    def translateOnRanges(self):
        self.translate(-self.last_x_translate, -self.last_y_translate, 0)
        self.last_x_translate = -self.x_strikes_1D[0]
        self.last_y_translate = -self.y_expirations_1D[0]
        self.translate(self.last_x_translate, self.last_y_translate, 0)

    def resetVisibility(self):
        are_strikes_defined = (
            isinstance(self.x_strikes_1D, np.ndarray) and self.x_strikes_1D.all()
        )
        are_expirations_defined = (
            isinstance(self.y_expirations_1D, np.ndarray)
            and self.y_expirations_1D.all()
        )

        if are_strikes_defined and are_expirations_defined:
            self.initializeValues()
            self.translateOnRanges()
        self.setVisible(False)

    def makeVisible(self, (min_value, max_value)):
        self.transformData((min_value, max_value))
        self.setData(
            x=self.x_strikes_1D,
            y=self.y_expirations_1D,
            z=self.z_values_2D,
            colors=self.generateColors((min_value, max_value)),
        )
        self.setVisible(True)

    def generateColors(self, (min_value, max_value)):
        colors = np.full((self.z_values_2D.shape[0], self.z_values_2D.shape[1], 4), 0.0)
        for i in range(len(self.z_values_2D)):
            for j in range(len(self.z_values_2D[i])):
                colors[i][j] = np.array(
                    VIS_UTILS.colormap((self.z_values_2D[i][j] + 1) / (2))
                )
        return colors

    def transformData(self, (min_value, max_value)):
        self.z_values_2D = VIS_UTILS.map2DArray(
            lambda z: VIS_UTILS.mapValueToRange(min_value, max_value, -1, 1, z),
            self.z_values_2D,
        )
