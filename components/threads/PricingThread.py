
import PyQt4.QtCore as Qt
from ..libs import BAW
from ..libs.Constants import constants as CONSTANTS

class PricingThread(Qt.QThread):
    resultSignal = Qt.pyqtSignal(object)
    def __init__(self, parent = None):
        Qt.QThread.__init__(self, parent)

        self.option_style = None
        self.option_type = None
        self.output_type = None

        self.spot_price = None
        self.interest_rate_ppa = None
        self.carry_rate_ppa = None
        self.volatility_ppa = None

        self.strikes_list = None
        self.expirations_list = None

    def setOptionStyle(self, o):
        self.option_style = o
    def setOptionType(self, o):
        self.option_type = o
    def setOutputType(self, o):
        self.output_type = o

    def setFactors(self, spot_price, interest_rate_ppa, carry_rate_ppa, volatility_ppa):
        self.spot_price = spot_price
        self.interest_rate_ppa = interest_rate_ppa
        self.carry_rate_ppa = carry_rate_ppa
        self.volatility_ppa = volatility_ppa

    def setStrikesList(self, strikes_list):
        self.strikes_list = strikes_list
    def setExpirationsList(self, expirations_list):
        self.expirations_list = expirations_list 

    def run(self): 
        for strike_index in range(len(self.strikes_list)):
            for expiration_index in range(len(self.expirations_list)):
                
                strike = self.strikes_list[strike_index]
                expiration = self.expirations_list[expiration_index]

                if self.option_type == CONSTANTS.window.pricing.type.otm:
                    if self.spot_price < strike:
                        call_put_flag = CONSTANTS.backend.pricing.flags.type.call
                    else:
                        call_put_flag = CONSTANTS.backend.pricing.flags.type.put
                elif self.option_type == CONSTANTS.window.pricing.type.itm:
                    if self.spot_price > strike:
                        call_put_flag = CONSTANTS.backend.pricing.flags.type.call
                    else:
                        call_put_flag = CONSTANTS.backend.pricing.flags.type.put
                else:
                    call_put_flag = self.option_type

                value = BAW.getValue(self.option_style, self.output_type, call_put_flag, self.spot_price, strike, expiration / 365.0, self.interest_rate_ppa / 100.0, self.carry_rate_ppa / 100.0, self.volatility_ppa / 100.0 )
                
                self.resultSignal.emit((strike_index, expiration_index, value))
