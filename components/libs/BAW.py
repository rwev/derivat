"""
Implements the Barone-Adesi And Whaley model for the pricing of American options. 
"""

import numpy as np
import cmath as m

from Constants import constants as CONSTANTS

dS = 0.001
dT = 1 / 365
dV = 0.00001

ITERATION_MAX_ERROR = 0.001

def standardNormalPDF(x): 
    val = (1 / (2 * m.pi)**0.5) * np.exp(-1 * (x**2) / 2)
    return val
def standardNormalCDF(X):     
    y = np.abs(X) 
    
    if y > 37: 
        return 0
    else:
        Exponential = np.exp(-1 * (y**2) / 2)
        
    if y < 7.07106781186547:
        SumA = 0.0352624965998911 * y + 0.700383064443688
        SumA = SumA * y + 6.37396220353165
        SumA = SumA * y + 33.912866078383
        SumA = SumA * y + 112.079291497871
        SumA = SumA * y + 221.213596169931
        SumA = SumA * y + 220.206867912376
        SumB = 0.0883883476483184 * y + 1.75566716318264
        SumB = SumB * y + 16.064177579207
        SumB = SumB * y + 86.7807322029461
        SumB = SumB * y + 296.564248779674
        SumB = SumB * y + 637.333633378831
        SumB = SumB * y + 793.826512519948
        SumB = SumB * y + 440.413735824752
        standardNormalCDF = Exponential * SumA / SumB
    else:
        SumA = y + 0.65
        SumA = y + 4 / SumA
        SumA = y + 3 / SumA
        SumA = y + 2 / SumA
        SumA = y + 1 / SumA
        standardNormalCDF = Exponential / (SumA * 2.506628274631)
    
    if X > 0:
         return 1 - standardNormalCDF
    else: 
         return standardNormalCDF
        
def priceEuropeanOption(option_type_flag, S, X, T, r, b, v):
    '''
    Black-Scholes
    '''

    d1 = (np.log(S / X) + (b + v**2 / 2) * T) / (v * (T)**0.5)
    d2 = d1 - v * (T)**0.5

    if option_type_flag == CONSTANTS.backend.pricing.flags.type.call:
        bsp = S * np.exp((b - r) * T) * standardNormalCDF(d1) - X * np.exp(-r * T) * standardNormalCDF(d2)
    else:
        bsp = X * np.exp(-r * T) * standardNormalCDF(-d2) - S * np.exp((b - r) * T) * standardNormalCDF(-d1)
        
    return bsp

def priceAmericanOption(option_type_flag, S, X, T, r, b, v):
    '''
    Barone-Adesi-Whaley
    '''
    
    if option_type_flag == CONSTANTS.backend.pricing.flags.type.call:
        return approximateAmericanCall(S, X, T, r, b, v)
    elif option_type_flag == CONSTANTS.backend.pricing.flags.type.put:
        return approximateAmericanPut(S, X, T, r, b, v)
def approximateAmericanCall(S, X, T, r, b, v):
    '''
    Barone-Adesi And Whaley
    '''

    if b >= r:
        return priceEuropeanOption(CONSTANTS.backend.pricing.flags.type.call, S, X, T, r, b, v)
    else:
        Sk = Kc(X, T, r, b, v)
        N = 2 * b / v**2                                           
        k = 2 * r / (v**2 * (1 - np.exp(-1 * r * T)))
        d1 = (np.log(Sk / X) + (b + (v**2) / 2) * T) / (v * (T**0.5))
        Q2 = (-1 * (N - 1) + ((N - 1)**2 + 4 * k))**0.5 / 2
        a2 = (Sk / Q2) * (1 - np.exp((b - r) * T) * standardNormalCDF(d1))
        if S < Sk:
            return priceEuropeanOption(CONSTANTS.backend.pricing.flags.type.call, S, X, T, r, b, v) + a2 * (S / Sk)**Q2
        else:
            return S - X
def approximateAmericanPut(S, X, T, r, b, v):
    '''
    Barone-Adesi-Whaley
    '''

    Sk = Kp(X, T, r, b, v)
    N = 2 * b / v**2
    k = 2 * r / (v**2 * (1 - np.exp(-1 * r * T)))
    d1 = (np.log(Sk / X) + (b + (v**2) / 2) * T) / (v * (T)**0.5)
    Q1 = (-1 * (N - 1) - (((N - 1)**2 + 4 * k))**0.5) / 2
    a1 = -1 * (Sk / Q1) * (1 - np.exp((b - r) * T) * standardNormalCDF(-1 * d1))

    if S > Sk:
        return priceEuropeanOption(CONSTANTS.backend.pricing.flags.type.put, S, X, T, r, b, v) + a1 * (S / Sk)**Q1
    else:
        return X - S
    
def Kc(X, T, r, b, v):

    N = 2 * b / v**2
    m = 2 * r / v**2
    q2u = (-1 * (N - 1) + ((N - 1)**2 + 4 * m)**0.5) / 2
    su = X / (1 - 1 / q2u)
    h2 = -1 * (b * T + 2 * v * (T)**0.5) * X / (su - X)
    Si = X + (su - X) * (1 - np.exp(h2))

    k = 2 * r / (v**2 * (1 - np.exp(-1 * r * T)))
    d1 = (np.log(Si / X) + (b + v**2 / 2) * T) / (v * (T)**0.5)
    Q2 = (-1 * (N - 1) + ((N - 1)**2 + 4 * k)**0.5) / 2
    LHS = Si - X
    RHS = priceEuropeanOption(CONSTANTS.backend.pricing.flags.type.call, Si, X, T, r, b, v) + (1 - np.exp((b - r) * T) * standardNormalCDF(d1)) * Si / Q2
    bi = np.exp((b - r) * T) * standardNormalCDF(d1) * (1 - 1 / Q2) + (1 - np.exp((b - r) * T) * standardNormalPDF(d1) / (v * (T)**0.5)) / Q2

    E = ITERATION_MAX_ERROR
    
    while np.abs(LHS - RHS) / X > E:
        Si = (X + RHS - bi * Si) / (1 - bi)
        d1 = (np.log(Si / X) + (b + v**2 / 2) * T) / (v * (T)**0.5)
        LHS = Si - X
        RHS = priceEuropeanOption(CONSTANTS.backend.pricing.flags.type.call, Si, X, T, r, b, v) + (1 - np.exp((b - r) * T) * standardNormalCDF(d1)) * Si / Q2
        bi = np.exp((b - r) * T) * standardNormalCDF(d1) * (1 - 1 / Q2) + (1 - np.exp((b - r) * T) * standardNormalCDF(d1) / (v * (T)**0.5)) / Q2
    
    return Si
def Kp(X, T, r, b, v):

    N = 2 * b / v**2
    m = 2 * r / v**2
    q1u = (-1 * (N - 1) - ((N - 1)**2 + 4 * m)**0.5) / 2
    su = X / (1 - 1 / q1u)
    h1 = (b * T - 2 * v * (T)**0.5) * X / (X - su)
    Si = su + (X - su) * np.exp(h1)

    k = 2 * r / (v**2 * (1 - np.exp(-1 * r * T)))
    d1 = (np.log(Si / X) + (b + v**2 / 2) * T) / (v * (T)**0.5)
    Q1 = (-1 * (N - 1) - ((N - 1)**2 + 4 * k)**0.5) / 2
    LHS = X - Si
    RHS = priceEuropeanOption( CONSTANTS.backend.pricing.flags.type.put, Si, X, T, r, b, v) - (1 - np.exp((b - r) * T) * standardNormalCDF(-1 * d1)) * Si / Q1
    bi = -1 * np.exp((b - r) * T) * standardNormalCDF(-1 * d1) * (1 - 1 / Q1) - (1 + np.exp((b - r) * T) * standardNormalPDF(-d1) / (v * (T)**0.5)) / Q1
    
    E = ITERATION_MAX_ERROR
    
    while np.abs(LHS - RHS) / X > E:
        Si = (X - RHS + bi * Si) / (1 + bi)
        d1 = (np.log(Si / X) + (b + v**2 / 2) * T) / (v * (T)**0.5)
        LHS = X - Si
        RHS = priceEuropeanOption(CONSTANTS.backend.pricing.flags.type.put, Si, X, T, r, b, v) - (1 - np.exp((b - r) * T) * standardNormalCDF(-1 * d1)) * Si / Q1
        bi = -np.exp((b - r) * T) * standardNormalCDF(-1 * d1) * (1 - 1 / Q1) - (1 + np.exp((b - r) * T) * standardNormalCDF(-1 * d1) / (v * (T)**0.5)) / Q1
        
    return Si

def getValue(option_style_flag, output_flag, option_type_flag, spot_price, strike_price, expiration_time_in_years, interest_rate_dec_pa, carry_rate_dec_pa, volatility_dec_pa):

    S = spot_price
    X = strike_price 
    T = expiration_time_in_years
    r = interest_rate_dec_pa
    b = carry_rate_dec_pa
    v = volatility_dec_pa
    
    if option_style_flag == CONSTANTS.backend.pricing.flags.style.american:
    
        if output_flag == CONSTANTS.backend.pricing.flags.value: 
            return priceAmericanOption(option_type_flag, S, X, T, r, b, v)
        elif output_flag == CONSTANTS.backend.pricing.flags.delta: 
            return (priceAmericanOption(option_type_flag, S + dS, X, T, r, b, v) - priceAmericanOption(option_type_flag, S - dS, X, T, r, b, v)) / (2 * dS)
        elif output_flag == CONSTANTS.backend.pricing.flags.gamma: 
            return (priceAmericanOption(option_type_flag, S + dS, X, T, r, b, v) - 2 * priceAmericanOption(option_type_flag, S, X, T, r, b, v) + priceAmericanOption(option_type_flag, S - dS, X, T, r, b, v)) / dS**2
        elif output_flag == CONSTANTS.backend.pricing.flags.vega:
            return (priceAmericanOption(option_type_flag, S + dS, X, T, r, b, v + dV) - priceAmericanOption(option_type_flag, S + dS, X, T, r, b, v - dV)) / 2
        elif output_flag == CONSTANTS.backend.pricing.flags.theta:
            return priceAmericanOption(option_type_flag, S + dS, X, T - dT, r, b, v) - priceAmericanOption(option_type_flag, S + dS, X, T, r, b, v)
            
    elif option_style_flag == CONSTANTS.backend.pricing.flags.style.european:

        # TODO implement Greeks for european options
        if output_flag == CONSTANTS.backend.pricing.flags.value: 
            return priceEuropeanOption(option_type_flag, S, X, T, r, b, v)

