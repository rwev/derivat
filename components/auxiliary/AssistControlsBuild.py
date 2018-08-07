
import PyQt4.QtCore as Qt
import PyQt4.QtGui as QtGui

import components.auxiliary.NumericInputGroupBox as NUMERIC_INPUT_GROUP_BOX
import components.auxiliary.RadioButtonGroupBox as RADIO_BUTTON_GROUP_BOX
import components.auxiliary.PushButtonGroupBox as PUSH_BUTTON_GROUP_BOX

from components.libs.Constants import constants as CONSTANTS

def buildInputFactorsWidget():        
    input_factors_widget = NUMERIC_INPUT_GROUP_BOX.NumericInputWidget(group_name = CONSTANTS.window.pricing.factors)
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
    strikes_widget = NUMERIC_INPUT_GROUP_BOX.NumericInputWidget(group_name = CONSTANTS.window.pricing.dimension.strikes)
    strikes_widget.displayParameters(param_name_type_default_tuples = 
            (
                (CONSTANTS.window.pricing.dimension.strike_min,  float, None),
                (CONSTANTS.window.pricing.dimension.strike_incr,   float, None),
                (CONSTANTS.window.pricing.dimension.strike_max,   float, None)
            )
        )
    return strikes_widget

def buildExpirationDimensionsWidget():
    expirations_widget = NUMERIC_INPUT_GROUP_BOX.NumericInputWidget(group_name = CONSTANTS.window.pricing.dimension.expirations)
    expirations_widget.displayParameters(param_name_type_default_tuples = 
            (
                (CONSTANTS.window.pricing.dimension.expiration_min, int, None),
                (CONSTANTS.window.pricing.dimension.expiration_incr,  int, None),
                (CONSTANTS.window.pricing.dimension.expiration_max,  int, None)
            )
        )
    return expirations_widget

def buildOptionStyleWidget(): 

    option_style_widget = RADIO_BUTTON_GROUP_BOX.RadioButtonGroupBox(CONSTANTS.window.pricing.styles)

    option_style_widget.addOptions(
        (
            CONSTANTS.window.pricing.style.american,
            CONSTANTS.window.pricing.style.european
        )
    )

    return option_style_widget

def buildOptionTypeWidget():

    option_type_widget = RADIO_BUTTON_GROUP_BOX.RadioButtonGroupBox(CONSTANTS.window.pricing.types)

    option_type_widget.addOptions(
        (
            CONSTANTS.window.pricing.type.call,
            CONSTANTS.window.pricing.type.put,
            CONSTANTS.window.pricing.type.otm,
            CONSTANTS.window.pricing.type.itm
        )
    )
 
    return option_type_widget

def buildOutputTypeWidget():

    output_type_widget = RADIO_BUTTON_GROUP_BOX.RadioButtonGroupBox(CONSTANTS.window.pricing.outputs)

    output_type_widget.addOptions(
        (
            CONSTANTS.window.pricing.output.value,
            CONSTANTS.window.pricing.output.delta,
            CONSTANTS.window.pricing.output.gamma,
            CONSTANTS.window.pricing.output.vega,
            CONSTANTS.window.pricing.output.theta
        )
    )
 
    return output_type_widget

def buildActionsWidget():

    actions_widget = PUSH_BUTTON_GROUP_BOX.PushButtonGroupBox(2, 2, CONSTANTS.window.actions)

    actions_widget.addActions(
        (
            CONSTANTS.window.action.clear_,
            CONSTANTS.window.action.calculate,
            CONSTANTS.window.action.save,
            CONSTANTS.window.action.load
        )
    )

    return actions_widget
