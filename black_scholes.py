import math
from scipy.stats import norm

# Defining variables here 
S = 45 #Stock price
K = 40 #Strick price
T = 0.5 #Expiration Date
r = 0.1 # Risk-Free Rate
vol = 0.2 #Volatility (sigma)

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

C , P = Calculate_Price(S , K , T , r , vol)

#Printing Results 
print('The Value of d1 is : ' , round(d1 , 4))
print('The Value of d2 is : ' , round(d2 , 4))
print('The Price of the call option is : $' , round(C , 2))
print('The Price of the Put option is : $' , round(P , 2))
