"""
holds variables to be shared between files, 
so that they must not be reinitialized / reloaded in each file,
nor passed as arguments. 
"""

import components.auxiliary.ValuationController as VALUE_CONTROL

global valuation_controller
global settings

valuation_controller = VALUE_CONTROL.ValuationController()


def copyStateIntoSettings():

    settings.valuation.style = valuation_controller.getOptionStyle()
    settings.valuation.type = valuation_controller.getOptionType()
    settings.valuation.output = valuation_controller.getOutputType()

    s, i, c, v = valuation_controller.getInputFactors()
    settings.valuation.factors.spot_price = s
    settings.valuation.factors.interest_rate = i
    settings.valuation.factors.carry_rate = c
    settings.valuation.factors.volatility = v

    min, incr, max = valuation_controller.getStrikeRange()
    settings.valuation.dimensions.strikes.min = min
    settings.valuation.dimensions.strikes.incr = incr
    settings.valuation.dimensions.strikes.max = max

    min, incr, max = valuation_controller.getExpirationRange()
    settings.valuation.dimensions.expirations.min = min
    settings.valuation.dimensions.expirations.incr = incr
    settings.valuation.dimensions.expirations.max = max
