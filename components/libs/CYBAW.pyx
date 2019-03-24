"""
Implements the Barone-Adesi And Whaley model for the valuation of American options and their greeks. 
"""

cimport libc.math as _math

# Option Styles
cdef int _AMERICAN = 11
cdef int _EUROPEAN = 12
# Option Types 
cdef int _CALL = 21
cdef int _PUT = 22
# Output Types 
cdef int _PRICE = 31
cdef int _DELTA = 32
cdef int _GAMMA = 33
cdef int _VEGA = 34
cdef int _THETA = 35

cdef double _dS = 0.001
cdef double _dT = 1 / 365
cdef double _dV = 0.00001

cdef double _ITERATION_MAX_ERROR = 0.001

cdef _standardNormalPDF(double x): 
    val = (1 / (2 * 3.14159265)**0.5) * _math.exp(-1 * (x**2) / 2)
    return val
cdef _standardNormalCDF(double X):     
    y = abs(X) 
    
    if y > 37: 
        return 0
    else:
        Exponential = _math.exp(-1 * (y**2) / 2)
        
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
        _standardNormalCDF = Exponential * SumA / SumB
    else:
        SumA = y + 0.65
        SumA = y + 4 / SumA
        SumA = y + 3 / SumA
        SumA = y + 2 / SumA
        SumA = y + 1 / SumA
        _standardNormalCDF = Exponential / (SumA * 2.506628274631)
    
    if X > 0:
         return 1 - _standardNormalCDF
    else: 
         return _standardNormalCDF
        
cdef _priceEuropeanOption(int option_type_flag, double S, double X, double T, double r, double b, double v):
    '''
    Black-Scholes
    '''

    cdef double d1, d2, bsp

    d1 = (_math.log(S / X) + (b + v**2 / 2) * T) / (v * (T)**0.5)
    d2 = d1 - v * (T)**0.5

    if option_type_flag == _CALL:
        bsp = S * _math.exp((b - r) * T) * _standardNormalCDF(d1) - X * _math.exp(-r * T) * _standardNormalCDF(d2)
    else:
        bsp = X * _math.exp(-r * T) * _standardNormalCDF(-d2) - S * _math.exp((b - r) * T) * _standardNormalCDF(-d1)
        
    return bsp

cdef _priceAmericanOption(int option_type_flag, double S, double X, double T, double r, double b, double v):
    '''
    Barone-Adesi-Whaley
    '''
    
    if option_type_flag == _CALL:
        return _approximateAmericanCall(S, X, T, r, b, v)
    elif option_type_flag == _PUT:
        return _approximateAmericanPut(S, X, T, r, b, v)
cdef _approximateAmericanCall(double S, double X, double T, double r, double b, double v):
    '''
    Barone-Adesi And Whaley
    '''

    cdef double Sk, N, k, d1, Q2, a2

    if b >= r:
        return _priceEuropeanOption(_CALL, S, X, T, r, b, v)
    else:
        Sk = _Kc(X, T, r, b, v)
        N = 2 * b / v**2                                           
        k = 2 * r / (v**2 * (1 - _math.exp(-1 * r * T)))
        d1 = (_math.log(Sk / X) + (b + (v**2) / 2) * T) / (v * (T**0.5))
        Q2 = (-1 * (N - 1) + ((N - 1)**2 + 4 * k))**0.5 / 2
        a2 = (Sk / Q2) * (1 - _math.exp((b - r) * T) * _standardNormalCDF(d1))
        if S < Sk:
            return _priceEuropeanOption(_CALL, S, X, T, r, b, v) + a2 * (S / Sk)**Q2
        else:
            return S - X
cdef _approximateAmericanPut(double S, double X, double T, double r, double b, double v):
    '''
    Barone-Adesi-Whaley
    '''

    cdef double Sk, N, k, d1, Q1, a1

    Sk = _Kp(X, T, r, b, v)
    N = 2 * b / v**2
    k = 2 * r / (v**2 * (1 - _math.exp(-1 * r * T)))
    d1 = (_math.log(Sk / X) + (b + (v**2) / 2) * T) / (v * (T)**0.5)
    Q1 = (-1 * (N - 1) - (((N - 1)**2 + 4 * k))**0.5) / 2
    a1 = -1 * (Sk / Q1) * (1 - _math.exp((b - r) * T) * _standardNormalCDF(-1 * d1))

    if S > Sk:
        return _priceEuropeanOption(_PUT, S, X, T, r, b, v) + a1 * (S / Sk)**Q1
    else:
        return X - S
    
cdef _Kc(double X, double T, double r, double b, double v):

    cdef double N, m, q2u, su, h2, Si
    cdef double k, d1, Q2
    cdef double LHS, RHS
    cdef double bi, E

    N = 2 * b / v**2
    m = 2 * r / v**2
    q2u = (-1 * (N - 1) + ((N - 1)**2 + 4 * m)**0.5) / 2
    su = X / (1 - 1 / q2u)
    h2 = -1 * (b * T + 2 * v * (T)**0.5) * X / (su - X)
    Si = X + (su - X) * (1 - _math.exp(h2))

    k = 2 * r / (v**2 * (1 - _math.exp(-1 * r * T)))
    d1 = (_math.log(Si / X) + (b + v**2 / 2) * T) / (v * (T)**0.5)
    Q2 = (-1 * (N - 1) + ((N - 1)**2 + 4 * k)**0.5) / 2
    LHS = Si - X
    RHS = _priceEuropeanOption(_CALL, Si, X, T, r, b, v) + (1 - _math.exp((b - r) * T) * _standardNormalCDF(d1)) * Si / Q2
    bi = _math.exp((b - r) * T) * _standardNormalCDF(d1) * (1 - 1 / Q2) + (1 - _math.exp((b - r) * T) * _standardNormalPDF(d1) / (v * (T)**0.5)) / Q2

    E = _ITERATION_MAX_ERROR
    
    while abs(LHS - RHS) / X > E:
        Si = (X + RHS - bi * Si) / (1 - bi)
        d1 = (_math.log(Si / X) + (b + v**2 / 2) * T) / (v * (T)**0.5)
        LHS = Si - X
        RHS = _priceEuropeanOption(_CALL, Si, X, T, r, b, v) + (1 - _math.exp((b - r) * T) * _standardNormalCDF(d1)) * Si / Q2
        bi = _math.exp((b - r) * T) * _standardNormalCDF(d1) * (1 - 1 / Q2) + (1 - _math.exp((b - r) * T) * _standardNormalCDF(d1) / (v * (T)**0.5)) / Q2
    
    return Si
cdef _Kp(double X, double T, double r, double b, double v):

    cdef double N, m, q1u, su, h1, Si
    cdef double k, d1, Q1
    cdef double LHS, RHS
    cdef double bi, E

    N = 2 * b / v**2
    m = 2 * r / v**2
    q1u = (-1 * (N - 1) - ((N - 1)**2 + 4 * m)**0.5) / 2
    su = X / (1 - 1 / q1u)
    h1 = (b * T - 2 * v * (T)**0.5) * X / (X - su)
    Si = su + (X - su) * _math.exp(h1)

    k = 2 * r / (v**2 * (1 - _math.exp(-1 * r * T)))
    d1 = (_math.log(Si / X) + (b + v**2 / 2) * T) / (v * (T)**0.5)
    Q1 = (-1 * (N - 1) - ((N - 1)**2 + 4 * k)**0.5) / 2
    LHS = X - Si
    RHS = _priceEuropeanOption( _PUT, Si, X, T, r, b, v) - (1 - _math.exp((b - r) * T) * _standardNormalCDF(-1 * d1)) * Si / Q1
    bi = -1 * _math.exp((b - r) * T) * _standardNormalCDF(-1 * d1) * (1 - 1 / Q1) - (1 + _math.exp((b - r) * T) * _standardNormalPDF(-d1) / (v * (T)**0.5)) / Q1
    
    E = _ITERATION_MAX_ERROR
    
    while abs(LHS - RHS) / X > E:
        Si = (X - RHS + bi * Si) / (1 + bi)
        d1 = (_math.log(Si / X) + (b + v**2 / 2) * T) / (v * (T)**0.5)
        LHS = X - Si
        RHS = _priceEuropeanOption(_PUT, Si, X, T, r, b, v) - (1 - _math.exp((b - r) * T) * _standardNormalCDF(-1 * d1)) * Si / Q1
        bi = -_math.exp((b - r) * T) * _standardNormalCDF(-1 * d1) * (1 - 1 / Q1) - (1 + _math.exp((b - r) * T) * _standardNormalCDF(-1 * d1) / (v * (T)**0.5)) / Q1
        
    return Si

cdef _checkBadFlagInput(int option_style_flag, int output_flag, int option_type_flag):

    styles = (_AMERICAN, _EUROPEAN)
    if option_style_flag not in styles:
        raise ValueError('Option Style must be one of %s' % (styles))
    outputs = (_PRICE, _DELTA, _GAMMA, _VEGA, _THETA)
    if output_flag not in outputs:
        raise ValueError('Output Type must be one of %s' % (outputs))
    types = (_CALL, _PUT)
    if option_type_flag not in types:
        raise ValueError('Option Type must be one of %s' % (types))

cdef _checkBadNumericInput(double spot_price, double strike_price, double expiration_time_in_years, double interest_rate_dec_pa, double carry_rate_dec_pa, double volatility_dec_pa):
    
    if spot_price <= 0:
        raise ValueError('Spot Price must be > 0')
    if strike_price <= 0:
        raise ValueError('Strike Price must be > 0')
    if expiration_time_in_years <= 0:
        raise ValueError('Time until Expiration must be > 0')
    if interest_rate_dec_pa < 0 or interest_rate_dec_pa >= 1:
        raise ValueError('Interest rate in annualized decimal format must be > 0 and < 1.00')
    if carry_rate_dec_pa < 0 or carry_rate_dec_pa >= 1:
        raise ValueError('Carry Rate in annualized decimal format must be > 0 and < 1.00')
    if volatility_dec_pa <= 0 or volatility_dec_pa >= 10.00:
        raise ValueError('Volatility in annualized decimal format must be > 0 and < 10.00 ')

cpdef getValue(int option_style_flag, int output_flag, int option_type_flag, double spot_price, double strike_price, double expiration_time_in_years, double interest_rate_dec_pa, double carry_rate_dec_pa, double volatility_dec_pa):
    '''Returns the value of a financial option according to the specified flag and numeric inputs,

    Keyword arguments:
    option_style_flag -- specifies the style of option to be valued. Must be contained in ('American', 'European')
    output_flag -- specifies the option characteristic value to be calculated. 
                    For price, give 'Price'. 
                    For an option greek, give one of ('Delta', 'Gamma', 'Vega', 'Theta').
    option_type_flag -- specifies the type of option to be valued. Must be contained in (_CALL, _PUT)
    spot_price -- Spot price of the underlying asset. Must be > 0.
    strike_price -- Strike price of the option. Must be > 0.
    expiration_time_in_years -- Time until Expiration. Must be > 0. 
    interest_rate_dec_pa -- Interest rate in annualized decimal format. Must be > 0 and < 1.00.
    carry_rate_dec_pa -- Carry rate in annualized decimal format. Must be > 0 and < 1.00.
    volatility_dec_pa -- Volatility in annualized decimal format. Must be > 0 and < 10.00
    '''

    cdef double S, X, T, r, b, v

    S = spot_price
    X = strike_price 
    T = expiration_time_in_years
    r = interest_rate_dec_pa
    b = carry_rate_dec_pa
    v = volatility_dec_pa

    _checkBadFlagInput(option_style_flag, output_flag, option_type_flag)
    _checkBadNumericInput(S, X, T, r, b, v)

    if option_style_flag == _AMERICAN:
        priceOption = _priceAmericanOption
    elif option_style_flag == _EUROPEAN:
        priceOption = _priceEuropeanOption
    
    if output_flag == _PRICE: 
        return priceOption(option_type_flag, S, X, T, r, b, v)
    elif output_flag == _DELTA: 
        return (priceOption(option_type_flag, S + _dS, X, T, r, b, v) - priceOption(option_type_flag, S - _dS, X, T, r, b, v)) / (2 * _dS)
    elif output_flag == _GAMMA: 
        return (priceOption(option_type_flag, S + _dS, X, T, r, b, v) - 2 * priceOption(option_type_flag, S, X, T, r, b, v) + priceOption(option_type_flag, S - _dS, X, T, r, b, v)) / _dS**2
    elif output_flag == _VEGA:
        return (priceOption(option_type_flag, S + _dS, X, T, r, b, v + _dV) - priceOption(option_type_flag, S + _dS, X, T, r, b, v - _dV)) / 2
    elif output_flag == _THETA:
        return priceOption(option_type_flag, S + _dS, X, T - _dT, r, b, v) - priceOption(option_type_flag, S + _dS, X, T, r, b, v)
        