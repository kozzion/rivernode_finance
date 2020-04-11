import sys
import os
import json
import requests
import time

from scipy.optimize import minimize
from sklearn.metrics import mean_squared_error

class ModelFitList(object):

    def __init__(self, function):
        super(ModelFitList, self).__init__()
        self.function = function
        # self.x_0 = x_0

    
    def fit(self, list_argument, list_instance, list_value_true):
        
        x0 = self.function.get_x_0(list_argument)
        args=(self, list_argument, list_instance, list_value_true)
        # train it

        maxfev = 1000
        if len(x0) == 1:
            initial_simplex = [
                [x0[0] * 0.9], 
                [x0[0] * 1.1]]
        elif len(x0) == 2:
            initial_simplex = [
                [x0[0] * 0.9, x0[1] * 1.1], 
                [x0[0] * 1.1, x0[1] * 0.9],
                [x0[0] * 1.1, x0[1] * 1.1]]
        else:
            raise RuntimeError

        result_minimize = minimize(
            fun=ModelFitList.compute_error,
            x0=x0,
            args=args,
            method='Nelder-Mead',
            options={
                'maxfev': maxfev, 
                'initial_simplex':initial_simplex})

        result_fit = {}
        result_fit['error'] = result_minimize['fun']
        result_fit['list_parameter'] = result_minimize['x'].tolist()
        result_fit['list_value_pred'] = self.compute_list(result_fit['list_parameter'], list_argument, list_instance)
        return result_fit

    def predict(self):
        pass

    @staticmethod
    def compute_error(list_parameter, model, list_argument, list_instance, list_value_true):
        list_value_pred = model.compute_list(list_parameter, list_argument, list_instance)
        return mean_squared_error(list_value_true, list_value_pred)
    
    def compute_list(self, list_parameter, list_argument, list_instance):
        return [self.function.compute(list_parameter, list_argument, instance) for instance in list_instance]
