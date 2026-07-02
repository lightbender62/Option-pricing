"""
Implied volatility solver using Newton-Raphson method.
"""
from option_pricing._core.black_scholes import calculate_price
from option_pricing._core.greeks import calculate_vega

tol = 1e-6

def calculate_iv(S, K, T, r, call_market, put_market):
    vol_old_C = 0.5 #initial guess
    vol_old_P = 0.5 #initial guess
    max_iter = 200 #safety limit

    b1 = False
    b2 = False

    #Calculation
    for _ in range (max_iter):
        # For Call option
        if(not b1):
            C,P = calculate_price(S , K , T ,r , vol_old_C)
            v = calculate_vega(S , K , T , r , vol_old_C)

            vol_new_C = vol_old_C - (C - call_market)/v

            if(abs(vol_new_C - vol_old_C) < tol):
                vol_old_C = vol_new_C
                b1 = True
            else:
                vol_old_C = vol_new_C

        #For Put option
        if(not b2):
            C , P = calculate_price(S , K , T ,r , vol_old_P)
            v = calculate_vega(S , K , T , r , vol_old_P)

            vol_new_P = vol_old_P - (P - put_market)/v

            if(abs(vol_new_P - vol_old_P) < tol):
                vol_old_P = vol_new_P
                b2 = True
            else:
                vol_old_P = vol_new_P

        if(b1 and b2):
            break
    
    return vol_old_C , vol_old_P