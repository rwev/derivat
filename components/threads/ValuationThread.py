import PyQt4.QtCore as Qt
from ..libs import BAW
from ..libs import CYBAW
from ..libs.Constants import constants as CONSTANTS


class ValuationThread(Qt.QThread):
    intermediateResultSignal = Qt.pyqtSignal(object)
    finishedSignal = Qt.pyqtSignal(object)

    def __init__(self, parent=None):
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

    def setStrikeList(self, strikes_list):
        self.strikes_list = strikes_list

    def setExpirationList(self, expirations_list):
        self.expirations_list = expirations_list

    def run(self):
        min_value = float("inf")
        max_value = -float("inf")

        for strike_index in range(len(self.strikes_list)):
            for expiration_index in range(len(self.expirations_list)):

                strike = self.strikes_list[strike_index]
                expiration = self.expirations_list[expiration_index]

                if self.option_type == CONSTANTS.window.valuation.type.otm:
                    if self.spot_price < strike:
                        call_put_flag = CONSTANTS.window.valuation.type.call
                    else:
                        call_put_flag = CONSTANTS.window.valuation.type.put
                elif self.option_type == CONSTANTS.window.valuation.type.itm:
                    if self.spot_price > strike:
                        call_put_flag = CONSTANTS.window.valuation.type.call
                    else:
                        call_put_flag = CONSTANTS.window.valuation.type.put
                else:
                    call_put_flag = self.option_type

                value = CYBAW.getValue(
                    CONSTANTS.backend.valuation.flags_map[self.option_style],
                    CONSTANTS.backend.valuation.flags_map[self.output_type],
                    CONSTANTS.backend.valuation.flags_map[call_put_flag],
                    self.spot_price,
                    strike,
                    expiration,
                    self.interest_rate_ppa / 100.0,
                    self.carry_rate_ppa / 100.0,
                    self.volatility_ppa / 100.0,
                )

                min_value = min(min_value, value)
                max_value = max(max_value, value)

                self.intermediateResultSignal.emit(
                    (strike_index, expiration_index, value)
                )
        self.finishedSignal.emit((min_value, max_value))
