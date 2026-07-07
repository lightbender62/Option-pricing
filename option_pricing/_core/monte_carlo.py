"""
Monte Carlo simulation for option pricing using Geometric Brownian Motion.
"""
import numpy as np


def simulate_paths(S, T, r, sigma, N, M):
    #precompute constants
    dt = T / N
    nudt = (r - 0.5 * sigma**2) * dt
    sigmasdt = sigma * np.sqrt(dt)
    lnS = np.log(S)

    #Monte carlo method
    Z = np.random.normal(size=(N, M))
    delta_lnSt = nudt + sigmasdt * Z
    lnSt = lnS + np.cumsum(delta_lnSt, axis=0)
    lnSt = np.concatenate((np.full(shape=(1, M), fill_value=lnS), lnSt))

    return np.exp(lnSt)

def european_price(S, K, T, r, sigma, N, M):
    paths = simulate_paths(S , T , r , sigma , N , M)
    ST = paths[-1]
    CT = np.maximum(0 , ST - K)
    PT = np.maximum(0 , K-ST)

    call = np.exp(-r*T)*np.mean(CT)
    put = np.exp(-r*T)*np.mean(PT)

    return call, put

def asian_price_arithmetic(S ,K , T , r , sigma , N , M):
    St = simulate_paths(S , T , r , sigma , N , M)
    average_St = np.mean(St[1:] , axis = 0)
    Ct = np.maximum(0 , average_St - K)
    Pt = np.maximum(0 , K - average_St)

    call = np.exp(-r*T)*np.mean(Ct)
    put = np.exp(-r*T)*np.mean(Pt)

    return call , put

def asian_price_geometric(S , K , T ,r , sigma , N , M):
    paths = simulate_paths(S , T , r , sigma , N , M)
    lnSt = np.log(paths)
    average_lnSt = np.mean(lnSt[1:] , axis = 0)
    average_St = np.exp(average_lnSt)
    Ct = np.maximum(0 , average_St - K)
    Pt = np.maximum(0 , K-average_St)

    call = np.exp(-r*T)*np.mean(Ct)
    put = np.exp(-r*T)*np.mean(Pt)

    return call , put

def barrier_price(S , K , T , r , sigma , N , M , H , barrier_type):
    if "down" in barrier_type and H >= S:
        raise ValueError("For down barriers, H must be less than S.")

    if "up" in barrier_type and H <= S:
        raise ValueError("For up barriers, H must be greater than S.")
    paths = simulate_paths(S , T , r , sigma , N , M)
    ST = paths[-1]
    CT = np.maximum(0 , ST - K)
    PT = np.maximum(0 , K-ST) 
    if barrier_type == "down-and-out":
        crossed = np.any(paths<=H , axis=0)
        CT[crossed] = 0
        PT[crossed] = 0
    
    elif barrier_type == "down-and-in":
        crossed = np.any(paths<=H , axis=0)
        CT[~crossed] = 0
        PT[~crossed] = 0
        
    elif barrier_type == "up-and-out":
        crossed = np.any(paths>=H , axis=0)
        CT[crossed] = 0
        PT[crossed] = 0
        
    elif barrier_type == "up-and-in":
        crossed = np.any(paths>=H , axis=0)
        CT[~crossed] = 0
        PT[~crossed] = 0
    else:
        raise ValueError(
            "Invalid barrier type. Choose from "
            "'down-and-out', 'down-and-in', "
            "'up-and-out', 'up-and-in'."
        )
    
    call = np.exp(-r*T)*np.mean(CT)
    put = np.exp(-r*T)*np.mean(PT)

    return call, put

def lookback_price_floating(S , T , r , sigma , N , M):
    paths = simulate_paths(S , T , r , sigma , N , M)
    S_minimum = np.min(paths , axis = 0)
    S_maximum = np.max(paths , axis = 0)

    CT = paths[-1] - S_minimum
    PT = S_maximum - paths[-1]
    
    call = np.exp(-r*T)*np.mean(CT)
    put = np.exp(-r*T)*np.mean(PT)

    return call , put

def lookback_price_fixed(S ,K , T , r , sigma , N , M):
    paths = simulate_paths(S , T , r , sigma , N , M)
    S_minimum = np.min(paths , axis = 0)
    S_maximum = np.max(paths , axis = 0)

    CT = np.maximum(S_maximum - K, 0)
    PT = np.maximum(K - S_minimum, 0)
    
    call = np.exp(-r*T)*np.mean(CT)
    put = np.exp(-r*T)*np.mean(PT)

    return call , put
    

        
    

