try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import pyximport; pyximport.install()
import BAW, CYBAW

from time import time
from collections import namedtuple
from random import choice, uniform
from pprint import pprint

NUM_OPTIONS_TO_VALUE =  100

def test():

    bounds =            namedtuple('bounds', ['min', 'max'])
    pricing_inputs =    namedtuple('pricing_inputs', ['output_type', 'option_type','spot', 'strike', 'years', 'interest', 'carry', 'volatility'])

    
    output_option_type_choice = (31, 32, 33, 34, 35)
    option_type_choice =        (21, 22)
    spot_bounds =       bounds(min = 95,    max = 105)
    strike_bounds =     bounds(min = 90,    max = 110)
    year_bounds =       bounds(min = 0.5,   max = 4.0)
    interest_bounds =   bounds(min = 0.001, max = 0.025)
    carry_bounds =      bounds(min = 0.001, max = 0.025)
    volatility_bounds = bounds(min = 0.05,  max = 0.5)

    to_price = []
    for i in range(NUM_OPTIONS_TO_VALUE):

        t_output_type = choice(output_option_type_choice)
        t_option_type = choice(option_type_choice)
        t_spot =        uniform(spot_bounds.min,        spot_bounds.max)
        t_strike =      uniform(strike_bounds.min,      strike_bounds.max)
        t_years =       uniform(year_bounds.min,        year_bounds.max)
        t_interest =    uniform(interest_bounds.min,    interest_bounds.max)
        t_carry =       uniform(carry_bounds.min,       carry_bounds.max)
        t_volatility =  uniform(volatility_bounds.min,  volatility_bounds.max)

        t_inputs = pricing_inputs(  
            output_type = t_output_type, 
            option_type = t_option_type, 
            spot = t_spot, 
            strike = t_strike, 
            years = t_years, 
            interest = t_interest, 
            carry = t_carry, 
            volatility = t_volatility
        )
        to_price.append(t_inputs)


    t = time()
    for pinp in to_price:
        BAW.getValue(
            11,
            pinp.output_type, 
            pinp.option_type, 
            pinp.spot, 
            pinp.strike, 
            pinp.years, 
            pinp.interest, 
            pinp.carry, 
            pinp.volatility
        )
    pure_py_ms = 1000* (time() - t)
    print "\nPYTHON BAW = %0.0f ms" % (pure_py_ms,)

    t = time()
    for pinp in to_price:
        CYBAW.getValue( 
            11,
            pinp.output_type, 
            pinp.option_type, 
            pinp.spot, 
            pinp.strike, 
            pinp.years, 
            pinp.interest, 
            pinp.carry, 
            pinp.volatility
        )
    cython_ms = 1000* (time() - t)
    print "\nCYTHON CYBAW = %0.0f ms" % (cython_ms,)

    print "\nSPEEDUP = %0.2f\n" % (pure_py_ms / cython_ms)

if __name__ == '__main__':
    test()