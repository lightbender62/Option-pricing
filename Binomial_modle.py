import numpy as np

# Initialise parameters
S0 = 45      # initial stock price
K = 40       # strike price
T = 0.5       # time to maturity in years
r = 0.1      # annual risk-free rate
N = 100       # number of time steps
sigma = 0.2   # Annualised stock price volatility

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


print('The Price of the call option is : $' , round(C[0] , 2))
print('The Price of the Put option is : $' , round(P[0] , 2))
