
import pyqtgraph as pg
import pyqtgraph.opengl as gl

class OptionValuesSurfacePlotItem(gl.GLSurfacePlotItem):
    def __init__(self, parent = None):
        gl.GLSurfacePlotItem.__init__(self, parent)
        
        self.x_strikes = None
        self.y_expirations = None
        self.z_values = None

    def setStrikeList(self, strike_list):
        self.x_strikes = strike_list
        self.updateGrid()

    def setExpirationList(self, expiration_list):
        self.y_expirations = expiration_list
        self.updateGrid()

    


