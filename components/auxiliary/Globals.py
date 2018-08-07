'''
holds variables to be shared between files, 
so that they must not be reinitialized / reloaded in each file,
nor passed as arguments. 
'''

import components.auxiliary.ValuationController as VALUE_CONTROL

global valuation_controller
global settings

valuation_controller = VALUE_CONTROL.ValuationController()

