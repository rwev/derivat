
import os
from sys import exit, argv
import PyQt4.QtCore as Qt
import PyQt4.QtGui as QtGui

import components.auxiliary.AssistControlsBuild as BUILD_CONTROLS
import components.auxiliary.NumericInputGroupBox as CUSTOM
import components.auxiliary.LineEdit as LINE_EDIT
import components.auxiliary.OptionValuesTable as OPT_VAL_TABLE
import components.auxiliary.IncrementalProgressBar as PROGRESS_BAR
import components.auxiliary.Globals as GLOBALS

import components.libs.PyQtShared as PYQT_SHARED
from components.libs.Constants import constants as CONSTANTS

import components.threads.SerializationThreads as SERIAL
import components.threads.ValuationThread as VALUE

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self, parent)

        self.buildGui()
        self.show()
        self.activateWindow()
        self.loadSettingsFromFile()

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

    def buildGui(self):

        self.setWindowTitle(CONSTANTS.window.title)
        self.setIcon()

        splitter = QtGui.QSplitter(Qt.Qt.Horizontal)

        tabs_widget = self.buildTabs()
        controls_widget = self.buildControls()

        splitter.addWidget(controls_widget)
        splitter.addWidget(tabs_widget)

        self.setCentralWidget(splitter)
        
    def buildTabs(self):
        tabs = QtGui.QTabWidget()

        values_tab = QtGui.QWidget()
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

    def buildControls(self):

        splitter = QtGui.QSplitter(Qt.Qt.Vertical)
 
        self.option_style_widget = BUILD_CONTROLS.buildOptionStyleWidget()
        self.option_type_widget = BUILD_CONTROLS.buildOptionTypeWidget()
        self.output_type_widget = BUILD_CONTROLS.buildOutputTypeWidget()

        self.input_factors_widget = BUILD_CONTROLS.buildInputFactorsWidget()
        self.strike_dimensions_widget = BUILD_CONTROLS.buildStrikeDimensionsWidget()
        self.expiration_dimensions_widget = BUILD_CONTROLS.buildExpirationDimensionsWidget()

        actions_widget = BUILD_CONTROLS.buildActionsWidget()

        progress_bar_container_widget = self.buildProgressBar()

        self.option_style_widget.changedSignal.connect(self.onOptionStyleChange)
        self.option_type_widget.changedSignal.connect(self.onOptionTypeChange)
        self.output_type_widget.changedSignal.connect(self.onOutputTypeChange)

        self.input_factors_widget.changedSignal.connect(self.onInputFactorChange)
        self.strike_dimensions_widget.changedSignal.connect(self.onStrikeDimensionChange)
        self.expiration_dimensions_widget.changedSignal.connect(self.onExpirationDimensionChange)

        actions_widget.actionSignal.connect(self.handleAction)

        splitter.addWidget(self.option_style_widget)
        splitter.addWidget(self.option_type_widget)
        splitter.addWidget(self.input_factors_widget)
        splitter.addWidget(self.strike_dimensions_widget)
        splitter.addWidget(self.expiration_dimensions_widget)
        splitter.addWidget(self.output_type_widget)
        splitter.addWidget(actions_widget)
        splitter.addWidget(progress_bar_container_widget)

        return splitter

    def buildProgressBar(self):

        progress_bar_container_widget = QtGui.QWidget()

        layout = QtGui.QHBoxLayout()
        progress_bar_container_widget.setLayout(layout)

        self.progress_bar = PROGRESS_BAR.IncrementalProgressBar()
        self.progress_bar.setTextVisible(False)

        layout.addWidget(self.progress_bar)
    
        return progress_bar_container_widget 

    def onOptionStyleChange(self, selected_option):
        GLOBALS.valuation_controller.setOptionStyle(selected_option)
        self.updateOptionStyleValidity()
    def onOptionTypeChange(self, selected_option):
        GLOBALS.valuation_controller.setOptionType(selected_option)
        self.updateOptionTypeValidity()
    def onOutputTypeChange(self, selected_option):
        GLOBALS.valuation_controller.setOutputType(selected_option)
        self.updateOutputTypeValidity()
        
    def updateOptionStyleValidity(self):
        self.option_style_widget.setValidity(bool(GLOBALS.valuation_controller.getOptionStyle()))
    def updateOptionTypeValidity(self):
        self.option_type_widget.setValidity(bool(GLOBALS.valuation_controller.getOptionType()))
    def updateOutputTypeValidity(self):
        self.output_type_widget.setValidity(bool(GLOBALS.valuation_controller.getOutputType()))

    def onInputFactorChange(self, input_factors_dict):
        GLOBALS.valuation_controller.setInputFactors(input_factors_dict)
        self.updateInputFactorValidity()
    def onStrikeDimensionChange(self, strike_dimensions_dict):
        GLOBALS.valuation_controller.setStrikeRange(strike_dimensions_dict)
        self.updateStrikeDimensionsValidity()
    def onExpirationDimensionChange(self, expiration_dimensions_dict):
        GLOBALS.valuation_controller.setExpirationRange(expiration_dimensions_dict)
        self.updateExpirationDimensionsValidity()

    def updateInputFactorValidity(self):
        if GLOBALS.valuation_controller.getInputFactors():
            self.input_factors_widget.setValidity(True)
        else:
            self.input_factors_widget.setValidity(False)
    def updateStrikeDimensionsValidity(self):
        if GLOBALS.valuation_controller.getStrikeRange():
            self.strike_dimensions_widget.setValidity(True)
            self.values_table.updateStrikeColumns(GLOBALS.valuation_controller.getStrikeList())
        else:
            self.strike_dimensions_widget.setValidity(False)
            self.values_table.clearStrikeColumns()

    def updateExpirationDimensionsValidity(self):
        if GLOBALS.valuation_controller.getExpirationRange():
            self.expiration_dimensions_widget.setValidity(True)
            self.values_table.updateExpirationRows(GLOBALS.valuation_controller.getExpirationList())
        else:
            self.expiration_dimensions_widget.setValidity(False)
            self.values_table.clearExpirationRows()

    def updateAllValidity(self):
        self.updateOptionStyleValidity()
        self.updateOptionTypeValidity()
        self.updateOutputTypeValidity()
        self.updateInputFactorValidity()
        self.updateStrikeDimensionsValidity()
        self.updateExpirationDimensionsValidity()

    def handleAction(self, action):
        if (action == CONSTANTS.window.action.clear_):
            self.clear()
        elif (action == CONSTANTS.window.action.calculate):
            self.priceIfReady()
        elif (action == CONSTANTS.window.action.load):
            self.loadSettingsFromFile()
        elif (action == CONSTANTS.window.action.save):
            self.saveSettingsToFile()
    def clear(self):

        self.option_style_widget.clearSelection()
        self.option_type_widget.clearSelection()
        self.output_type_widget.clearSelection()

        self.input_factors_widget.clearForm()
        self.strike_dimensions_widget.clearForm()
        self.expiration_dimensions_widget.clearForm()

        self.values_table.clearContents()
        self.progress_bar.reset()

        GLOBALS.valuation_controller.reset()
        self.updateAllValidity()

    def loadSettingsFromFile(self):
        self.load_thread = SERIAL.LoadYAMLThread()
        self.load_thread.resultsSignal.connect(self.processSettings)
        self.load_thread.start()
    def saveSettingsToFile(self):
        if GLOBALS.valuation_controller.readyToValue():
            self.save_thread = SERIAL.SaveYAMLThread()
            GLOBALS.copyStateIntoSettings()
            self.save_thread.start()
    def processSettings(self, settingsMBD):

        GLOBALS.settings = settingsMBD

        GLOBALS.valuation_controller.loadFromSettings()

        self.input_factors_widget.loadValues(
            (
                (CONSTANTS.window.valuation.factor.spot_price,      CONSTANTS.backend.serialization.path.setting.spot_price),
                (CONSTANTS.window.valuation.factor.interest_rate,   CONSTANTS.backend.serialization.path.setting.interest_rate),
                (CONSTANTS.window.valuation.factor.carry_rate,      CONSTANTS.backend.serialization.path.setting.carry_rate),
                (CONSTANTS.window.valuation.factor.volatility,      CONSTANTS.backend.serialization.path.setting.volatility),
            )
        )

        self.option_style_widget.loadSelectedOption(CONSTANTS.backend.serialization.path.setting.style)
        self.option_type_widget.loadSelectedOption(CONSTANTS.backend.serialization.path.setting.type)
        self.output_type_widget.loadSelectedOption(CONSTANTS.backend.serialization.path.setting.output)

        self.strike_dimensions_widget.loadValues(
            (
                (CONSTANTS.window.valuation.dimension.strike_min,   CONSTANTS.backend.serialization.path.setting.strike_min),
                (CONSTANTS.window.valuation.dimension.strike_incr,  CONSTANTS.backend.serialization.path.setting.strike_incr),
                (CONSTANTS.window.valuation.dimension.strike_max,   CONSTANTS.backend.serialization.path.setting.strike_max)
            )
        )
        self.expiration_dimensions_widget.loadValues(
            (
                (CONSTANTS.window.valuation.dimension.expiration_min,   CONSTANTS.backend.serialization.path.setting.expiration_min),
                (CONSTANTS.window.valuation.dimension.expiration_incr,  CONSTANTS.backend.serialization.path.setting.expiration_incr),
                (CONSTANTS.window.valuation.dimension.expiration_max,   CONSTANTS.backend.serialization.path.setting.expiration_max)
            )
        )



    def priceIfReady(self):
        if GLOBALS.valuation_controller.readyToValue():

            self.prepareProgressBar()
            self.price_thread = self.prepareValuationThread()
            
            
            self.price_thread.resultSignal.connect(self.values_table.updateValue)
            self.price_thread.resultSignal.connect(self.progress_bar.increment)

            self.price_thread.start()
    def prepareProgressBar(self):
        self.progress_bar.resetToIncrement()
        self.progress_bar.setMaximumIncrements(GLOBALS.valuation_controller.getNumberOfCalculations())
    def prepareValuationThread(self):
        price_thread = VALUE.ValuationThread()

        price_thread.setOptionStyle(GLOBALS.valuation_controller.getOptionStyle())
        price_thread.setOptionType(GLOBALS.valuation_controller.getOptionType())
        price_thread.setOutputType(GLOBALS.valuation_controller.getOutputType())

        price_thread.setFactors(*GLOBALS.valuation_controller.getInputFactors())

        price_thread.setStrikesList(GLOBALS.valuation_controller.getStrikeList())
        price_thread.setExpirationsList(GLOBALS.valuation_controller.getExpirationList())

        return price_thread

def main():
    app = QtGui.QApplication(argv)  
    main = MainWindow()
    exit(app.exec_())

if __name__ == "__main__":
    main()

