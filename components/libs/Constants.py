
# -*- coding: utf-8 -*-
"""
Contains constants saved into an MBD instance for accessibility via members. 
"""

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
constants.window.valuation.output.value = 'Value'
constants.window.valuation.output.delta = 'Delta'
constants.window.valuation.output.gamma = 'Gamma'
constants.window.valuation.output.vega = 'Vega'
constants.window.valuation.output.theta = 'Theta'

constants.window.valuation.factors = 'Factors'
constants.window.valuation.factor.spot_price = 'Spot'
constants.window.valuation.factor.interest_rate = 'Interest Rate (% p.a.)'
constants.window.valuation.factor.carry_rate = 'Carry (% p.a.)'
constants.window.valuation.factor.volatility = 'Volatility (% p.a.)'
constants.window.valuation.factor.option_type = 'Option Type'

constants.window.valuation.dimension.strikes = 'Strikes'
constants.window.valuation.dimension.strike_min = 'Min.'
constants.window.valuation.dimension.strike_incr = 'Incr.'
constants.window.valuation.dimension.strike_max = 'Max.' 
constants.window.valuation.dimension.expirations = 'Expirations (days)'
constants.window.valuation.dimension.expiration_min = 'Min.'
constants.window.valuation.dimension.expiration_incr = 'Incr.'
constants.window.valuation.dimension.expiration_max = 'Max.'

constants.backend.valuation.flags.style.american = 'American'
constants.backend.valuation.flags.style.european = 'European'
constants.backend.valuation.flags.type.call = 'Call'
constants.backend.valuation.flags.type.put = 'Put'
constants.backend.valuation.flags.value = 'Value'
constants.backend.valuation.flags.delta = 'Delta'
constants.backend.valuation.flags.gamma = 'Gamma'
constants.backend.valuation.flags.vega = 'Vega'
constants.backend.valuation.flags.theta = 'Theta'

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
