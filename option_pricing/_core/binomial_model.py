"""
Binomial tree (CRR) option pricing model.
"""
import numpy as np

def binomial_price(S0, K, T, r, sigma, N):

    #precomute constants
    dt = T/N
    u = np.exp(sigma*np.sqrt(dt))
    d = 1/u
    q = (np.exp(r*dt) - d) / (u-d)
    disc = np.exp(-r*dt)

    # initialise asset prices at maturity - Time step N
    S = np.zeros(N+1)
    S[0] = S0*d**N
    for j in range(1,N+1):
        S[j] = S[j-1]*u/d

    # initialise option values at maturity
    C = np.zeros(N+1)
    P = np.zeros(N+1)
    for j in range(0,N+1):
        C[j] = max(0, S[j]-K)
        P[j] = max(0, K - S[j])

    # step backwards through tree
    for i in np.arange(N,0,-1):
        for j in range(0,i):
            C[j] = disc * ( q*C[j+1] + (1-q)*C[j])
            P[j] = disc * (q*P[j+1] + (1-q)*P[j])
    
    return C[0] , P[0]

def american_price(S0, K, T, r, sigma, N):
    # precompute constants
    dt = T / N
    u = np.exp(sigma * np.sqrt(dt))
    d = 1 / u
    q = (np.exp(r * dt) - d) / (u - d)
    disc = np.exp(-r * dt)

    # initialise asset prices at maturity
    S = np.zeros(N + 1)
    S[0] = S0 * d**N
    for j in range(1, N + 1):
        S[j] = S[j - 1] * u / d

    # initialise option values at maturity
    C = np.zeros(N + 1)
    P = np.zeros(N + 1)
    for j in range(0, N + 1):
        C[j] = max(0, S[j] - K)
        P[j] = max(0, K - S[j])

    # step backwards — early exercise check added here
    for i in np.arange(N, 0, -1):
        for j in range(0, i):
            S[j] = S[j] * u  # update stock price at this node
            C[j] = max(disc * (q * C[j + 1] + (1 - q) * C[j]), S[j] - K)
            P[j] = max(disc * (q * P[j + 1] + (1 - q) * P[j]), K - S[j])

    return C[0], P[0]
