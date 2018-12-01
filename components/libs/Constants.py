
# -*- coding: utf-8 -*-
"""
Contains constants saved into an MBD instance for accessibility via members. 
"""

import BAW
from MBD import *

constants = MBD()

constants.sources.icon = 'assets/gamma.png'

constants.window.title = 'derivat'

constants.window.tabs.values_ = 'Values'
constants.window.tabs.graphs = 'Graphs'

constants.window.messages.exit.title = 'Confirm Exit'
constants.window.messages.exit.description = 'Close derivat? Any unsaved valuation configuration will be lost.'

constants.window.table.content.font.size = 8
constants.window.table.content.characters = 6

constants.window.actions = 'Actions'
constants.window.action.clear_ = 'Clear'
constants.window.action.calculate = 'Calculate'
constants.window.action.save = 'Save'
constants.window.action.load = 'Load'

constants.window.valuation.styles = 'Option Style'
constants.window.valuation.style.european = 'European'
constants.window.valuation.style.american = 'American'

constants.window.valuation.types = 'Option Type'
constants.window.valuation.type.call = 'Call'
constants.window.valuation.type.put = 'Put'
constants.window.valuation.type.otm = 'OTM'
constants.window.valuation.type.itm = 'ITM'

constants.window.valuation.outputs = 'Output'
constants.window.valuation.output.price = 'Price'
constants.window.valuation.output.delta = 'Delta'
constants.window.valuation.output.gamma = 'Gamma'
constants.window.valuation.output.vega = 'Vega'
constants.window.valuation.output.theta = 'Theta'

constants.window.valuation.factors = 'Input Factors'
constants.window.valuation.factor.spot_price = 'Spot'
constants.window.valuation.factor.interest_rate = 'Interest Rate (% p.a.)'
constants.window.valuation.factor.carry_rate = 'Carry (% p.a.)'
constants.window.valuation.factor.volatility = 'Volatility (% p.a.)'
constants.window.valuation.factor.option_type = 'Option Type'

constants.window.valuation.dimension.strikes = 'Strike Price'
constants.window.valuation.dimension.strike_min = 'Minimum'
constants.window.valuation.dimension.strike_incr = 'Increment'
constants.window.valuation.dimension.strike_max = 'Maximum' 
constants.window.valuation.dimension.expirations = 'Time until Expiration (Years)'
constants.window.valuation.dimension.expiration_min = 'Minimum'
constants.window.valuation.dimension.expiration_incr = 'Increment'
constants.window.valuation.dimension.expiration_max = 'Maximum' 

constants.backend.serialization.path.file = 'components/serial/settings.yaml'

constants.backend.serialization.path.setting.style = 'valuation.style'
constants.backend.serialization.path.setting.type = 'valuation.type'
constants.backend.serialization.path.setting.output = 'valuation.output'

constants.backend.serialization.path.setting.spot_price = 'valuation.factors.spot_price'
constants.backend.serialization.path.setting.interest_rate = 'valuation.factors.interest_rate'
constants.backend.serialization.path.setting.carry_rate = 'valuation.factors.carry_rate'
constants.backend.serialization.path.setting.volatility = 'valuation.factors.volatility'

constants.backend.serialization.path.setting.strike_min = 'valuation.dimensions.strikes.min'
constants.backend.serialization.path.setting.strike_incr = 'valuation.dimensions.strikes.incr'
constants.backend.serialization.path.setting.strike_max = 'valuation.dimensions.strikes.max'

constants.backend.serialization.path.setting.expiration_min = 'valuation.dimensions.expirations.min'
constants.backend.serialization.path.setting.expiration_incr = 'valuation.dimensions.expirations.incr'
constants.backend.serialization.path.setting.expiration_max = 'valuation.dimensions.expirations.max'

constants.backend.valuation.flags_map = {

    constants.window.valuation.style.european: BAW.EUROPEAN,
    constants.window.valuation.style.american: BAW.AMERICAN,

    constants.window.valuation.type.call: BAW.CALL,
    constants.window.valuation.type.put: BAW.PUT,

    constants.window.valuation.output.price: BAW.PRICE,
    constants.window.valuation.output.delta: BAW.DELTA,
    constants.window.valuation.output.gamma: BAW.GAMMA,
    constants.window.valuation.output.vega: BAW.VEGA,
    constants.window.valuation.output.theta: BAW.THETA
    
}