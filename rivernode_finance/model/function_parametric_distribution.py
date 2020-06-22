
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

    def name_model(self):
        return self.variant

    def is_model_put(self):
        if self.variant == 'normal_put':
            return True
        if self.variant == 'normal_call':
            return False
        if self.variant == 'normalt_put':
            return True
        if self.variant == 'normalt_call':
            return False
        else:
            raise RuntimeError()

    def list_name_parameter(self):
        return ['pdf_mu', 'pdf_sd', 'pdf_df']

    def get_x_0(self, option_chain):
        if (option_chain['is_normalized']):
            return [0, 0.35, 5]
        else:
            raise RuntimeError()
            # if self.variant == 'normal_put':
            #     return [list_argument[0], list_argument[0]/15] #TODO do something with the distance to the future here
            # if self.variant == 'normal_call':
            #     return [list_argument[0], list_argument[0]/15]
            # else:
            #     raise RuntimeError()

    def compute(self, list_parameter, list_argument, list_instance):
        if self.variant == 'normal_put':
            return self.compute_normal_put(list_parameter, list_argument, list_instance)
        if self.variant == 'normal_call':
            return self.compute_normal_call(list_parameter, list_argument, list_instance)
        if self.variant == 'normal_put':
            return self.compute_normalt_put(list_parameter, list_argument, list_instance)
        if self.variant == 'normal_call':
            return self.compute_normalt_call(list_parameter, list_argument, list_instance)
        else:
            raise RuntimeError()


    def compute_normal_put(self, list_parameter, list_argument, list_instance):
        mu = list_parameter[0]
        sd = abs(list_parameter[1])
        array_strike = np.array(list_instance)
        # array_domain_cdf = np.array(list_instance) # here we can speed up A lot!!!
        resolution = 0.1
        domain_min = -0.2
        domain_max = 0.2
        array_domain_cdf = np.arange(domain_min, domain_max + resolution, resolution) #TO

        array_value_cdf = norm.cdf(array_domain_cdf, mu, sd)
        return ToolsModel.array_price_put_for_cdf(array_domain_cdf, array_value_cdf, array_strike).tolist()

    def compute_normal_call(self, list_parameter, list_argument, list_instance):
        mu = list_parameter[0]
        sd = abs(list_parameter[1])
        array_strike = np.array(list_instance)
        array_strike = np.array(list_instance) 
        # array_domain_cdf = np.array(list_instance) # here we can speed up A lot!!!
        resolution = 0.1
        domain_min = -0.2
        domain_max = 0.2
        array_domain_cdf = np.arange(domain_min, domain_max + resolution, resolution) #TO

        array_value_cdf = norm.cdf(array_domain_cdf, mu, sd)
        return ToolsModel.array_price_call_for_cdf(array_domain_cdf, array_value_cdf, array_strike).tolist()




    def compute_normalt_put(self, list_parameter, list_argument, list_instance):
        mu = list_parameter[0]
        sd = abs(list_parameter[1])
        array_strike = np.array(list_instance)
        # array_domain_cdf = np.array(list_instance) # here we can speed up A lot!!!
        resolution = 0.1
        domain_min = -0.2
        domain_max = 0.2
        array_domain_cdf = np.arange(domain_min, domain_max + resolution, resolution) #TO

        array_value_cdf = norm.cdf(array_domain_cdf, mu, sd)
        return ToolsModel.array_price_put_for_cdf(array_domain_cdf, array_value_cdf, array_strike).tolist()

    def compute_normalt_call(self, list_parameter, list_argument, list_instance):
        mu = list_parameter[0]
        sd = abs(list_parameter[1])
        array_strike = np.array(list_instance)
        array_strike = np.array(list_instance) 
        # array_domain_cdf = np.array(list_instance) # here we can speed up A lot!!!
        resolution = 0.1
        domain_min = -0.2
        domain_max = 0.2
        array_domain_cdf = np.arange(domain_min, domain_max + resolution, resolution) #TO

        array_value_cdf = norm.cdf(array_domain_cdf, mu, sd)
        return ToolsModel.array_price_call_for_cdf(array_domain_cdf, array_value_cdf, array_strike).tolist()