'''
Defines the PricingController class, 
which accepts dictionaries of various input components (i.e. factors, dimensions),
processes them (e.g. unpacks / expands)
stores them, 
and offers a validity check on them,
and returns them
'''

import numpy as np

from ..libs.Constants import derivat_constants as CONSTANTS

def checkRange(start, step, stop):
    return (start > 0 and step > 0 and stop > 0 and start < stop and start + step < stop)
def getStrikeRangeInputs(strike_dimensions_dict):
    return strike_dimensions_dict[CONSTANTS.window.pricing.input_dimensions.strike_start], strike_dimensions_dict[CONSTANTS.window.pricing.input_dimensions.strike_step], strike_dimensions_dict[CONSTANTS.window.pricing.input_dimensions.strike_stop]
def getExpirationRangeInputs(expiration_dimensions_dict):
    return expiration_dimensions_dict[CONSTANTS.window.pricing.input_dimensions.strike_start], expiration_dimensions_dict[CONSTANTS.window.pricing.input_dimensions.strike_step], expiration_dimensions_dict[CONSTANTS.window.pricing.input_dimensions.strike_stop]

class PricingController():
    def __init__(self):
        self.factors_dict = None
        self.strike_dimensions_dict = None
        self.expiration_dimensions_dict = None

    def setFactorsDict(self, d):
        self.factors_dict = d
    def setStrikesDict(self, d):
        self.strike_dimensions_dict = d
    def setExpirationsDict(self, d):
        self.expiration_dimensions_dict = d  

    def areFactorsValid(self):
        if not self.factors_dict:
            return False
        
        spot_price = self.factors_dict[CONSTANTS.window.pricing.input_factors.spot_price]
        if not (spot_price > 0):
            return False

        interest_rate = self.factors_dict[CONSTANTS.window.pricing.input_factors.interest_rate]
        if not (interest_rate > 0):
            return False

        carry_rate = self.factors_dict[CONSTANTS.window.pricing.input_factors.carry_rate]
        if not (carry_rate > 0):
            return False
        
        volatility = self.factors_dict[CONSTANTS.window.pricing.input_factors.volatility]
        if not (volatility > 0):
            return False

        option_type = self.factors_dict[CONSTANTS.window.pricing.input_factors.option_type]
        if not ((option_type == CONSTANTS.window.pricing.types.european) or (option_type == CONSTANTS.window.pricing.types.american)):
            return False
        return True

    def areStrikesValid(self):
        if not self.strike_dimensions_dict:
            return False
        start, step, stop = getStrikeRangeInputs(self.strike_dimensions_dict) 
        if checkRange(start, step, stop):
            return True
        return False
    def getStrikesList(self):
        if not self.areStrikesValid():
            return False
        start, step, stop = getStrikeRangeInputs(self.strike_dimensions_dict) 
        strikes_list = list(np.arange(start, stop, step))
        return strikes_list

    def areExpirationsValid(self):
        if not self.expiration_dimensions_dict:
            return False
        start, step, stop = getExpirationRangeInputs(self.expiration_dimensions_dict) 
        if checkRange(start, step, stop):
            return True
        return False
    def getExpirationsList(self):
        if not self.areExpirationsValid():
            return False
        start, step, stop = getExpirationRangeInputs(self.expiration_dimensions_dict) 
        expirations_list = list(np.arange(start, stop, step))
        return expirations_list

    def readyToPrice(self):
        return self.areFactorsValid() and self.areStrikesValid() and self.areExpirationsValid() 
    
