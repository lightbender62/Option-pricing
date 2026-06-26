from black_scholes import Calculate_Price
from Greeks import Vega

#Tolerance, keeping it fixed so I can standardize it
tol = 1e-6

def Implied_vol(S , K , T , r , Cm , Pm):
    vol_old_C = 0.5 #initial guess
    vol_old_P = 0.5 #initial guess
    max_iter = 200 #safety limit

    b1 = False
    b2 = False

    #Calculation
    for k in range (max_iter):
        # For Call option
        if(b1 == False):
            C,P = Calculate_Price(S , K , T ,r , vol_old_C)
            v = Vega(S , K , T , r , vol_old_C)

            vol_new_C = vol_old_C - (C - Cm)/v

            if(abs(vol_new_C - vol_old_C) < tol):
                vol_old_C = vol_new_C
                b1 = True;
            else:
                vol_old_C = vol_new_C

        #For Put option
        if(b2 == False):
            C , P = Calculate_Price(S , K , T ,r , vol_old_P)
            v = Vega(S , K , T , r , vol_old_P)

            vol_new_P = vol_old_P - (P - Pm)/v

            if(abs(vol_new_P - vol_old_P) < tol):
                vol_old_P = vol_new_P
                b2 = True
            else:
                vol_old_P = vol_new_P

        if(b1 and b2):
            break;
    
    return vol_old_C , vol_old_P