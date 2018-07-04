
# -*- coding: utf-8 -*-
"""
Contains constants saved into an MBD instance for accessibility via members. 
"""

from MBD import *

derivat_constants = MBD()

derivat_constants.sources.icon = 'assets/gamma.png'

derivat_constants.window.title = 'derivat'

derivat_constants.window.tabs.prices = 'Prices'
derivat_constants.window.tabs.graphs = 'Graphs'

derivat_constants.window.messages.exit.title = 'Confirm Exit'
derivat_constants.window.messages.exit.description = 'Close derivat? Any unsaved pricing configuration will be lost.'

derivat_constants.window.pricing.types.european = 'European'
derivat_constants.window.pricing.types.american = 'American'

derivat_constants.window.pricing.inputs = 'Pricing Inputs'
derivat_constants.window.pricing.input_factors.spot_price = 'Spot'
derivat_constants.window.pricing.input_factors.interest_rate = 'Interest Rate (% p.a.)'
derivat_constants.window.pricing.input_factors.carry_rate = 'Carry (% p.a.)'
derivat_constants.window.pricing.input_factors.volatility = 'Volatility (% p.a.)'
derivat_constants.window.pricing.input_factors.option_type = 'Option Type'

derivat_constants.window.pricing.dimensions = 'Pricing Dimensions'
derivat_constants.window.pricing.input_dimensions.strikes = 'Strikes'
derivat_constants.window.pricing.input_dimensions.expirations = 'Expirations'

derivat_constants.backend.pricing.flags.call = 'Call'
derivat_constants.backend.pricing.flags.put = 'Put'
derivat_constants.backend.pricing.flags.value = 'Value'
derivat_constants.backend.pricing.flags.delta = 'Delta'
derivat_constants.backend.pricing.flags.gamma = 'Gamma'
derivat_constants.backend.pricing.flags.vega = 'Vega'
derivat_constants.backend.pricing.flags.theta = 'Theta'
