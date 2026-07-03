"""
Monte Carlo simulation for option pricing using Geometric Brownian Motion.
"""
import numpy as np

def monte_carlo_price(S, K, T, r, sigma, N, M):
    #precompute constants
    dt = T/N
    nudt = (r - 0.5*sigma**2)*dt
    sigmasdt = sigma*np.sqrt(dt)
    lnS = np.log(S)

    #Monte carlo method
    half = (M + 1) // 2

    Z = np.random.normal(size=(N, half))
    Z = np.concatenate((Z, -Z), axis=1)[:, :M]
    delta_lnSt = nudt + sigmasdt*Z
    lnSt = lnS + np.cumsum(delta_lnSt , axis=0)
    lnSt = np.concatenate((np.full(shape=(1 , M) , fill_value=lnS) , lnSt))

    #compute Expectation
    ST = np.exp(lnSt)
    CT = np.maximum(0 , ST - K)
    PT = np.maximum(0 , K-ST)

    call = np.exp(-r*T)*np.sum(CT[-1])/M
    put = np.exp(-r*T)*np.sum(PT[-1])/M

    return call, put


