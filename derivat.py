
import os
from sys import exit, argv
import PyQt4.QtCore as Qt
import PyQt4.QtGui as QtGui

import components.auxiliary.CustomInputs as CUSTOM
import components.auxiliary.LineEdit as LINE_EDIT
import components.auxiliary.AutoAxisTable as AUTO_TABLE

import components.lib.PyQtShared as PYQT_SHARED

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self, parent)
        self.buildGui()
        self.show()
        self.activateWindow()

    def buildGui(self):

        self.setWindowTitle('derivat')
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

        params_widget = CUSTOM.ParameterSelectionWidget(group_name = 'Pricing Inputs')
        params_widget.displayParameters(param_name_type_default_tuples = 
                                        (('Spot',                   float,  None),
                                        ('Interest Rate (% p.a.)',  float,  None),
                                        ('Carry (% p.a.)',          float,  None),
                                        ('Volatility (% p.a.)',     float,  None),
                                        ('Option Type',             tuple,  ('American', 'European'))))

        params_list_widget = CUSTOM.ParameterSelectionWidget(group_name = 'Pricing Dimensions')
        params_list_widget.displayParameters(param_name_type_default_tuples = 
                                            (('Strikes', list, None),
                                            ('Expirations (days)', list, None)))

        splitter.addWidget(params_widget)
        splitter.addWidget(params_list_widget)

        return splitter

    def updatePriceTableAxis(self, param_name_values_dict):
        self.prices_table.updateColumnLabels(param_name_values_dict['Strikes'])
        self.prices_table.updateRowLabels(param_name_values_dict['Expirations (days)'])

    def buildView(self):
        tabs = QtGui.QTabWidget()
        self.buildViewsTabs(tabs)
        return tabs

    def buildViewsTabs(self, tabs):
        
        prices_tab =   QtGui.QWidget()
        graphs_tab =   QtGui.QWidget()

        self.buildPricesTab(    prices_tab)
        self.buildGraphsTab(    graphs_tab)

        tabs.addTab(prices_tab,   'Prices')
        tabs.addTab(graphs_tab,   'Graphs')

        return tabs
     
    def buildPricesTab(self, tab):
        layout = QtGui.QVBoxLayout()
        layout.setAlignment(Qt.Qt.AlignTop)
        #layout.addWidget(view)
        self.prices_table = AUTO_TABLE.AutoAxisTable(range(5), range(5))
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
        # overwrite the default QMainWindow close
        # behavior in order to verify

        return

        quit_title = "Confirm Exit"
        quit_msg = 'Close derivat? Any unsaved pricing configuration will be lost.'
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
        source = 'assets/gamma.png'
        app_icon = PYQT_SHARED.getIcon(source)
        self.setWindowIcon(app_icon)

def main():
    app = QtGui.QApplication(argv)  
    main = MainWindow()
    exit(app.exec_())

if __name__ == "__main__":
    main()

