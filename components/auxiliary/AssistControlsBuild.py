import PyQt4.QtCore as Qt
import PyQt4.QtGui as QtGui

import components.auxiliary.NumericInputGroupBox as NUMERIC_INPUT_GROUP_BOX
import components.auxiliary.RadioButtonGroupBox as RADIO_BUTTON_GROUP_BOX
import components.auxiliary.PushButtonGroupBox as PUSH_BUTTON_GROUP_BOX

from components.libs.Constants import constants as CONSTANTS


def buildInputFactorsWidget():
    input_factors_widget = NUMERIC_INPUT_GROUP_BOX.NumericInputWidget(
        group_name=CONSTANTS.window.valuation.factors
    )
    input_factors_widget.displayParameters(
        param_name_type_default_tuples=(
            (CONSTANTS.window.valuation.factor.spot_price, float, None),
            (CONSTANTS.window.valuation.factor.interest_rate, float, None),
            (CONSTANTS.window.valuation.factor.carry_rate, float, None),
            (CONSTANTS.window.valuation.factor.volatility, float, None),
        )
    )
    return input_factors_widget


def buildStrikeDimensionsWidget():
    strikes_widget = NUMERIC_INPUT_GROUP_BOX.NumericInputWidget(
        group_name=CONSTANTS.window.valuation.dimension.strikes
    )
    strikes_widget.displayParameters(
        param_name_type_default_tuples=(
            (CONSTANTS.window.valuation.dimension.strike_min, float, None),
            (CONSTANTS.window.valuation.dimension.strike_incr, float, None),
            (CONSTANTS.window.valuation.dimension.strike_max, float, None),
        )
    )
    return strikes_widget


def buildExpirationDimensionsWidget():
    expirations_widget = NUMERIC_INPUT_GROUP_BOX.NumericInputWidget(
        group_name=CONSTANTS.window.valuation.dimension.expirations
    )
    expirations_widget.displayParameters(
        param_name_type_default_tuples=(
            (CONSTANTS.window.valuation.dimension.expiration_min, float, None),
            (CONSTANTS.window.valuation.dimension.expiration_incr, float, None),
            (CONSTANTS.window.valuation.dimension.expiration_max, float, None),
        )
    )
    return expirations_widget


def buildOptionStyleWidget():

    option_style_widget = RADIO_BUTTON_GROUP_BOX.RadioButtonGroupBox(
        CONSTANTS.window.valuation.styles
    )

    option_style_widget.addOptions(
        (
            CONSTANTS.window.valuation.style.american,
            CONSTANTS.window.valuation.style.european,
        )
    )

    return option_style_widget


def buildOptionTypeWidget():

    option_type_widget = RADIO_BUTTON_GROUP_BOX.RadioButtonGroupBox(
        CONSTANTS.window.valuation.types
    )

    option_type_widget.addOptions(
        (
            CONSTANTS.window.valuation.type.call,
            CONSTANTS.window.valuation.type.put,
            CONSTANTS.window.valuation.type.otm,
            CONSTANTS.window.valuation.type.itm,
        )
    )

    return option_type_widget


def buildOutputTypeWidget():

    output_type_widget = RADIO_BUTTON_GROUP_BOX.RadioButtonGroupBox(
        CONSTANTS.window.valuation.outputs
    )

    output_type_widget.addOptions(
        (
            CONSTANTS.window.valuation.output.price,
            CONSTANTS.window.valuation.output.delta,
            CONSTANTS.window.valuation.output.gamma,
            CONSTANTS.window.valuation.output.vega,
            CONSTANTS.window.valuation.output.theta,
        )
    )

    return output_type_widget


def buildActionsWidget():

    actions_widget = PUSH_BUTTON_GROUP_BOX.PushButtonGroupBox(
        2, 2, CONSTANTS.window.actions
    )

    actions_widget.addActions(
        (
            CONSTANTS.window.action.clear_,
            CONSTANTS.window.action.calculate,
            CONSTANTS.window.action.save,
            CONSTANTS.window.action.load,
        )
    )

    return actions_widget
