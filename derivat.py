
import os
from sys import exit, argv
import PyQt4.QtCore as Qt
import PyQt4.QtGui as QtGui

import components.auxiliary.CustomInputs as CUSTOM
import components.auxiliary.LineEdit as LINE_EDIT
import components.auxiliary.AutoAxisTable as AUTO_TABLE
import components.auxiliary.PricingController as PRICE_CONTROL

import components.libs.PyQtShared as PYQT_SHARED
from components.libs.Constants import derivat_constants as CONSTANTS

import components.threads.SerializationThreads as SERIAL

pricing_controller = PRICE_CONTROL.PricingController()
class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self, parent)

        self.buildGui()
        self.show()
        self.activateWindow()
        self.loadSettings()

    def buildGui(self):

        self.setWindowTitle(CONSTANTS.window.title)
        self.setIcon()

        splitter = QtGui.QSplitter(Qt.Qt.Horizontal)

        settings_widget = self.buildSettings()
        view_widget = self.buildView()

        splitter.addWidget(settings_widget)
        splitter.addWidget(view_widget)

        self.setCentralWidget(splitter)
        
        Qt.QCoreApplication.processEvents()

    def buildSettings(self):

        splitter = QtGui.QSplitter(Qt.Qt.Vertical)

        input_factors_widget = CUSTOM.ParameterSelectionWidget(group_name = CONSTANTS.window.pricing.inputs)
        input_factors_widget.displayParameters(param_name_type_default_tuples = 
            (
                (CONSTANTS.window.pricing.input_factors.spot_price,     float,  None),
                (CONSTANTS.window.pricing.input_factors.interest_rate,  float,  None),
                (CONSTANTS.window.pricing.input_factors.carry_rate,     float,  None),
                (CONSTANTS.window.pricing.input_factors.volatility,     float,  None),
                (CONSTANTS.window.pricing.input_factors.option_type,    tuple,  (
                                                        CONSTANTS.window.pricing.types.american, 
                                                        CONSTANTS.window.pricing.types.european
                                                        )
                )
            )
        )

        strikes_widget = CUSTOM.ParameterSelectionWidget(group_name = CONSTANTS.window.pricing.input_dimensions.strikes)
        strikes_widget.displayParameters(param_name_type_default_tuples = 
            (
                (CONSTANTS.window.pricing.input_dimensions.strike_start,  float, None),
                (CONSTANTS.window.pricing.input_dimensions.strike_step,   float, None),
                (CONSTANTS.window.pricing.input_dimensions.strike_stop,   float, None)
            )
        )

        expirations_widget = CUSTOM.ParameterSelectionWidget(group_name = CONSTANTS.window.pricing.input_dimensions.expirations)
        expirations_widget.displayParameters(param_name_type_default_tuples = 
            (
                (CONSTANTS.window.pricing.input_dimensions.expiration_start, float, None),
                (CONSTANTS.window.pricing.input_dimensions.expiration_step,  float, None),
                (CONSTANTS.window.pricing.input_dimensions.expiration_stop,  float, None)
            )
        )

        strikes_widget.changedSignal.connect(self.onStrikeDimensionChange)
        expirations_widget.changedSignal.connect(self.onExpirationDimensionChange)

        splitter.addWidget(input_factors_widget)
        splitter.addWidget(strikes_widget)
        splitter.addWidget(expirations_widget)

        return splitter

    def onStrikeDimensionChange(self, strike_dimensions_dict):
        pricing_controller.setStrikesDict(strike_dimensions_dict)
        if pricing_controller.areStrikesValid():
            self.prices_table.updateColumnLabels(pricing_controller.getStrikesList())

    def onExpirationDimensionChange(self, expiration_dimensions_dict):
        pricing_controller.setExpirationsDict(expiration_dimensions_dict)
        if pricing_controller.areExpirationsValid():
            self.prices_table.updateRowLabels(pricing_controller.getExpirationsList())

    def buildView(self):
        tabs = QtGui.QTabWidget()
        self.buildViewsTabs(tabs)
        return tabs

    def buildViewsTabs(self, tabs):
        
        prices_tab =   QtGui.QWidget()
        graphs_tab =   QtGui.QWidget()

        self.buildPricesTab(prices_tab)
        self.buildGraphsTab(graphs_tab)

        tabs.addTab(prices_tab, CONSTANTS.window.tabs.prices)
        tabs.addTab(graphs_tab, CONSTANTS.window.tabs.graphs)

        return tabs
     
    def buildPricesTab(self, tab):
        layout = QtGui.QVBoxLayout()
        layout.setAlignment(Qt.Qt.AlignTop)
        self.prices_table = AUTO_TABLE.AutoAxisTable()
        layout.addWidget(self.prices_table)
        tab.setLayout(layout)
        return

    def buildGraphsTab(self, tab):

        import pyqtgraph as pg
        import pyqtgraph.opengl as gl
        import numpy as np

        view = gl.GLViewWidget()

        ## create three grids, add each to the view
        xgrid = gl.GLGridItem()
        ygrid = gl.GLGridItem()
        zgrid = gl.GLGridItem()

        xgrid.scale(1, 1, 1)
        ygrid.scale(1, 1, 1)
        zgrid.scale(1, 1, 1)

        xgrid.setSpacing(1, 1, 1)
        ygrid.setSpacing(1, 1, 1)
        zgrid.setSpacing(1, 1, 1)

        view.addItem(xgrid)
        view.addItem(ygrid)
        view.addItem(zgrid)

        xx = np.array([0, 10])
        yy = np.array([0, 10]) 
        zz = np.array([0, 10]) 

        means = [xx.mean(), yy.mean(), zz.mean()]  
        stds = [xx.std() / 3, yy.std() / 3, yy.std() / 3]

        xy_corr = 0.6         
        yz_corr = -0.8
        xz_corr = -0.6

        covs = [
                [stds[0]**2,                stds[0]*stds[1]*xy_corr,    stds[0]*stds[2]*xz_corr], 
                [stds[1]*stds[0]*xy_corr,   stds[1]**2,                 stds[1]*stds[2]*yz_corr],
                [stds[2]*stds[0]*xz_corr,   stds[2]*stds[1]*yz_corr,    stds[2]**2] 
                ]

        m = np.random.multivariate_normal(means, covs, 1000).T # (3 x 1000)

        # print m
        pos = np.array([(c[0], c[1], c[2]) for c in m.T])
        # print m.shape
        # print pos

        scatter = gl.GLScatterPlotItem(pos=pos, size=0.1, pxMode=False)
        view.addItem(scatter)

        view.show()
        layout = QtGui.QVBoxLayout()
        layout.setAlignment(Qt.Qt.AlignTop)
        #layout.addWidget(view)
        
        tab.setLayout(layout)
        
        Qt.QCoreApplication.processEvents()
        return

    def closeEvent(self, event):
        quit_title = CONSTANTS.window.messages.exit.title
        quit_msg = CONSTANTS.window.messages.exit.description
        reply = QtGui.QMessageBox.question(self, 
                                            quit_title,
                                            quit_msg,
                                            QtGui.QMessageBox.Yes, 
                                            QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def setIcon(self):
        source = CONSTANTS.sources.icon
        app_icon = PYQT_SHARED.getIcon(source)
        self.setWindowIcon(app_icon)

    def loadSettings(self):
        self.load_thread = SERIAL.LoadYAMLThread()
        self.load_thread.resultsSignal.connect(self.printSettings)
        self.load_thread.start()

    def printSettings(self, settingsMBD):
        print(settingsMBD)

def main():
    app = QtGui.QApplication(argv)  
    main = MainWindow()
    exit(app.exec_())

if __name__ == "__main__":
    main()

