
import sys
import os
import json
import requests
import time

import numpy as np
from scipy.optimize import minimize
from sklearn.metrics import mean_squared_error

class FunctionBlackScholes(object):

    def __init__(self, variant):
        super(FunctionBlackScholes, self).__init__()
        self.variant = variant
        self.type = 'single'
        # https://en.wikipedia.org/wiki/Black%E2%80%93Scholes_model


    def is_model_put(self):
        if self.variant == 'infinite_put':
            return True
        elif self.variant == 'infinite_call':
            return False
        elif self.variant == 'infinite_put_free_spot':
            return True
        elif self.variant == 'infinite_call_free_spot':
            return False
        else:
            raise RuntimeError()

    def list_name_parameter(self):
        if self.variant == 'infinite_put':
            return ['l2']
        elif self.variant == 'infinite_call':
            return ['l2']
        elif self.variant == 'infinite_put_free_spot':
            return ['l2','spot']
        elif self.variant == 'infinite_call_free_spot':
            return ['l2','spot']
        else:
            raise RuntimeError()
        
    def get_x_0(self, list_argument):
        if self.variant == 'infinite_put':
            return [-12]
        elif self.variant == 'infinite_call':
            return [-12]
        elif self.variant == 'infinite_put_free_spot':
            return [-12, list_argument[0]]
        elif self.variant == 'infinite_call_free_spot':
            return [-12, list_argument[0]]
        else:
            raise RuntimeError()

    def compute(self, list_parameter, list_argument, instance):
        if self.variant == 'infinite_put':
            return self.compute_infinite_put(list_parameter, list_argument, instance)
        elif self.variant == 'infinite_call':
            return self.compute_infinite_call(list_parameter, list_argument, instance)
        elif self.variant == 'infinite_put_free_spot':
            return self.compute_infinite_put_free_spot(list_parameter, list_argument, instance)
        elif self.variant == 'infinite_call_free_spot':
            return self.compute_infinite_call_free_spot(list_parameter, list_argument, instance)
        else:
            raise RuntimeError()


    def compute_infinite_put(self, list_parameter, list_argument, instance):
        l2 = list_parameter[0]
        S = list_argument[0]
        K = instance
        return (K / (1 - l2)) * (((l2-1)/l2)**l2 ) * ((S/K)**l2)


    def compute_infinite_call(self, list_parameter, list_argument, instance):
        l2 = list_parameter[0]
        S = list_argument[0]
        K = instance
        K = S - (K - S)
        return (K / (1 - l2)) * (((l2-1)/l2)**l2 ) * ((S/K)**l2)



    def compute_infinite_put_free_spot(self, list_parameter, list_argument, instance):
        l2 = list_parameter[0]
        S = list_parameter[1]
        K = instance
        if ((l2-1)/l2) < 0:
            return 999999 # if it goes complex fuck it all up
        return (K / (1 - l2)) * (((l2-1)/l2)**l2 ) * ((S/K)**l2)


    def compute_infinite_call_free_spot(self, list_parameter, list_argument, instance):
        l2 = list_parameter[0]
        S = list_parameter[1]
        K = instance
        K = S - (K - S)
        if ((l2-1)/l2) < 0:
            return 999999 # if it goes complex fuck it all up

        return (K / (1 - l2)) * (((l2-1)/l2)**l2 ) * ((S/K)**l2)
