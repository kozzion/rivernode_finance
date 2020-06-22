import sys
import os
import numpy as np

class ToolsModel(object):



    @staticmethod 
    def compute_mu(array_domain, array_pdf):
        return np.dot(array_domain, array_pdf)

    @staticmethod 
    def compute_sd(array_domain, array_pdf):
        #TODO this is broken
        mu = ToolsModel.compute_mu(array_domain, array_pdf)
        #print( len(array_pdf + 1))
        array_pdf = array_pdf / np.sum(array_pdf)
        result = np.sqrt(np.dot(np.square(array_domain - mu), array_pdf))
        return result

    @staticmethod 
    def function_value_put(array_domain):
        array_price_put = np.zeros(array_domain.shape)
        array_price_put[0 < array_domain] = array_domain[0 < array_domain]
        return array_price_put

    @staticmethod
    def array_price_put_for_cdf(array_domain_cdf, array_value_cdf, array_strike):
        array_price_put = np.zeros(array_strike.shape)
        # plot
        for index, strike in enumerate(array_strike):
            array_price_put[index] = ToolsModel.price_put_for_cdf(array_domain_cdf, array_value_cdf, strike)
        return array_price_put
        
    @staticmethod
    def array_price_call_for_cdf(array_domain_cdf, array_value_cdf, array_strike):
        array_price_put = np.zeros(array_strike.shape)
        # plot
        for index, strike in enumerate(array_strike):
            array_price_put[index] = ToolsModel.price_put_for_call(array_domain_cdf, array_value_cdf, strike)
        return array_price_put

    @staticmethod
    def price_put_for_cdf(array_domain_cdf, array_value_cdf, strike):
        e_total = 0

        for index in range(1, len(array_domain_cdf)):
            p_segment = array_value_cdf[index] - array_value_cdf[index - 1]
            s_segment = (array_domain_cdf[index] + array_domain_cdf[index -1]) / 2.0
            e_segment = max(strike - s_segment, 0) * p_segment
            e_total += e_segment 
        return e_total

    @staticmethod
    def price_put_for_call(array_domain_cdf, array_value_cdf, strike):
        e_total = 0
        for index in range(1, len(array_domain_cdf)):
            p_segment = array_value_cdf[index] - array_value_cdf[index - 1]
            s_segment = (array_domain_cdf[index] + array_domain_cdf[index -1]) / 2.0
            e_segment = max(s_segment - strike, 0) * p_segment
            e_total += e_segment 
        return e_total

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