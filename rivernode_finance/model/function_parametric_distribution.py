
import sys
import os
import json
import requests
import time

from scipy.optimize import minimize
from scipy.stats import norm
from sklearn.metrics import mean_squared_error

class FunctionParametricDistribution(object):

    def __init__(self, variant):
        super(FunctionParametricDistribution, self).__init__()
        self.variant = variant

    def get_x_0(self, list_argument):
        if self.variant == 'normal_put':
            return [list_argument[0], 10]
        else:
            raise RuntimeError()

    def compute(self, list_parameter, list_argument, instance):
        if self.variant == 'normal_put':
            return self.compute_normal_put(list_parameter, list_argument, instance)
        else:
            raise RuntimeError()


    def compute_normal_put(self, list_parameter, list_argument, instance):
        mu = list_parameter[0]
        sigma = list_parameter[1]
        # spot = list_argument[0]
        list_strike = list_argument[1]
        
        v_total = 0
        for index in range(1, len(list_strike)):
            p_segment = norm.cdf(list_strike[index], mu, sigma) - norm.cdf(list_strike[index -1], mu, sigma)
            s_segment = (list_strike[index] - list_strike[index -1]) / 2.0
            v_segment = max(s_segment - instance, 0) * p_segment
            v_total += v_segment 
        return v_total

