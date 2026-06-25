import sys
sys.path.append('.')
from black_scholes import Calculate_d1_d2
import math
from scipy.stats import norm

# Defining variables here 
S = 45 #Stock price
K = 40 #Strick price
T = 0.5 #Expiration Date
r = 0.1 # Risk-Free Rate
vol = 0.2 #Volatility (sigma)

def Greeks(S , K , T , r , vol):
    # Getting d1 , d2 again
    d1 , d2 = Calculate_d1_d2(S , K , T, r , vol)

    #delta
    delta_call = norm.cdf(d1)
    delta_put = norm.cdf(d1) - 1

    #Gamma
    gamma = norm.pdf(d1) /(S*vol*math.sqrt(T))

    #Theta 
    theta_call = -(S*norm.pdf(d1)*vol)/(2*math.sqrt(T)) - r*K*math.exp(-r*T)*norm.cdf(d2)
    theta_put = -(S*norm.pdf(d1)*vol)/(2*math.sqrt(T)) + r*K*math.exp(-r*T)*norm.cdf(-d2)

    #Vega
    vega = S*norm.pdf(d1) *math.sqrt(T)

    #Rho
    rho_call = K*T*math.exp(-r*T)*norm.cdf(d2)
    rho_put = -K*T*math.exp(-r*T)*norm.cdf(-d2)

    return delta_call , delta_put , gamma , theta_call , theta_put , vega , rho_call , rho_put

dc , dp , g , tc , tp , v , rc , rp = Greeks(S , K , T , r , vol)

print('The Value of Delta for Call function is : ' , round(dc , 4))
print('The Value of Delta for put function is : ' , round(dp , 4))
print('The Value of Gamma is : ' , round(g , 4))
print('The Value of Theta for Call function is : ' , round(tc , 4))
print('The Value of Theta for put function is : ' , round(tp , 4))
print('The Value of Vega is : ' , round(v , 4))
print('The Value of Rho for Call function is : ' , round(rc , 4))
print('The Value of Rho for put function is : ' , round(rp , 4))


