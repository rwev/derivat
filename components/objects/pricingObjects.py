# -*- coding: utf-8 -*-
"""
Created on Sat Feb 10 21:02:07 2018

@author: Ryan
"""

from collections import namedtuple

pricing_inputs = namedtuple('PricingInputs',
                            ['spot_price_dollars',
                             'interest_rate_pa',
                             'carry_rate_pa',
                             'volatility_pa'])

pricing_dimensions = namedtuple('PricingDimensions',
                            ['strikes_list_dollars',
                             'expirations_list_days'])

pricing_inputs_variable_to_display_map = {'spot_price_dollars':  'Spot',
     'interest_rate_pa':    'Interest Rate (% p.a.)',
     'carry_rate_pa':       'Carry (% p.a.)',
     'volatility_pa':       'Volatility (% p.a.)'}

pricing_dimensions_variable_to_display_map = {'strikes_list_dollars':  'Strikes',
     'expirations_list_days': 'Expirations (days)'}

def invertDict(adict):
    return {v: k for k, v in adict.iteritems()}

pricing_inputs_display_to_variable_map = invertDict(pricing_inputs_variable_to_display_map)
pricing_dimensions_display_to_variable_map = invertDict(pricing_dimensions_variable_to_display_map)

