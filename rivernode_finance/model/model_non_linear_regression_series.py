import sys
import os
import json
import requests
import time
import numpy as np

from scipy.optimize import minimize
from sklearn.metrics import mean_squared_error

class ModelNonLinearRegression(object):

    def __init__(self, function):
        super(ModelNonLinearRegression, self).__init__()
        self.function = function
        # self.x_0 = x_0

    def name_model(self):
        return self.function.name_model()

    def list_name_parameter(self):
        return ['error', 'cost'].extend(self.function.list_name_parameter())
    
    def fit(self, list_sd):
        list_strike = option_chain['list_strike']


        if self.function.is_model_put():
            list_value_bid = option_chain['list_put_bid']
            list_value_ask = option_chain['list_put_ask']
            cost = min(min(list_value_bid, list_value_ask))
            list_value_true = (np.array(list_value_bid) - cost).tolist()
        else:
            list_value_bid = option_chain['list_call_bid']
            list_value_ask = option_chain['list_call_ask']
            cost = min(min(list_value_bid, list_value_ask))
            list_value_true = (np.array(list_value_bid) - cost).tolist()    

        x0 = self.function.get_x_0(option_chain)
        list_argument = []
      

        args=(list_argument, list_strike, list_value_true)
        # train it

        maxfev = 1000
        if len(x0) == 1:
            initial_simplex = [
                [x0[0] * 1.1], 
                [x0[0] * 0.9]]
        elif len(x0) == 2:
            initial_simplex = [
                [x0[0] * 1.1, x0[1] * 0.9],
                [x0[0] * 0.9, x0[1] * 1.1],
                [x0[0] * 1.1 + 0.1, x0[1] * 1.1]]
        elif len(x0) == 3:
            initial_simplex = [
                [x0[0] * 1.1, x0[1] * 0.9, x0[2] * 0.9],
                [x0[0] * 0.9, x0[1] * 1.1, x0[2] * 0.9],
                [x0[0] * 0.9, x0[1] * 0.9, x0[2] * 1.1],
                [x0[0] * 1.1, x0[1] * 1.1, x0[2] * 1.1]]
        else:
            raise RuntimeError

        result_minimize = minimize(
            fun=self.compute_error,
            x0=x0,
            args=args,
            method='Nelder-Mead',
            options={
                'maxfev': maxfev, 
                'initial_simplex':initial_simplex})

        error = result_minimize['fun']
        list_parameter = result_minimize['x'].tolist()

        list_value_pred = self.function.compute(list_parameter, list_argument, list_strike)

        result_option_chain = {}
        result_option_chain['name_model'] = self.function.name_model()
        result_option_chain['name_modeled'] = 'list_put_bid'
        result_option_chain['list_value_pred'] = list_value_pred
        result_option_chain['dict_parameter'] = {}
        result_option_chain['dict_parameter']['error'] = error
        result_option_chain['dict_parameter']['cost'] = cost
        for list_name_parameter, value_parameter in zip(self.function.list_name_parameter(), list_parameter):
            result_option_chain['dict_parameter'][list_name_parameter] =  value_parameter
        return result_option_chain

    def compute_error(self, list_parameter, list_argument, list_instance, list_value_true):
        list_value_pred = self.function.compute(list_parameter, list_argument, list_instance)
        return mean_squared_error(list_value_true, list_value_pred)
    
