
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
constants.window.messages.exit.description = 'Close derivat? Any unsaved pricing configuration will be lost.'

constants.window.table.content.font.size = 8
constants.window.table.content.characters = 6

constants.window.actions = 'Actions'
constants.window.action.clear_ = 'Clear'
constants.window.action.calculate = 'Calculate'
constants.window.action.save = 'Save'
constants.window.action.load = 'Load'

constants.window.pricing.styles = 'Option Style'
constants.window.pricing.style.european = 'European'
constants.window.pricing.style.american = 'American'

constants.window.pricing.types = 'Option Type'
constants.window.pricing.type.call = 'Call'
constants.window.pricing.type.put = 'Put'
constants.window.pricing.type.otm = 'OTM'
constants.window.pricing.type.itm = 'ITM'

constants.window.pricing.outputs = 'Output'
constants.window.pricing.output.value = 'Value'
constants.window.pricing.output.delta = 'Delta'
constants.window.pricing.output.gamma = 'Gamma'
constants.window.pricing.output.vega = 'Vega'
constants.window.pricing.output.theta = 'Theta'

constants.window.pricing.factors = 'Factors'
constants.window.pricing.factor.spot_price = 'Spot'
constants.window.pricing.factor.interest_rate = 'Interest Rate (% p.a.)'
constants.window.pricing.factor.carry_rate = 'Carry (% p.a.)'
constants.window.pricing.factor.volatility = 'Volatility (% p.a.)'
constants.window.pricing.factor.option_type = 'Option Type'

constants.window.pricing.dimension.strikes = 'Strikes'
constants.window.pricing.dimension.strike_min = 'Min.'
constants.window.pricing.dimension.strike_incr = 'Incr.'
constants.window.pricing.dimension.strike_max = 'Max.' 
constants.window.pricing.dimension.expirations = 'Expirations (days)'
constants.window.pricing.dimension.expiration_min = 'Min.'
constants.window.pricing.dimension.expiration_incr = 'Incr.'
constants.window.pricing.dimension.expiration_max = 'Max.'

constants.backend.pricing.flags.style.american = 'American'
constants.backend.pricing.flags.style.european = 'European'
constants.backend.pricing.flags.type.call = 'Call'
constants.backend.pricing.flags.type.put = 'Put'
constants.backend.pricing.flags.value = 'Value'
constants.backend.pricing.flags.delta = 'Delta'
constants.backend.pricing.flags.gamma = 'Gamma'
constants.backend.pricing.flags.vega = 'Vega'
constants.backend.pricing.flags.theta = 'Theta'

constants.backend.serialization.settings_path = 'components/serial/settings.yaml'