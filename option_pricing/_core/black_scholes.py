"""
Black-Scholes analytical pricing model.
"""
import math
from scipy.stats import norm


#Calculating d1 & d2

def calculate_d1_d2(S, K, T, r, sigma):
    d1 = (math.log(S/K) + (r + 0.5 * sigma**2)*T)/(sigma * math.sqrt(T))
    d2 = d1 - sigma*math.sqrt(T)
    return d1 , d2

#Calculate Call price & Put Price
def calculate_price(S, K, T, r, sigma):
    d1 , d2 = calculate_d1_d2(S , K , T , r , sigma)
    call = S*norm.cdf(d1) - K* math.exp(-r * T ) * norm.cdf(d2)

    put = K*math.exp(-r * T)*norm.cdf(-d2) - S*norm.cdf(-d1)

    return call , put

#Calculate Call Price & Put Price for Asian options
def asian_price_geometric(S , K , T , r , sigma):
    sigma_adjusted = sigma/math.sqrt(3)
    r_adjusted = 0.5*(r - 0.5*sigma**2) + 0.5*sigma_adjusted**2

    d1 , d2 = calculate_d1_d2(S , K , T , r_adjusted , sigma_adjusted)
    call = math.exp(-r*T)*((S*math.exp(r_adjusted*T)*norm.cdf(d1)) - (K*norm.cdf(d2)))
    put = math.exp(-r*T)*(K*norm.cdf(-d2) - S*math.exp(r_adjusted*T)*norm.cdf(-d1))

    return call , put
