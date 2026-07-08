"""
Implied volatility solver using Newton-Raphson method.
"""
from option_pricing._core.black_scholes import calculate_price
from option_pricing._core.greeks import calculate_vega

tol = 1e-6

def calculate_iv(S, K, T, r, call_market, put_market):
    if S <= 0:
        raise ValueError(f"S must be positive, got {S}")
    if K <= 0:
        raise ValueError(f"K must be positive, got {K}")
    if T <= 0:
        raise ValueError(f"T must be positive, got {T}")
    if call_market < 0:
        raise ValueError(f"call_market must be non-negative, got {call_market}")
    if put_market < 0:
        raise ValueError(f"put_market must be non-negative, got {put_market}")

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

            if abs(v) < 1e-10:
                raise ValueError("IV solver failed for call: vega too close to zero, Newton-Raphson step is unstable.")

            vol_new_C = vol_old_C - (C - call_market)/v

            if vol_new_C <= 0:
                raise ValueError("IV solver failed for call: sigma stepped to a non-positive value, no solution in valid range.")

            if(abs(vol_new_C - vol_old_C) < tol):
                vol_old_C = vol_new_C
                b1 = True
            else:
                vol_old_C = vol_new_C

        #For Put option
        if(not b2):
            C , P = calculate_price(S , K , T ,r , vol_old_P)
            v = calculate_vega(S , K , T , r , vol_old_P)

            if abs(v) < 1e-10:
                raise ValueError("IV solver failed for put: vega too close to zero, Newton-Raphson step is unstable.")

            vol_new_P = vol_old_P - (P - put_market)/v

            if vol_new_P <= 0:
                raise ValueError("IV solver failed for put: sigma stepped to a non-positive value, no solution in valid range.")

            if(abs(vol_new_P - vol_old_P) < tol):
                vol_old_P = vol_new_P
                b2 = True
            else:
                vol_old_P = vol_new_P

        if(b1 and b2):
            break

    if not b1:
        raise ValueError(f"IV solver did not converge for call within {max_iter} iterations.")
    if not b2:
        raise ValueError(f"IV solver did not converge for put within {max_iter} iterations.")
    
    return vol_old_C , vol_old_P