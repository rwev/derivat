
import pyqtgraph.opengl as gl

class OptionValuesAxisItem(gl.GLAxisItem):
    def __init__(self, parent = None):
        gl.GLAxisItem.__init__(self, parent)

        self.x_size_strike_span = None
        self.y_size_expiration_span = None

        self.translate(0, 0, -1)
        self.updateVisibility()

    def resetStrikeRange(self):
        self.x_size_strike_span = None
        self.updateVisibility()
    def setStrikeRange(self, min_, incr, max_ ):
        self.x_size_strike_span = max_ - min_
        self.updateVisibility()
    
    def resetExpirationRange(self):
        self.y_size_expiration_span = None
        self.updateVisibility()
    def setExpirationRange(self, min_, incr, max_):
        self.y_size_expiration_span = max_ - min_
        self.updateVisibility()

    def updateVisibility(self):
        is_visible = self.x_size_strike_span and self.y_size_expiration_span
        if is_visible:
            self.setSize(x = self.x_size_strike_span, y = self.y_size_expiration_span, z = 10)

        self.setVisible(is_visible)

    