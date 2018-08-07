
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
 
        self.option_style_widget = BUILD_CONTROLS.buildOptionStyleWidget()
        self.option_type_widget = BUILD_CONTROLS.buildOptionTypeWidget()
        self.output_type_widget = BUILD_CONTROLS.buildOutputTypeWidget()

        self.input_factors_widget = BUILD_CONTROLS.buildInputFactorsWidget()
        self.strikes_widget = BUILD_CONTROLS.buildStrikeDimensionsWidget()
        self.expirations_widget = BUILD_CONTROLS.buildExpirationDimensionsWidget()

        actions_widget = BUILD_CONTROLS.buildActionsWidget()

        progress_bar_container_widget = self.buildProgressBar()

        self.option_style_widget.changedSignal.connect(self.onOptionStyleChange)
        self.option_type_widget.changedSignal.connect(self.onOptionTypeChange)
        self.output_type_widget.changedSignal.connect(self.onOutputTypeChange)

        self.input_factors_widget.changedSignal.connect(self.onInputFactorChange)
        self.strikes_widget.changedSignal.connect(self.onStrikeDimensionChange)
        self.expirations_widget.changedSignal.connect(self.onExpirationDimensionChange)

        actions_widget.actionSignal.connect(self.handleAction)

        splitter.addWidget(self.option_style_widget)
        splitter.addWidget(self.option_type_widget)
        splitter.addWidget(self.input_factors_widget)
        splitter.addWidget(self.strikes_widget)
        splitter.addWidget(self.expirations_widget)
        splitter.addWidget(self.output_type_widget)
        splitter.addWidget(actions_widget)
        splitter.addWidget(progress_bar_container_widget)

        return splitter

    def handleAction(self, action):
        if (action == CONSTANTS.window.action.clear_):
            self.clearInputs()
        elif (action == CONSTANTS.window.action.calculate):
            self.priceIfReady()
        elif (action == CONSTANTS.window.action.load):
            self.loadSettings()
        elif (action == CONSTANTS.window.action.save):
            self.saveSettings()

    def clearInputs(self):
        self.option_style_widget.clearSelection()
        self.option_type_widget.clearSelection()
        self.output_type_widget.clearSelection()

        self.input_factors_widget.clearForm()
        self.strikes_widget.clearForm()
        self.expirations_widget.clearForm()
        
    def buildProgressBar(self):

        progress_bar_container_widget = QtGui.QWidget()

        layout = QtGui.QHBoxLayout()
        progress_bar_container_widget.setLayout(layout)

        self.progress_bar = PROGRESS_BAR.IncrementalProgressBar()

        layout.addWidget(self.progress_bar)
    
        return progress_bar_container_widget 

    def onOptionStyleChange(self, selected_option):
        pricing_controller.setOptionStyle(selected_option)
    def onOptionTypeChange(self, selected_option):
        pricing_controller.setOptionType(selected_option)
    def onOutputTypeChange(self, selected_option):
        pricing_controller.setOutputType(selected_option)
    def onInputFactorChange(self, input_factors_dict):
        pricing_controller.setFactorsDict(input_factors_dict)
    def onStrikeDimensionChange(self, strike_dimensions_dict):
        pricing_controller.setStrikesDict(strike_dimensions_dict)
        if pricing_controller.areStrikesValid():
            self.values_table.updateStrikeColumns(pricing_controller.getStrikesList())
    def onExpirationDimensionChange(self, expiration_dimensions_dict):
        pricing_controller.setExpirationsDict(expiration_dimensions_dict)
        if pricing_controller.areExpirationsValid():
            self.values_table.updateExpirationRows(pricing_controller.getExpirationsList())

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
        
        values_tab =   QtGui.QWidget()

        self.buildValuesTab(values_tab)

        tabs.addTab(values_tab, CONSTANTS.window.tabs.values_)

        return tabs
    def buildValuesTab(self, tab):
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

    def saveSettings(self):
        print('saveSettings [TO IMPLEMENT]')

    def printSettings(self, settingsMBD):
        print(settingsMBD)

def main():
    app = QtGui.QApplication(argv)  
    main = MainWindow()
    exit(app.exec_())

if __name__ == "__main__":
    main()

