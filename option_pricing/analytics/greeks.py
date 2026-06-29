from option_pricing.models.black_scholes import Calculate_d1_d2
import math
from scipy.stats import norm

def Greeks(S , K , T , r , vol):
    # Getting d1 , d2 again
    d1 , d2 = Calculate_d1_d2(S , K , T, r , vol)

    #delta
    delta_call = norm.cdf(d1)
    delta_put = norm.cdf(d1) - 1

    #Gamma
    gamma = norm.pdf(d1) /(S*vol*math.sqrt(T))

    #Theta (daily)
    theta_call = -(S*norm.pdf(d1)*vol)/(2*math.sqrt(T)) - r*K*math.exp(-r*T)*norm.cdf(d2)
    theta_call/=365
    theta_put = -(S*norm.pdf(d1)*vol)/(2*math.sqrt(T)) + r*K*math.exp(-r*T)*norm.cdf(-d2)
    theta_put /=365

    #Vega
    vega = S*norm.pdf(d1) *math.sqrt(T)

    #Rho
    rho_call = K*T*math.exp(-r*T)*norm.cdf(d2)
    rho_put = -K*T*math.exp(-r*T)*norm.cdf(-d2)

    return delta_call , delta_put , gamma , theta_call , theta_put , vega , rho_call , rho_put

#just for implied volatility
def Vega(S , K , T , r , vol):
    # Getting d1 , d2 again
    d1 , _ = Calculate_d1_d2(S , K , T, r , vol)

    #Vega
    vega = S*norm.pdf(d1) *math.sqrt(T)
    return vega


