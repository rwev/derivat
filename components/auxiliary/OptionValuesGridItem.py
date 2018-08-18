
import pyqtgraph.opengl as gl

class OptionValuesGridItem(gl.GLGridItem):
    def __init__(self, parent = None):
        gl.GLGridItem.__init__(self, parent)

        self.x_size_strike_span = None
        self.y_size_expiration_span = None

        self.x_spacing_strike_incr = None
        self.y_spacing_expiration_incr = None
        
        self.updateVisibility()

    def resetStrikeRange(self):
        self.x_size_strike_span = None
        self.x_spacing_strike_incr = None
        self.updateVisibility()
    def setStrikeRange(self, min_, incr, max_ ):
        self.x_size_strike_span = max_ - min_
        self.x_spacing_strike_incr = incr
        self.updateVisibility()
    
    def resetExpirationRange(self):
        self.y_size_expiration_span = None
        self.y_spacing_expiration_incr = None
        self.updateVisibility()
    def setExpirationRange(self, min_, incr, max_):
        self.y_size_expiration_span = max_ - min_
        self.y_spacing_expiration_incr = incr
        self.updateVisibility()

    def updateVisibility(self):
        have_x = self.x_size_strike_span and self.x_spacing_strike_incr
        have_y = self.y_size_expiration_span and self.y_spacing_expiration_incr

        is_visible = have_x and have_y
        if is_visible:
            self.setSize(x = self.x_size_strike_span, y = self.y_size_expiration_span)
            self.setSpacing(x = self.x_spacing_strike_incr, y = self.y_spacing_expiration_incr)

        self.setVisible(is_visible)

    