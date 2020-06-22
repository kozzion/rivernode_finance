
import sys
import os
import json
import requests
import time

import numpy as np
from scipy.optimize import minimize
from sklearn.metrics import mean_squared_error

class FunctionLogaritm(object):

    def __init__(self, name_model, name_parameter, variant='base'):
        super(FunctionLogaritm, self).__init__()

        self.variant = variant

    def list_name_parameter(self):
        if self.variant == 'base':
            return ['l2']
        
    def get_x_0(self, list_argument):
        if self.variant == 'base':
            return [-12]
        else:
            raise RuntimeError()

    def compute(self, list_parameter, arguments):
        array_timestamp = arguments['list_timestamp']
        return np.log(array_timestamp)
        
        #list_timestamp, list_value = ToolsOption.create_series(result_series_option_chain, name_model, name_parameter)

