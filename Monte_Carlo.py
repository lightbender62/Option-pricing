import numpy as np

# Defining variables here 
S = 45 #Stock price
K = 40 #Strick price
T = 0.5 #Expiration Date
r = 0.1 # Risk-Free Rate
vol = 0.2 #Volatility (sigma)
N = 100 #Time Steps number
M = 1000 #Number of Simulations

#precompute constants
dt = T/N
nudt = (r - 0.5*vol**2)*dt
volsdt = vol*np.sqrt(dt)
lnS = np.log(S)

#Monte carlo methoed
sum_ct = 0
sum_pt = 0

for i in range(M):
    lnSt = lnS
    for j in range (N):
        lnSt = lnSt + nudt + volsdt*np.random.normal()
    
    ST = np.exp(lnSt)
    CT = max(0 , ST - K)
    PT = max(0 , K-ST)
    sum_ct += CT
    sum_pt += PT

#compute Expectation
C0 = np.exp(-r*T)*sum_ct/M
P0 = np.exp(-r*T)*sum_pt/M
print('The Price of the call option is : $' , round(C0 , 2))
print('The Price of the Put option is : $' , round(P0 , 2))

