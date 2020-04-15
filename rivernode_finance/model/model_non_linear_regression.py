import sys
import os
import json
import requests
import time

from scipy.optimize import minimize
from sklearn.metrics import mean_squared_error

class ModelNonLinearRegression(object):

    def __init__(self, function):
        super(ModelNonLinearRegression, self).__init__()
        self.function = function
        # self.x_0 = x_0


    def is_model_put(self):
        return self.function.is_model_put()

    def list_name_parameter(self):
        return self.function.list_name_parameter()
    
    def fit(self, list_argument, list_instance, list_value_true):
        
        x0 = self.function.get_x_0(list_argument)
        args=(list_argument, list_instance, list_value_true)
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
                [x0[0] * 1.1, x0[1] * 1.1]]
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

        result_fit = {}
        result_fit['error'] = result_minimize['fun']
        result_fit['list_parameter'] = result_minimize['x'].tolist()

        if self.function.type == 'single':
            result_fit['list_value_pred'] = [self.function.compute(result_fit['list_parameter'], list_argument, instance) for instance in list_instance]
        elif self.function.type == 'list':
            result_fit['list_value_pred'] = self.function.compute(result_fit['list_parameter'], list_argument, list_instance)
        else:          
            raise RuntimeError(self.function.type)    
        return result_fit

    def compute_error(self, list_parameter, list_argument, list_instance, list_value_true):
        if self.function.type == 'single':
            list_value_pred = [self.function.compute(list_parameter, list_argument, instance) for instance in list_instance]
        elif self.function.type == 'list':
            list_value_pred = self.function.compute(list_parameter, list_argument, list_instance)
        else:          
            raise RuntimeError(self.function.type)    
        return mean_squared_error(list_value_true, list_value_pred)
    
