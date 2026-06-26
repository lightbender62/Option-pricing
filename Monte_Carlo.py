import numpy as np

def Monte_Carlo(S , K , r , T , vol , N , M):
    #precompute constants
    dt = T/N
    nudt = (r - 0.5*vol**2)*dt
    volsdt = vol*np.sqrt(dt)
    lnS = np.log(S)

    #Monte carlo methoed
    Z = np.random.normal(size=(N , M))
    delta_lnSt = nudt + volsdt*Z
    lnSt = lnS + np.cumsum(delta_lnSt , axis=0)
    lnSt = np.concatenate((np.full(shape=(1 , M) , fill_value=lnS) , lnSt))

    #compute Expectation
    ST = np.exp(lnSt)
    CT = np.maximum(0 , ST - K)
    PT = np.maximum(0 , K-ST)

    C0 = np.exp(-r*T)*np.sum(CT[-1])/M
    P0 = np.exp(-r*T)*np.sum(PT[-1])/M

    return C0, P0


