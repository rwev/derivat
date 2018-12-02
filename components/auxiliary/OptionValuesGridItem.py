
import pyqtgraph.opengl as gl

class OptionValuesGridItem(gl.GLGridItem):
    def __init__(self, parent = None):
        gl.GLGridItem.__init__(self, parent)

        self.last_x_translate = 0
        self.last_y_translate = 0

        self.x_size_strike_span = None
        self.y_size_expiration_span = None

        self.x_spacing_strike_incr = None
        self.y_spacing_expiration_incr = None
        
        self.translate(0, 0, -1)
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

    def translateOnRanges(self):
        self.translate(-self.last_x_translate, -self.last_y_translate, 0)
        self.last_x_translate = self.x_size_strike_span / 2.0
        self.last_y_translate = self.y_size_expiration_span / 2.0
        self.translate(self.last_x_translate, self.last_y_translate, 0)

    def updateVisibility(self):
        have_x = self.x_size_strike_span and self.x_spacing_strike_incr
        have_y = self.y_size_expiration_span and self.y_spacing_expiration_incr

        is_visible = have_x and have_y
        if is_visible:
            self.setSize(x = self.x_size_strike_span, y = self.y_size_expiration_span)
            self.setSpacing(x = self.x_spacing_strike_incr, y = self.y_spacing_expiration_incr)
            self.translateOnRanges()
        self.setVisible(is_visible)

    