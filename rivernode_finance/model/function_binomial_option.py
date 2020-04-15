
import sys
import os
import json
import requests
import time

from scipy.optimize import minimize
from sklearn.metrics import mean_squared_error

class FunctionBinominalOption(object):

    def __init__(self, variant):
        super(FunctionBlackScholes, self).__init__()
        self.variant = variant
        # https://en.wikipedia.org/wiki/Black%E2%80%93Scholes_equation

    def get_x_0(self):
        if self.variant == 'american_put':
            return [-12]
        if self.variant == 'american_call':
            return [-12]
        else:
            raise RuntimeError()

    def compute(self, list_parameter, list_argument, instance):
        if self.variant == 'american_put':
            return self.compute_american_put(list_parameter, list_argument, instance)
        if self.variant == 'american_call':
            return self.compute_american_call(list_parameter, list_argument, instance)
        else:
            raise RuntimeError()


    def compute_american_put(self, list_parameter, list_argument, instance):
        #  T... expiration time
        #  S... stock price
        #  K... strike price
        #  n... height of the binomial tree
        deltaT = T / n
        up = exp(sigma * sqrt(deltaT))
        p0 = (up - exp(-r * deltaT)) / (up^2 - 1)
        p1 = exp(-r * deltaT) - p0
        #' initial values at time T
        for i in range(n):
            p[i] = K - S * up^(2*i - n)
            if p[i] < 0:
                p[i] = 0

        #' move to earlier times
        for j in range(n,-1, 0):
            for i in range(j):
                #' binomial value
                p[i] = p0 * p[i+1] + p1 * p[i]
                #' exercise value
                exercise = K - S * up^(2*i - j)
                if p[i] < exercise:
                    p[i] = exercise
            
        americanPut = p[0]
        return americanPut

    def compute_infinite_call(self, list_parameter, list_argument, instance):
        l2 = list_parameter[0]
        s = list_argument[0]
        K = s - (instance - s)
        # stike_mirrored = [ spot - (strike - spot) for strike in option_chain['list_strike']]
        return (k / (1 - l2)) * (((l2-1)/l2)**l2 ) * ((s/k)**l2)





# https://en.wikipedia.org/wiki/Binomial_options_pricing_model
#         function americanPut(T, S, K, r, sigma, q, n) 
# { 
#   '  T... expiration time
#   '  S... stock price
#   '  K... strike price
#   '  q... dividend yield
#   '  n... height of the binomial tree
#   deltaT := T / n;
#   up := exp(sigma * sqrt(deltaT));
#   p0 := (up*exp(-q * deltaT) - exp(-r * deltaT)) / (up^2 - 1);
#   p1 := exp(-r * deltaT) - p0;
#   ' initial values at time T
#   for i := 0 to n {
#       p[i] := K - S * up^(2*i - n);
#       if p[i] < 0 then p[i] := 0;
#   }
#   ' move to earlier times
#   for j := n-1 down to 0 {
#       for i := 0 to j {
#           ' binomial value
#           p[i] := p0 * p[i+1] + p1 * p[i];   
#           ' exercise value
#           exercise := K - S * up^(2*i - j);  
#           if p[i] < exercise then p[i] := exercise;
#       }
#   }
#   return americanPut := p[0];
# }