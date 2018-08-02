
import PyQt4.QtCore as Qt
import PyQt4.QtGui as QtGui

import components.auxiliary.CustomInputs as CUSTOM
import components.auxiliary.LineEdit as LINE_EDIT
import components.auxiliary.PriceTable as PRICE_TABLE
import components.auxiliary.PricingController as PRICE_CONTROL

import components.libs.PyQtShared as PYQT_SHARED
from components.libs.Constants import constants as CONSTANTS

def buildInputFactorsWidget():        
    input_factors_widget = CUSTOM.ParameterSelectionWidget(group_name = CONSTANTS.window.pricing.factors)
    input_factors_widget.displayParameters(param_name_type_default_tuples = 
        (
            (CONSTANTS.window.pricing.factor.spot_price,     float,  None),
            (CONSTANTS.window.pricing.factor.interest_rate,  float,  None),
            (CONSTANTS.window.pricing.factor.carry_rate,     float,  None),
            (CONSTANTS.window.pricing.factor.volatility,     float,  None),
        )
    )
    return input_factors_widget

def buildStrikeDimensionsWidget():
    strikes_widget = CUSTOM.ParameterSelectionWidget(group_name = CONSTANTS.window.pricing.dimension.strikes)
    strikes_widget.displayParameters(param_name_type_default_tuples = 
            (
                (CONSTANTS.window.pricing.dimension.strike_start,  float, None),
                (CONSTANTS.window.pricing.dimension.strike_step,   float, None),
                (CONSTANTS.window.pricing.dimension.strike_stop,   float, None)
            )
        )
    return strikes_widget

def buildExpirationDimensionsWidget():
    expirations_widget = CUSTOM.ParameterSelectionWidget(group_name = CONSTANTS.window.pricing.dimension.expirations)
    expirations_widget.displayParameters(param_name_type_default_tuples = 
            (
                (CONSTANTS.window.pricing.dimension.expiration_start, int, None),
                (CONSTANTS.window.pricing.dimension.expiration_step,  int, None),
                (CONSTANTS.window.pricing.dimension.expiration_stop,  int, None)
            )
        )
    return expirations_widget

def buildOptionStyleWidget(): 

    option_style_widget = QtGui.QWidget()
    option_style_layout = QtGui.QVBoxLayout()

    option_style_widget.setLayout(option_style_layout)
 
    option_style_group_box = QtGui.QGroupBox(CONSTANTS.window.pricing.styles)
    option_style_group_box_content_layout = QtGui.QHBoxLayout()
    option_style_group_box.setLayout(option_style_group_box_content_layout)
    option_style_layout.addWidget(option_style_group_box)

    american_radio_button = QtGui.QRadioButton(CONSTANTS.window.pricing.style.american)
    european_radio_button = QtGui.QRadioButton(CONSTANTS.window.pricing.style.european)

    option_style_button_group = QtGui.QButtonGroup()
    option_style_button_group.addButton(american_radio_button)
    option_style_button_group.addButton(european_radio_button)

    option_style_group_box_content_layout.addWidget(american_radio_button)
    option_style_group_box_content_layout.addWidget(european_radio_button)

    return option_style_widget

def buildOptionTypeWidget():

    option_type_widget = QtGui.QWidget()
    option_type_layout = QtGui.QVBoxLayout()

    option_type_widget.setLayout(option_type_layout)
 
    option_type_group_box = QtGui.QGroupBox(CONSTANTS.window.pricing.types)
    option_type_group_box_content_layout = QtGui.QHBoxLayout()
    option_type_group_box.setLayout(option_type_group_box_content_layout)
    option_type_layout.addWidget(option_type_group_box)

    call_radio_button = QtGui.QRadioButton(CONSTANTS.window.pricing.type.call)
    put_radio_button = QtGui.QRadioButton(CONSTANTS.window.pricing.type.put)
    otm_radio_button = QtGui.QRadioButton(CONSTANTS.window.pricing.type.otm)
    itm_radio_button = QtGui.QRadioButton(CONSTANTS.window.pricing.type.itm)

    option_type_button_group = QtGui.QButtonGroup()
    option_type_button_group.addButton(call_radio_button)
    option_type_button_group.addButton(put_radio_button)
    option_type_button_group.addButton(otm_radio_button)
    option_type_button_group.addButton(itm_radio_button)

    option_type_group_box_content_layout.addWidget(call_radio_button)
    option_type_group_box_content_layout.addWidget(put_radio_button)
    option_type_group_box_content_layout.addWidget(otm_radio_button)
    option_type_group_box_content_layout.addWidget(itm_radio_button)
    
    return option_type_widget

def buildOutputTypeWidget():

    output_type_widget = QtGui.QWidget()
    output_type_layout = QtGui.QVBoxLayout()

    output_type_widget.setLayout(output_type_layout)
 
    output_type_group_box = QtGui.QGroupBox(CONSTANTS.window.pricing.outputs)
    output_type_group_box_content_layout = QtGui.QHBoxLayout()
    output_type_group_box.setLayout(output_type_group_box_content_layout)
    output_type_layout.addWidget(output_type_group_box)

    value_radio_button = QtGui.QRadioButton(CONSTANTS.window.pricing.output.value)
    delta_radio_button = QtGui.QRadioButton(CONSTANTS.window.pricing.output.delta)
    gamma_radio_button = QtGui.QRadioButton(CONSTANTS.window.pricing.output.gamma)
    vega_radio_button = QtGui.QRadioButton(CONSTANTS.window.pricing.output.vega)
    theta_radio_button = QtGui.QRadioButton(CONSTANTS.window.pricing.output.theta)

    output_type_button_group = QtGui.QButtonGroup()
    output_type_button_group.addButton(value_radio_button)
    output_type_button_group.addButton(delta_radio_button)
    output_type_button_group.addButton(gamma_radio_button)
    output_type_button_group.addButton(vega_radio_button)
    output_type_button_group.addButton(theta_radio_button)

    output_type_group_box_content_layout.addWidget(value_radio_button)
    output_type_group_box_content_layout.addWidget(delta_radio_button)
    output_type_group_box_content_layout.addWidget(gamma_radio_button)
    output_type_group_box_content_layout.addWidget(vega_radio_button)
    output_type_group_box_content_layout.addWidget(theta_radio_button)
        
    return output_type_widget
