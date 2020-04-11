import sys
import os
import time
import matplotlib.pyplot as plt

from scipy.optimize import minimize
from sklearn.metrics import mean_squared_error

from rivernode_finance.model.model_fit_list import ModelFitList
from rivernode_finance.model.function_black_scholes import FunctionBlackScholes
class ToolsOption(object):

    @staticmethod
    def analyse_response_option_chain(response_option_chain):
        spot = response_option_chain['spot']
        option_chain = list(response_option_chain['dict_option_chain'].values())[0]
        ToolsOption.analyse_option_chain(spot, option_chain)


    @staticmethod
    def analyse_option_chain(spot, option_chain):

        model_put = ModelFitList(FunctionBlackScholes('infinite_put'))
        model_call = ModelFitList(FunctionBlackScholes('infinite_call'))
        result_fit_put = model_put.fit([spot], option_chain['list_strike'], option_chain['list_put_bid'])
        result_fit_call = model_call.fit([spot], option_chain['list_strike'], option_chain['list_call_bid'])
        print(result_fit_put['list_parameter'][0])
        print(result_fit_call['list_parameter'][0])
        
        plt.figure()
        plt.title(option_chain['expiryDate'])
        plt.plot(option_chain['list_strike'], option_chain['list_put_bid'])
        plt.plot(option_chain['list_strike'], option_chain['list_call_bid'])
        plt.plot(option_chain['list_strike'], result_fit_put['list_value_pred'])
        plt.plot(option_chain['list_strike'], result_fit_call['list_value_pred'])
        plt.legend(['put bid', 'call bid', 'fit_bid', 'fit_call'])
        plt.show()

        model_put = ModelFitList(FunctionBlackScholes('infinite_put_free_spot'))
        model_call = ModelFitList(FunctionBlackScholes('infinite_call_free_spot'))
        result_fit_put = model_put.fit([spot], option_chain['list_strike'], option_chain['list_put_bid'])
        result_fit_call = model_call.fit([spot], option_chain['list_strike'], option_chain['list_call_bid'])
        print(result_fit_put['list_parameter'])
        print(result_fit_call['list_parameter'])
        
        plt.figure()
        plt.title(option_chain['expiryDate'])
        plt.plot(option_chain['list_strike'], option_chain['list_put_bid'])
        plt.plot(option_chain['list_strike'], option_chain['list_call_bid'])
        plt.plot(option_chain['list_strike'], result_fit_put['list_value_pred'])
        plt.plot(option_chain['list_strike'], result_fit_call['list_value_pred'])
        plt.legend(['put bid', 'call bid', 'fit_bid', 'fit_call'])
        plt.show()



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