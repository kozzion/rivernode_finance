import sys
import os
import json
import requests
import time
import numpy as np

from scipy.stats import norm
from scipy.interpolate import interp1d
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

from rivernode_finance.tools_model import ToolsModel

class ModelDeconvolution(object):

    def __init__(self):
        super(ModelDeconvolution, self).__init__()

    def name_model(self):
        return 'deconvolution_put_0'

    def list_name_parameter(self):
        return ['error', 'cost', 'pdf_mu', 'pdf_sd', 'pdf_sk', 'pdf_ku']
    
    def fit(self, option_chain):
        list_strike = option_chain['list_strike']
        list_value_bid = option_chain['list_put_bid']
        list_value_ask = option_chain['list_put_ask']

        cost = min(min(list_value_bid, list_value_ask))
        array_value_true = np.array(list_value_bid) - cost
        array_pdf_domain, matrix_value_pdf, matrix_value_bas = self.build_matrix(list_strike)

        weights = np.linalg.lstsq(matrix_value_bas, array_value_true, rcond=None)[0]
        array_value_pred = np.dot(matrix_value_bas, weights) + cost
        array_pdf_pred = np.dot(matrix_value_pdf, weights) 
        array_pdf_pred = array_pdf_pred / np.sum(array_pdf_pred) # this is shit....

        result_option_chain = {}
        result_option_chain['name_model'] = 'deconvolution_put_0'
        result_option_chain['name_modeled'] = 'list_put_bid'
        result_option_chain['list_value_pred'] = array_value_pred.tolist()
        result_option_chain['list_pdf_domain'] = array_pdf_domain.tolist()
        result_option_chain['list_pdf_pred'] = array_pdf_pred.tolist()
        result_option_chain['dict_parameter'] = {}
        result_option_chain['dict_parameter']['error'] = mean_squared_error(array_value_true, array_value_pred)
        result_option_chain['dict_parameter']['cost'] = cost
        result_option_chain['dict_parameter']['pdf_mu'] = ToolsModel.compute_mu(array_pdf_domain, array_pdf_pred)
        result_option_chain['dict_parameter']['pdf_sd'] = 0 #ToolsModel.compute_sd(array_pdf_domain, array_pdf_pred)
        result_option_chain['dict_parameter']['pdf_sk'] = 0
        result_option_chain['dict_parameter']['pdf_ku'] = 0
        return result_option_chain


    def build_matrix(self, list_strike):
        resolution = 0.01
        domain_min = -0.2
        domain_max = 0.2
        pad = 20
        array_domain_pdf = np.arange(domain_min, domain_max + resolution, resolution) #TODO we would like an odd number here
        array_domain_val = np.arange(domain_min - (resolution * pad), domain_max + (resolution * (pad + 1)), resolution)
        array_value_val = ToolsModel.function_value_put(array_domain_val) 

        list_array_value_pdf = []
        list_array_value_bas = []
        list_mu = [-0.065, -0.045, -0.020, 0.00, 0.020, 0.045, 0.065]
        list_sd = [ 0.025,  0.020,  0.015, 0.01, 0.015, 0.020, 0.025]

        for mu, sd in zip(list_mu, list_sd):
            array_value_pdf = norm.pdf(array_domain_pdf, mu, sd) * resolution
            array_value_con = np.convolve(array_value_pdf, array_value_val, 'valid') 
            array_value_bas = interp1d(array_domain_pdf, array_value_con)(list_strike)
            list_array_value_pdf.append(array_value_pdf)
            list_array_value_bas.append(array_value_bas)

        # plt.figure()
        # for array_value_pdf in list_array_value_pdf:
        #     plt.plot(array_domain_pdf, array_value_pdf)
        # plt.show()
        # exit()

        matrix_value_pdf = np.stack(list_array_value_pdf, axis=0).transpose()
        matrix_value_bas = np.stack(list_array_value_bas, axis=0).transpose()
        return array_domain_pdf, matrix_value_pdf, matrix_value_bas


