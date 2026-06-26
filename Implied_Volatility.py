import numpy as np
import math
from scipy.stats import norm

# Defining variables here 
S = 45 #Stock price
K = 40 #Strick price
T = 0.5 #Expiration Date
r = 0.1 # Risk-Free Rate
Cm = 7.29 # market call option value
Pm = 0.34 #market put option value
tol = 0.00001 #tolerance or minimum diff

# Re-creating black-scholes for test
def Calculate_d1_d2(S , K , T , r , vol):
    d1 = (math.log(S/K) + (r + 0.5 * vol**2)*T)/(vol * math.sqrt(T))
    d2 = d1 - vol*math.sqrt(T)
    return d1 , d2

def Calculate_Price_C(S , K , T , r , vol):
    d1 , d2 = Calculate_d1_d2(S , K , T , r , vol)
    C = S*norm.cdf(d1) - K* math.exp(-r * T ) * norm.cdf(d2)

    return C

def Calculate_Price_P(S , K , T , r , vol):
    d1 , d2 = Calculate_d1_d2(S , K , T , r , vol)
    
    P = K*math.exp(-r * T)*norm.cdf(-d2) - S*norm.cdf(-d1)

    return P

#Vega
def vega(S ,  K , T , r , vol):
    d1 , d2 = Calculate_d1_d2(S , K , T , r , vol)
    v = S*norm.pdf(d1) *math.sqrt(T)
    return v;

vol_old_C = 0.5 #initial guess
vol_old_P = 0.5 #initial guess
max_iter = 200 #safety limit

#For Call option
for k in range (max_iter):
    C = Calculate_Price_C(S , K , T ,r , vol_old_C)
    v = vega(S , K , T , r , vol_old_C)

    vol_new_C = vol_old_C - (C - Cm)/v

    if(abs(vol_new_C - vol_old_C) < tol):
        vol_old_C = vol_new_C
        break;
    else:
        vol_old_C = vol_new_C

#For Put option
for k in range (max_iter):
    P = Calculate_Price_P(S , K , T ,r , vol_old_P)
    v = vega(S , K , T , r , vol_old_P)

    vol_new_P = vol_old_P - (P - Pm)/v

    if(abs(vol_new_P - vol_old_P) < tol):
        vol_old_P = vol_new_P
        break;
    else:
        vol_old_P = vol_new_P

print('The Implied Volatility for Call option is : ' , round(vol_old_C , 2))
print('The Implied Volatility for Put option is : ' , round(vol_old_P , 2))
