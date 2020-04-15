import sys
import os
import time
import matplotlib.pyplot as plt
import datetime
import pytz
import numpy as np

from scipy.stats import norm
from scipy.optimize import minimize
from sklearn.metrics import mean_squared_error

from rivernode_finance.model.model_non_linear_regression import ModelNonLinearRegression
from rivernode_finance.model.function_black_scholes import FunctionBlackScholes
from rivernode_finance.model.function_parametric_distribution import FunctionParametricDistribution
class ToolsOption(object):

    @staticmethod
    def analyse_series_option_chain(series_option_chain):
        spot = series_option_chain['spot']
        
        result_series_option_chain = {}
        result_series_option_chain['list_timestamp_expiry'] = []
        result_series_option_chain['list_str_date_expiry'] = []
        result_series_option_chain['dict_model'] = {}
        
        dict_model = {}
        dict_model['nlr_bs_inf_ls_put'] = ModelNonLinearRegression(FunctionBlackScholes('infinite_put'))
        dict_model['nlr_bs_inf_ls_call'] = ModelNonLinearRegression(FunctionBlackScholes('infinite_call'))
        dict_model['nlr_bs_inf_fs_put'] = ModelNonLinearRegression(FunctionBlackScholes('infinite_put_free_spot'))
        dict_model['nlr_bs_inf_fs_call'] = ModelNonLinearRegression(FunctionBlackScholes('infinite_call_free_spot'))
        dict_model['nlr_pd_normal_put'] = ModelNonLinearRegression(FunctionParametricDistribution('normal_put'))
        dict_model['nlr_pd_normal_call'] = ModelNonLinearRegression(FunctionParametricDistribution('normal_call'))

        for option_chain in list(series_option_chain['dict_option_chain'].values()): #TODO sort these or make sure they are sorted to begin with
            month = int(option_chain['expiryDate'].split('/')[0])
            day = int(option_chain['expiryDate'].split('/')[1])
            year = int(option_chain['expiryDate'].split('/')[2])
            timestamp_expiry = int(datetime.datetime(year, month, day, tzinfo=pytz.timezone('US/Eastern')).timestamp())
            str_date_expiry = option_chain['expiryDate']
            result_series_option_chain['list_timestamp_expiry'].append(timestamp_expiry)
            result_series_option_chain['list_str_date_expiry'].append(str_date_expiry)
            for name_model, model in dict_model.items():
                if not name_model in result_series_option_chain['dict_model']:
                    result_series_option_chain['dict_model'][name_model] = {}
                    result_series_option_chain['dict_model'][name_model]['error'] = []
                    for name_parameter in model.list_name_parameter():
                        result_series_option_chain['dict_model'][name_model][name_parameter] = []

                if model.is_model_put():
                    result_fit = model.fit([spot], option_chain['list_strike'], option_chain['list_put_bid'])
                else:
                    result_fit = model.fit([spot], option_chain['list_strike'], option_chain['list_call_bid'])


                result_series_option_chain['dict_model'][name_model]['error'].append(result_fit['error'])
                for index, name_parameter in enumerate(model.list_name_parameter()): 
                    result_series_option_chain['dict_model'][name_model][name_parameter].append(result_fit['list_parameter'][index])

            print('done')
            sys.stdout.flush()
        return result_series_option_chain
   

    # @staticmethod
    # def analyse_option_chain(spot, option_chain, list_model):
    #     option_chain_result = {}
    #     month = int(option_chain['expiryDate'].split('/')[0])
    #     day = int(option_chain['expiryDate'].split('/')[1])
    #     year = int(option_chain['expiryDate'].split('/')[2])
    #     option_chain_result['timestamp_expiry'] = int(datetime.datetime(year, month, day, tzinfo=pytz.timezone('US/Eastern')).timestamp())
    #     option_chain_result['str_date_expiry'] = option_chain['expiryDate']
        
        
    #     for model in list_model:




    #     result_fit_put = model_put.fit([spot], option_chain['list_strike'], option_chain['list_put_bid'])
    #     result_fit_call = model_call.fit([spot], option_chain['list_strike'], option_chain['list_call_bid'])
        
        
    #     option_chain_result['bs_inf_put_l2'] = result_fit_put['list_parameter'][0]
    #     option_chain_result['bs_inf_call_l2'] = result_fit_call['list_parameter'][0]
    #     option_chain_result['bs_inffs_put_l2'] = result_fit_put['list_parameter'][0]
    #     option_chain_result['bs_inffs_put_spot'] = result_fit_put['list_parameter'][1]
    #     option_chain_result['bs_inffs_call_l2'] = result_fit_call['list_parameter'][0]
    #     option_chain_result['bs_inffs_call_spot'] = result_fit_call['list_parameter'][1]



    #     result_fit_put = model_put.fit([spot], option_chain['list_strike'], option_chain['list_put_bid'])
    #     result_fit_call = model_call.fit([spot], option_chain['list_strike'], option_chain['list_call_bid'])

    #     result_fit_put = model_put.fit([spot], option_chain['list_strike'], option_chain['list_put_bid'])
    #     result_fit_call = model_call.fit([spot], option_chain['list_strike'], option_chain['list_call_bid'])
 
    #     option_chain_result['normal_put_spot'] = result_fit_put['list_parameter'][0]
    #     option_chain_result['normal_put_sigma'] = result_fit_put['list_parameter'][1]
    #     option_chain_result['normal_call_spot'] = result_fit_call['list_parameter'][0]
    #     option_chain_result['normal_call_sigma'] = result_fit_call['list_parameter'][1]


    #     plt.figure()
    #     plt.title(option_chain['expiryDate'])
    #     plt.plot(option_chain['list_strike'], option_chain['list_put_bid'])
    #     plt.plot(option_chain['list_strike'], option_chain['list_call_bid'])
    #     plt.plot(option_chain['list_strike'], result_fit_put['list_value_pred'])
    #     plt.plot(option_chain['list_strike'], result_fit_call['list_value_pred'])
    #     plt.legend(['put bid', 'call bid', 'fit_bid', 'fit_call'])
    #     plt.show()

    #     return option_chain_result

    @staticmethod
    def plot(list_result_option_chain, list_parameter):
        print(len(list_result_option_chain))
        print(len(list_parameter))


   
        list_name_parameter = []
        plt.figure()
        for parameter in list_parameter:
            name_model = parameter[0]
            name_parameter = parameter[1]
            list_name_parameter.append(name_model + ' ' + name_parameter)
            list_value = list_result_option_chain['dict_model'][name_model][name_parameter]
            print(len(list_value))
            print(len(list_result_option_chain['list_timestamp_expiry']))
            plt.plot(list_result_option_chain['list_timestamp_expiry'], list_value)
        plt.xticks(list_result_option_chain['list_timestamp_expiry'], list_result_option_chain['list_str_date_expiry'], rotation='vertical')
        plt.legend(list_parameter)
        plt.show()




    @staticmethod
    def option_price_test(option_chain):

        mu = 370
        sd = 30

        array_strike = np.array(option_chain['list_strike']) #TODO make sure every strike is in the domain
        array_domain_cdf = np.arange(270, 470, 1)


        array_value_cdf = norm.cdf(array_domain_cdf, mu, sd)

        # plt.figure()
        # plt.plot(array_domain_cdf, array_value_cdf)
        # plt.show()
        array_price_put = ToolsOption.array_price_put_for_cdf(array_domain_cdf, array_value_cdf, array_strike)
        array_price_call = ToolsOption.array_price_call_for_cdf(array_domain_cdf, array_value_cdf, array_strike)
        plt.figure()
        plt.plot(array_strike, array_price_put)
        plt.plot(array_strike, array_price_call)
        plt.plot(option_chain['list_strike'], option_chain['list_put_ask'])
        plt.plot(option_chain['list_strike'], option_chain['list_call_ask'])

        plt.legend(['put', 'call', 'model_put', 'model_call'])
        plt.show()

    @staticmethod
    def option_model_test_2(option_chain):

        spot = 370
        model_put = ModelNonLinearRegression(FunctionParametricDistribution('normal_put'))
        result_fit_put_bid = model_put.fit([spot], option_chain['list_strike'], option_chain['list_put_bid'])
        result_fit_put_ask = model_put.fit([spot], option_chain['list_strike'], option_chain['list_put_ask'])
        model_call = ModelNonLinearRegression(FunctionParametricDistribution('normal_call'))
        result_fit_call_bid = model_call.fit([spot], option_chain['list_strike'], option_chain['list_call_bid'])
        result_fit_call_ask = model_call.fit([spot], option_chain['list_strike'], option_chain['list_call_ask'])


        print(result_fit_put_bid['list_parameter'])
        print(result_fit_put_ask['list_parameter'])
        print(result_fit_call_bid['list_parameter'])
        print(result_fit_call_ask['list_parameter'])

        plt.figure()
        plt.plot(option_chain['list_strike'], option_chain['list_put_bid'])
        plt.plot(option_chain['list_strike'], option_chain['list_put_ask'])
        plt.plot(option_chain['list_strike'], option_chain['list_call_bid'])
        plt.plot(option_chain['list_strike'], option_chain['list_call_ask'])
        plt.plot(option_chain['list_strike'], result_fit_put_bid['list_value_pred'])
        plt.plot(option_chain['list_strike'], result_fit_put_ask['list_value_pred'])
        plt.plot(option_chain['list_strike'], result_fit_call_bid['list_value_pred'])
        plt.plot(option_chain['list_strike'], result_fit_call_ask['list_value_pred'])

        plt.legend(['put_bid', 'put_ask', 'call_bid', 'call_ask', 'fit_put_bid', 'fit_put_ask', 'fit_call_bid', 'fit_call_ask'])
        plt.show()





