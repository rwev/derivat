
import PyQt4.QtCore as Qt
import PyQt4.QtGui as QtGui

import components.auxiliary.CustomInputs as CUSTOM
import components.auxiliary.LineEdit as LINE_EDIT
import components.auxiliary.PriceTable as PRICE_TABLE
import components.auxiliary.PricingController as PRICE_CONTROL

import components.libs.PyQtShared as PYQT_SHARED
from components.libs.Constants import derivat_constants as CONSTANTS

def buildInputFactorsWidget():        
    input_factors_widget = CUSTOM.ParameterSelectionWidget(group_name = CONSTANTS.window.pricing.inputs)
    input_factors_widget.displayParameters(param_name_type_default_tuples = 
        (
            (CONSTANTS.window.pricing.input_factors.spot_price,     float,  None),
            (CONSTANTS.window.pricing.input_factors.interest_rate,  float,  None),
            (CONSTANTS.window.pricing.input_factors.carry_rate,     float,  None),
            (CONSTANTS.window.pricing.input_factors.volatility,     float,  None),
            (CONSTANTS.window.pricing.input_factors.option_type,    tuple,  (
                                                    CONSTANTS.window.pricing.styles.american, 
                                                    CONSTANTS.window.pricing.styles.european
                                                    )
            )
        )
    )
    return input_factors_widget

def buildStrikeDimensionsWidget():
    strikes_widget = CUSTOM.ParameterSelectionWidget(group_name = CONSTANTS.window.pricing.input_dimensions.strikes)
    strikes_widget.displayParameters(param_name_type_default_tuples = 
            (
                (CONSTANTS.window.pricing.input_dimensions.strike_start,  float, None),
                (CONSTANTS.window.pricing.input_dimensions.strike_step,   float, None),
                (CONSTANTS.window.pricing.input_dimensions.strike_stop,   float, None)
            )
        )
    return strikes_widget

def buildExpirationDimensionsWidget():
    expirations_widget = CUSTOM.ParameterSelectionWidget(group_name = CONSTANTS.window.pricing.input_dimensions.expirations)
    expirations_widget.displayParameters(param_name_type_default_tuples = 
            (
                (CONSTANTS.window.pricing.input_dimensions.expiration_start, int, None),
                (CONSTANTS.window.pricing.input_dimensions.expiration_step,  int, None),
                (CONSTANTS.window.pricing.input_dimensions.expiration_stop,  int, None)
            )
        )
    return expirations_widget

def buildOptionStyleWidget():

    option_style_widget = QtGui.QWidget()
    option_style_layout = QtGui.QVBoxLayout()

    option_style_widget.setLayout(option_style_layout)

    option_style_group_box = QtGui.QGroupBox(CONSTANTS.window.pricing.style)
    option_style_group_box_content_layout = QtGui.QHBoxLayout()
    option_style_group_box.setLayout(option_style_group_box_content_layout)
    option_style_layout.addWidget(option_style_group_box)

    american_radio_button = QtGui.QRadioButton(CONSTANTS.window.pricing.styles.american)
    european_radio_button = QtGui.QRadioButton(CONSTANTS.window.pricing.styles.european)

    option_style_button_group = QtGui.QButtonGroup()
    option_style_button_group.addButton(american_radio_button)
    option_style_button_group.addButton(european_radio_button)

    option_style_group_box_content_layout.addWidget(american_radio_button)
    option_style_group_box_content_layout.addWidget(european_radio_button)
    
    return option_style_widget
