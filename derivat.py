
import os
from sys import exit, argv
import PyQt4.QtCore as Qt
import PyQt4.QtGui as QtGui

import components.auxiliary.AssistControlsBuild as BUILD_CONTROLS
import components.auxiliary.NumericInputGroupBox as CUSTOM
import components.auxiliary.LineEdit as LINE_EDIT
import components.auxiliary.OptionValuesTable as OPT_VAL_TABLE
import components.auxiliary.IncrementalProgressBar as PROGRESS_BAR
import components.auxiliary.PricingController as PRICE_CONTROL


import components.libs.PyQtShared as PYQT_SHARED
from components.libs.Constants import constants as CONSTANTS

import components.threads.SerializationThreads as SERIAL
import components.threads.PricingThread as PRICE

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

        controls_widget = self.buildControls()
        view_widget = self.buildView()

        splitter.addWidget(controls_widget)
        splitter.addWidget(view_widget)

        self.setCentralWidget(splitter)
        
        Qt.QCoreApplication.processEvents()

    def buildControls(self):

        splitter = QtGui.QSplitter(Qt.Qt.Vertical)
 
        option_style_widget = BUILD_CONTROLS.buildOptionStyleWidget()
        option_type_widget = BUILD_CONTROLS.buildOptionTypeWidget()
        output_type_widget = BUILD_CONTROLS.buildOutputTypeWidget()

        input_factors_widget = BUILD_CONTROLS.buildInputFactorsWidget()
        strikes_widget = BUILD_CONTROLS.buildStrikeDimensionsWidget()
        expirations_widget = BUILD_CONTROLS.buildExpirationDimensionsWidget()

        progress_bar_container_widget = self.buildProgressBar()

        option_style_widget.changedSignal.connect(self.onOptionStyleChange)
        option_type_widget.changedSignal.connect(self.onOptionTypeChange)
        output_type_widget.changedSignal.connect(self.onOutputTypeChange)

        input_factors_widget.changedSignal.connect(self.onInputFactorChange)
        strikes_widget.changedSignal.connect(self.onStrikeDimensionChange)
        expirations_widget.changedSignal.connect(self.onExpirationDimensionChange)

        splitter.addWidget(option_style_widget)
        splitter.addWidget(option_type_widget)
        splitter.addWidget(input_factors_widget)
        splitter.addWidget(strikes_widget)
        splitter.addWidget(expirations_widget)
        splitter.addWidget(output_type_widget)
        splitter.addWidget(progress_bar_container_widget)

        return splitter

    def buildProgressBar(self):

        progress_bar_container_widget = QtGui.QWidget()

        layout = QtGui.QHBoxLayout()
        progress_bar_container_widget.setLayout(layout)

        self.progress_bar = PROGRESS_BAR.IncrementalProgressBar()

        layout.addWidget(self.progress_bar)
    
        return progress_bar_container_widget 

    def onOptionStyleChange(self, selected_option):
        pricing_controller.setOptionStyle(selected_option)
        self.priceIfReady()

    def onOptionTypeChange(self, selected_option):
        pricing_controller.setOptionType(selected_option)
        self.priceIfReady()
    
    def onOutputTypeChange(self, selected_option):
        pricing_controller.setOutputType(selected_option)
        self.priceIfReady()

    def onInputFactorChange(self, input_factors_dict):
        pricing_controller.setFactorsDict(input_factors_dict)
        self.priceIfReady()

    def onStrikeDimensionChange(self, strike_dimensions_dict):
        pricing_controller.setStrikesDict(strike_dimensions_dict)
        if pricing_controller.areStrikesValid():
            self.values_table.updateStrikeColumns(pricing_controller.getStrikesList())
        self.priceIfReady()

    def onExpirationDimensionChange(self, expiration_dimensions_dict):
        pricing_controller.setExpirationsDict(expiration_dimensions_dict)
        if pricing_controller.areExpirationsValid():
            self.values_table.updateExpirationRows(pricing_controller.getExpirationsList())
        self.priceIfReady()

    def priceIfReady(self):
        if pricing_controller.readyToPrice():

            self.prepareProgressBar()
            self.price_thread = self.preparePricingThread()
            
            self.values_table.clearContents()
            self.price_thread.resultSignal.connect(self.values_table.updateValue)
            self.price_thread.resultSignal.connect(self.progress_bar.increment)

            self.price_thread.start()


    def prepareProgressBar(self):

        self.progress_bar.resetToIncrement()
        self.progress_bar.setMaximumIncrements(pricing_controller.getNumberOfCalculations())
    
    def preparePricingThread(self):
        price_thread = PRICE.PricingThread()

        price_thread.setOptionStyle(pricing_controller.getOptionStyle())
        price_thread.setOptionType(pricing_controller.getOptionType())
        price_thread.setOutputType(pricing_controller.getOutputType())

        price_thread.setFactors(*pricing_controller.getFactors())

        price_thread.setStrikesList(pricing_controller.getStrikesList())
        price_thread.setExpirationsList(pricing_controller.getExpirationsList())

        return price_thread

    def buildView(self):
        tabs = QtGui.QTabWidget()
        self.buildViewsTabs(tabs)
        return tabs

    def buildViewsTabs(self, tabs):
        
        prices_tab =   QtGui.QWidget()
        graphs_tab =   QtGui.QWidget()

        self.buildPricesTab(prices_tab)

        tabs.addTab(prices_tab, CONSTANTS.window.tabs.prices)

        return tabs
     
    def buildPricesTab(self, tab):
        layout = QtGui.QVBoxLayout()
        layout.setAlignment(Qt.Qt.AlignTop)
        self.values_table = OPT_VAL_TABLE.OptionValuesTable()
        layout.addWidget(self.values_table)
        tab.setLayout(layout)
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

