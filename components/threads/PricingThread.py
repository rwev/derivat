
import PyQt4.QtCore as Qt
from ..libs import BAW
from ..libs.Constants import constants as CONSTANTS

class PricingThread(Qt.QThread):
    resultSignal = Qt.pyqtSignal(object)
    def __init__(self, parent = None):
        Qt.QThread.__init__(self, parent)

        self.spot_price = None
        self.interest_rate_ppa = None
        self.carry_rate_ppa = None
        self.volatility_ppa = None
        self.option_type = None

        self.strikes_list = None
        self.expirations_list = None

    def setFactors(self, spot_price, interest_rate_ppa, carry_rate_ppa, volatility_ppa, option_type):
        self.spot_price = spot_price
        self.interest_rate_ppa = interest_rate_ppa
        self.carry_rate_ppa = carry_rate_ppa
        self.volatility_ppa = volatility_ppa
        self.option_type = option_type
    def setStrikesList(self, strikes_list):
        self.strikes_list = strikes_list
    def setExpirationsList(self, expirations_list):
        self.expirations_list = expirations_list 

    def run(self): 
        for strike in self.strikes_list:
            for expiration in self.expirations_list:
                
                # determine whether to price call or put based on OTM.
                if self.spot_price < strike:
                    call_put_flag = CONSTANTS.backend.pricing.flags.call
                else:
                    call_put_flag = CONSTANTS.backend.pricing.flags.put

                price = BAW.getValue(self.option_type, CONSTANTS.backend.pricing.flags.value, call_put_flag, self.spot_price, strike, expiration / 365.0, self.interest_rate_ppa / 100.0, self.carry_rate_ppa / 100.0, self.volatility_ppa / 100.0 )
                self.resultSignal.emit((strike, expiration, price))
