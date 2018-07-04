"""
Implements the Barone-Adesi And Whaley model for the pricing of American options. 
"""

import numpy as np
import cmath as m

from Constants import derivat_constants as CONSTANTS

def ND(x):  ## PDF for standard normal
    val = (1 / (2 * m.pi)**0.5) * np.exp(-1 * (x**2) / 2)
    return val

def CND(X):     
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
        CND = Exponential * SumA / SumB
    else:
        SumA = y + 0.65
        SumA = y + 4 / SumA
        SumA = y + 3 / SumA
        SumA = y + 2 / SumA
        SumA = y + 1 / SumA
        CND = Exponential / (SumA * 2.506628274631)
    
    if X > 0:
         return 1 - CND
    else: 
         return CND

    
##### Black Scholes Function -----> WORKS! #####
        
def GBlackScholes(CallPutFlag, S, X, T, r, b, v):

    d1 = (np.log(S / X) + (b + v**2 / 2) * T) / (v * (T)**0.5)
    d2 = d1 - v * (T)**0.5

    if CallPutFlag == CONSTANTS.backend.pricing.flags.call:
        bsp = S * np.exp((b - r) * T) * CND(d1) - X * np.exp(-r * T) * CND(d2)
    else:
        bsp = X * np.exp(-r * T) * CND(-d2) - S * np.exp((b - r) * T) * CND(-d1)
        
    return bsp

def BAWAmericanApprox(CallPutFlag, S, X, T, r, b, v):
    
    if CallPutFlag == CONSTANTS.backend.pricing.flags.call:
        AmericanApprox = BAWAmericanCallApprox(S, X, T, r, b, v)
    else:
        AmericanApprox = BAWAmericanPutApprox(S, X, T, r, b, v)
        
    return AmericanApprox

################################################
        
## American call
def BAWAmericanCallApprox(S, X, T, r, b, v):

    if b >= r:
        AmericanCallApprox = GBlackScholes(CONSTANTS.backend.pricing.flags.call, S, X, T, r, b, v)
    else:
        Sk = Kc(X, T, r, b, v)
        N = 2 * b / v**2                                           
        k = 2 * r / (v**2 * (1 - np.exp(-1 * r * T)))
        d1 = (np.log(Sk / X) + (b + (v**2) / 2) * T) / (v * (T**0.5))
        Q2 = (-1 * (N - 1) + ((N - 1)**2 + 4 * k))**0.5 / 2
        a2 = (Sk / Q2) * (1 - np.exp((b - r) * T) * CND(d1))
        if S < Sk:
            AmericanCallApprox = GBlackScholes(CONSTANTS.backend.pricing.flags.call, S, X, T, r, b, v) + a2 * (S / Sk)**Q2
        else:
            AmericanCallApprox = S - X
    return AmericanCallApprox
    
def BAWAmericanPutApprox(S, X, T, r, b, v):

    Sk = Kp(X, T, r, b, v)
    N = 2 * b / v**2
    k = 2 * r / (v**2 * (1 - np.exp(-1 * r * T)))
    d1 = (np.log(Sk / X) + (b + (v**2) / 2) * T) / (v * (T)**0.5)
    Q1 = (-1 * (N - 1) - (((N - 1)**2 + 4 * k))**0.5) / 2
    a1 = -1 * (Sk / Q1) * (1 - np.exp((b - r) * T) * CND(-1 * d1))

    if S > Sk:
        AmericanPutApprox = GBlackScholes(CONSTANTS.backend.pricing.flags.put, S, X, T, r, b, v) + a1 * (S / Sk)**Q1
    else:
        AmericanPutApprox = X - S
    
    return AmericanPutApprox
    
## Newton Raphson algorithm to solve for the critical commodity price for a Call
def Kc(X, T, r, b, v):

    ## Calculation of seed value, Si
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
    RHS = GBlackScholes(CONSTANTS.backend.pricing.flags.call, Si, X, T, r, b, v) + (1 - np.exp((b - r) * T) * CND(d1)) * Si / Q2
    bi = np.exp((b - r) * T) * CND(d1) * (1 - 1 / Q2) + (1 - np.exp((b - r) * T) * ND(d1) / (v * (T)**0.5)) / Q2
    #E = 0.000001
    E = 0.001 # faster interation
    ## newton Raphson algorithm for finding critical price Si
    
    while np.abs(LHS - RHS) / X > E:
        Si = (X + RHS - bi * Si) / (1 - bi)
        d1 = (np.log(Si / X) + (b + v**2 / 2) * T) / (v * (T)**0.5)
        LHS = Si - X
        RHS = GBlackScholes(CONSTANTS.backend.pricing.flags.call, Si, X, T, r, b, v) + (1 - np.exp((b - r) * T) * CND(d1)) * Si / Q2
        bi = np.exp((b - r) * T) * CND(d1) * (1 - 1 / Q2) + (1 - np.exp((b - r) * T) * CND(d1) / (v * (T)**0.5)) / Q2
    
    return Si

def Kp(X, T, r, b, v):

    ## Calculation of seed value, Si
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
    RHS = GBlackScholes( CONSTANTS.backend.pricing.flags.put, Si, X, T, r, b, v) - (1 - np.exp((b - r) * T) * CND(-1 * d1)) * Si / Q1
    bi = -1 * np.exp((b - r) * T) * CND(-1 * d1) * (1 - 1 / Q1) - (1 + np.exp((b - r) * T) * ND(-d1) / (v * (T)**0.5)) / Q1
   # E = 0.000001
    E = 0.1 # faster interation
   ## Newton Raphson algorithm for finding critical price Si
    
    while np.abs(LHS - RHS) / X > E:
        Si = (X - RHS + bi * Si) / (1 + bi)
        d1 = (np.log(Si / X) + (b + v**2 / 2) * T) / (v * (T)**0.5)
        LHS = X - Si
        RHS = GBlackScholes(CONSTANTS.backend.pricing.flags.put, Si, X, T, r, b, v) - (1 - np.exp((b - r) * T) * CND(-1 * d1)) * Si / Q1
        bi = -np.exp((b - r) * T) * CND(-1 * d1) * (1 - 1 / Q1) - (1 + np.exp((b - r) * T) * CND(-1 * d1) / (v * (T)**0.5)) / Q1
        
    return Si

def EBAWAmericanApprox(OutPutFlag, CallPutFlag, S, X, T, r, b, v):
    
    dS = 0.001
    
    if OutPutFlag == CONSTANTS.backend.pricing.flags.value: 
        EBAWAmericanApprox_ = BAWAmericanApprox(CallPutFlag, S, X, T, r, b, v)
    elif OutPutFlag == CONSTANTS.backend.pricing.flags.delta: 
         EBAWAmericanApprox_ = (BAWAmericanApprox(CallPutFlag, S + dS, X, T, r, b, v) - BAWAmericanApprox(CallPutFlag, S - dS, X, T, r, b, v)) / (2 * dS)
    elif OutPutFlag == CONSTANTS.backend.pricing.flags.gamma: 
        EBAWAmericanApprox_ = (BAWAmericanApprox(CallPutFlag, S + dS, X, T, r, b, v) - 2 * BAWAmericanApprox(CallPutFlag, S, X, T, r, b, v) + BAWAmericanApprox(CallPutFlag, S - dS, X, T, r, b, v)) / dS**2
    elif OutPutFlag == CONSTANTS.backend.pricing.flags.vega:
         EBAWAmericanApprox_ = (BAWAmericanApprox(CallPutFlag, S, X, T, r, b, v + 0.00001) - BAWAmericanApprox(CallPutFlag, S, X, T, r, b, v - 0.00001)) / 2
    elif OutPutFlag == CONSTANTS.backend.pricing.flags.theta:
        if T <= 1 / 365:
                EBAWAmericanApprox_ = BAWAmericanApprox(CallPutFlag, S, X, 0.00001, r, b, v) - BAWAmericanApprox(CallPutFlag, S, X, T, r, b, v)
        else:
                EBAWAmericanApprox_ = BAWAmericanApprox(CallPutFlag, S, X, T - 1 / 365, r, b, v) - BAWAmericanApprox(CallPutFlag, S, X, T, r, b, v)
       
    return EBAWAmericanApprox_