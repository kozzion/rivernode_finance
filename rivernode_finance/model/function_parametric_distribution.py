
import sys
import os
import json
import requests
import time


from scipy.stats import norm
import numpy as np

# sys.path.append(os.path.abspath('../../rivernode_finance'))
from rivernode_finance.tools_model import ToolsModel

class FunctionParametricDistribution(object):

    def __init__(self, variant):
        super(FunctionParametricDistribution, self).__init__()
        self.variant = variant
        self.type = 'list'

    def is_model_put(self):
        if self.variant == 'normal_put':
            return True
        if self.variant == 'normal_call':
            return False
        else:
            raise RuntimeError()

    def list_name_parameter(self):
        return ['mu', 'sigma']

    def get_x_0(self, list_argument):
        if self.variant == 'normal_put':
            return [list_argument[0], list_argument[0]/15] #TODO do something with the distance to the future here
        if self.variant == 'normal_call':
            return [list_argument[0], list_argument[0]/15]
        else:
            raise RuntimeError()

    def compute(self, list_parameter, list_argument, list_instance):
        if self.variant == 'normal_put':
            return self.compute_normal_put(list_parameter, list_argument, list_instance)
        if self.variant == 'normal_call':
            return self.compute_normal_call(list_parameter, list_argument, list_instance)
        else:
            raise RuntimeError()


    def compute_normal_put(self, list_parameter, list_argument, list_instance):
        mu = list_parameter[0]
        sigma = list_parameter[1]
        array_strike = np.array(list_instance)
        # array_domain_cdf = np.array(list_instance) # here we can speed up A lot!!!
        array_domain_cdf = np.arange(int(mu * 0.5), int(mu * 1.5), mu/40) # here we can speed up A lot!!! 
        #TODO do something with the min strike here
        #TODO also make sure that the option prices are in here
        array_value_cdf = norm.cdf(array_domain_cdf, mu, sigma)
        return ToolsModel.array_price_put_for_cdf(array_domain_cdf, array_value_cdf, array_strike).tolist()

    def compute_normal_call(self, list_parameter, list_argument, list_instance):
        mu = list_parameter[0]
        sigma = list_parameter[1]


        array_strike = np.array(list_instance) 
        array_domain_cdf = np.arange(int(mu * 0.5), int(mu * 1.5), mu/40) # here we can speed up A lot!!! 
        #TODO do something with the min strike here
        #TODO also make sure that the option prices are in here
        array_value_cdf = norm.cdf(array_domain_cdf, mu, sigma)

        # plt.figure()
        # plt.plot(array_domain_cdf, array_value_cdf)
        # plt.show()
        return ToolsModel.array_price_call_for_cdf(array_domain_cdf, array_value_cdf, array_strike).tolist()


