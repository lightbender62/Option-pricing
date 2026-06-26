import math
from scipy.stats import norm


#Calculating d1 & d2

def Calculate_d1_d2(S , K , T , r , vol):
    d1 = (math.log(S/K) + (r + 0.5 * vol**2)*T)/(vol * math.sqrt(T))
    d2 = d1 - vol*math.sqrt(T)
    return d1 , d2

#Calculate Call price & Put Price
def Calculate_Price(S , K , T , r , vol):
    d1 , d2 = Calculate_d1_d2(S , K , T , r , vol)
    C = S*norm.cdf(d1) - K* math.exp(-r * T ) * norm.cdf(d2)

    P = K*math.exp(-r * T)*norm.cdf(-d2) - S*norm.cdf(-d1)

    return C , P
