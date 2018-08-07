'''
Defines the ValuationController class, 
which accepts dictionaries of various input components (i.e. factors, dimensions),
processes them (e.g. unpacks / expands)
stores them, 
and offers a validity check on them,
and returns them
'''

import numpy as np

from ..libs.Constants import constants as CONSTANTS

import Globals as GLOBALS

class ValuationController():
    def __init__(self):

        self.option_style = None
        self.option_type = None
        self.output_type = None

        self.factors_dict = None
        self.strike_dimensions_dict = None
        self.expiration_dimensions_dict = None

    def setOptionStyle(self, o):
        if o == CONSTANTS.window.valuation.style.american or \
            o == CONSTANTS.window.valuation.style.european:
            self.option_style = o
    def setOptionType(self, o):
        if o == CONSTANTS.window.valuation.type.call or \
            o == CONSTANTS.window.valuation.type.put or \
            o == CONSTANTS.window.valuation.type.otm or \
            o == CONSTANTS.window.valuation.type.itm:
            self.option_type = o
    def setOutputType(self, o):
        if o == CONSTANTS.window.valuation.output.value or \
            o == CONSTANTS.window.valuation.output.delta or \
            o == CONSTANTS.window.valuation.output.gamma or \
            o == CONSTANTS.window.valuation.output.vega or \
            o == CONSTANTS.window.valuation.output.theta:
           self.output_type = o

    def setFactorsDict(self, d):
        self.factors_dict = d
    def setStrikesDict(self, d):
        self.strike_dimensions_dict = d
    def setExpirationsDict(self, d):
        self.expiration_dimensions_dict = d  

    def getFactorInputs(self):
        return self.factors_dict[CONSTANTS.window.valuation.factor.spot_price], \
                self.factors_dict[CONSTANTS.window.valuation.factor.interest_rate], \
                self.factors_dict[CONSTANTS.window.valuation.factor.carry_rate], \
                self.factors_dict[CONSTANTS.window.valuation.factor.volatility]
    def areFactorsValid(self):
        if not self.factors_dict:
            return False
        
        spot_price, interest_rate_ppa, carry_rate_ppa, volatility_ppa = self.getFactorInputs()
        
        if not (spot_price > 0):
            return False
        if not (interest_rate_ppa > 0):
            return False
        if not (carry_rate_ppa > 0):
            return False
        if not (volatility_ppa > 0):
            return False
        return True
    def getFactors(self):
        if not self.areFactorsValid():
            return False
        return self.getFactorInputs()

    def checkRange(self, min, incr, max):
        return (min > 0 and incr > 0 and max > 0 and min < max and min + incr < max)

    def getOptionStyle(self):
        if self.option_style:
            return self.option_style
        return False
    def getOptionType(self):
        if self.option_type:
            return self.option_type
        return False
    def getOutputType(self):
        if self.output_type:
            return self.output_type
        return False
    
    def getStrikeRangeInputs(self):
        return self.strike_dimensions_dict[CONSTANTS.window.valuation.dimension.strike_min], \
                self.strike_dimensions_dict[CONSTANTS.window.valuation.dimension.strike_incr], \
                self.strike_dimensions_dict[CONSTANTS.window.valuation.dimension.strike_max]
    def areStrikesValid(self):
        if not self.strike_dimensions_dict:
            return False
        min, incr, max = self.getStrikeRangeInputs() 
        if self.checkRange(min, incr, max):
            return True
        return False
    def getStrikesList(self):
        if not self.areStrikesValid():
            return False
        min, incr, max = self.getStrikeRangeInputs() 
        strikes_list = list(np.arange(min, max + incr, incr))
        return strikes_list
    
    def getExpirationRangeInputs(self):
        return self.expiration_dimensions_dict[CONSTANTS.window.valuation.dimension.expiration_min], \
                self.expiration_dimensions_dict[CONSTANTS.window.valuation.dimension.expiration_incr], \
                self.expiration_dimensions_dict[CONSTANTS.window.valuation.dimension.expiration_max]
    def areExpirationsValid(self):
        if not self.expiration_dimensions_dict:
            return False
        min, incr, max = self.getExpirationRangeInputs() 
        if self.checkRange(min, incr, max):
            return True
        return False
    def getExpirationsList(self):
        if not self.areExpirationsValid():
            return False
        min, incr, max = self.getExpirationRangeInputs() 
        expirations_list = list(np.arange(min, max + incr, incr))
        return expirations_list

    def getNumberOfCalculations(self):
        return len(self.getExpirationsList()) * len(self.getStrikesList())

    def readyToValue(self):
        radio_options_ready = (self.getOptionStyle() and self.getOptionType() and self.getOutputType())
        numeric_inputs_ready = (self.areFactorsValid() and self.areStrikesValid() and self.areExpirationsValid())
        return radio_options_ready and numeric_inputs_ready
    
    def getValueFromSettings(self, serialization_path):
        temp = GLOBALS.settings
        for attr in serialization_path.split('.'):
            temp = temp[attr]
        return temp

    def loadFromSettings(self):

        self.option_style = self.getValueFromSettings(CONSTANTS.backend.serialization.path.setting.style)
        self.option_type = self.getValueFromSettings(CONSTANTS.backend.serialization.path.setting.type)
        self.output_type = self.getValueFromSettings(CONSTANTS.backend.serialization.path.setting.output)
        
        self.factors_dict = {}
        self.factors_dict[CONSTANTS.window.valuation.factor.spot_price] =    self.getValueFromSettings(CONSTANTS.backend.serialization.path.setting.spot_price)
        self.factors_dict[CONSTANTS.window.valuation.factor.interest_rate] = self.getValueFromSettings(CONSTANTS.backend.serialization.path.setting.interest_rate)
        self.factors_dict[CONSTANTS.window.valuation.factor.carry_rate] =    self.getValueFromSettings(CONSTANTS.backend.serialization.path.setting.carry_rate)
        self.factors_dict[CONSTANTS.window.valuation.factor.volatility] =    self.getValueFromSettings(CONSTANTS.backend.serialization.path.setting.volatility)

        self.expiration_dimensions_dict = {}
        self.expiration_dimensions_dict[CONSTANTS.window.valuation.dimension.expiration_min] =  self.getValueFromSettings(CONSTANTS.backend.serialization.path.setting.expiration_min)
        self.expiration_dimensions_dict[CONSTANTS.window.valuation.dimension.expiration_incr] = self.getValueFromSettings(CONSTANTS.backend.serialization.path.setting.expiration_incr)
        self.expiration_dimensions_dict[CONSTANTS.window.valuation.dimension.expiration_max] =  self.getValueFromSettings(CONSTANTS.backend.serialization.path.setting.expiration_max)

        self.strike_dimensions_dict = {}
        self.strike_dimensions_dict[CONSTANTS.window.valuation.dimension.strike_min] =  self.getValueFromSettings(CONSTANTS.backend.serialization.path.setting.strike_min)
        self.strike_dimensions_dict[CONSTANTS.window.valuation.dimension.strike_incr] = self.getValueFromSettings(CONSTANTS.backend.serialization.path.setting.strike_incr)
        self.strike_dimensions_dict[CONSTANTS.window.valuation.dimension.strike_max] =  self.getValueFromSettings(CONSTANTS.backend.serialization.path.setting.strike_max)
