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
from rivernode_finance.model.model_deconvolution import ModelDeconvolution
from rivernode_finance.model.function_black_scholes import FunctionBlackScholes
from rivernode_finance.model.function_parametric_distribution import FunctionParametricDistribution

class ToolsOption(object):

   

    @staticmethod
    def analyse_option_chain(option_chain):
        dict_result_option_chain = {}
        list_model = []
        list_model.append(ModelDeconvolution())
        list_model.append(ModelNonLinearRegression(FunctionParametricDistribution('normal_put')))
        list_model.append(ModelNonLinearRegression(FunctionParametricDistribution('normal_call')))
        for model in list_model:
            dict_result_option_chain[model.name_model()] = model.fit(option_chain)
        return dict_result_option_chain

    @staticmethod
    def create_series(result_series_option_chain, name_model, name_parameter):
        list_timestamp = result_series_option_chain['list_timestamp_expiry']
        list_value = []
        for dict_result_option_chain in result_series_option_chain['list_dict_result_option_chain']:
            list_value.append(dict_result_option_chain[name_model]['dict_parameter'][name_parameter])
        list_timestamp = ((np.array(list_timestamp) - list_timestamp[0]) / (3600 * 24)).tolist()
        return list_timestamp, list_value

    @staticmethod
    def analyse_series_option_chain_deconv(series_option_chain):
        result_series_option_chain = {}
        result_series_option_chain['symbol'] = series_option_chain['symbol']
        result_series_option_chain['list_timestamp_expiry'] = []
        result_series_option_chain['list_dict_result_option_chain'] = []

        for option_chain in series_option_chain['list_option_chain']:
            dict_result_option_chain = ToolsOption.analyse_option_chain(option_chain)
            result_series_option_chain['list_dict_result_option_chain'].append(dict_result_option_chain)
            result_series_option_chain['list_timestamp_expiry'].append(option_chain['timestamp_expiry'])

        # list_timestamp, list_value = ToolsOption.create_series(series_option_chain, result_series_option_chain, 'deconvolution_put_0', 'error')
        # plt.figure()        
        # plt.plot(list_timestamp, list_value)
        # plt.legend(['deconvolution_put_0'])
        # plt.show()
        return result_series_option_chain

    @staticmethod
    def analyse_series_option_chain(series_option_chain):
        spot = series_option_chain['spot']
        
        result_series_option_chain = {}
        result_series_option_chain['symbol'] = series_option_chain['symbol']
        result_series_option_chain['list_timestamp_expiry'] = []
        result_series_option_chain['list_str_date_expiry'] = []
        result_series_option_chain['list_list_stike'] = []
        result_series_option_chain['list_list_put_bid'] = []
        result_series_option_chain['list_list_call_bid']= []

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
            result_series_option_chain['list_list_stike'].append(option_chain['list_strike'])
            result_series_option_chain['list_list_put_bid'].append(option_chain['list_put_bid'])
            result_series_option_chain['list_list_call_bid'].append(option_chain['list_call_bid'])
            for name_model, model in dict_model.items():
                if not name_model in result_series_option_chain['dict_model']:
                    result_series_option_chain['dict_model'][name_model] = {}
                    result_series_option_chain['dict_model'][name_model]['list_error'] = []
                    result_series_option_chain['dict_model'][name_model]['list_list_value_pred'] = []
                    for name_parameter in model.list_name_parameter():
                        result_series_option_chain['dict_model'][name_model][name_parameter] = []

                if model.is_model_put():
                    result_fit = model.fit([spot], option_chain['list_strike'], option_chain['list_put_bid'])
                else:
                    result_fit = model.fit([spot], option_chain['list_strike'], option_chain['list_call_bid'])

            
                result_series_option_chain['dict_model'][name_model]['list_list_value_pred'].append(result_fit['list_value_pred'])

                result_series_option_chain['dict_model'][name_model]['list_error'].append(result_fit['error'])
                for index, name_parameter in enumerate(model.list_name_parameter()): 
                    result_series_option_chain['dict_model'][name_model][name_parameter].append(result_fit['list_parameter'][index])

            print('done')
            sys.stdout.flush()
        return result_series_option_chain
   
    @staticmethod
    def pick_option_value_put(result_series_option_chain):
        name_model = 'nlr_pd_normal_put'
        list_list_stike = result_series_option_chain['list_list_stike']
        list_timestamp_expiry = result_series_option_chain['list_str_date_expiry']
        list_list_value_true = result_series_option_chain['list_list_put_bid']
        list_error = result_series_option_chain['dict_model'][name_model]['list_error']
        list_list_value_pred = result_series_option_chain['dict_model'][name_model]['list_list_value_pred']
        
        for timestamp_expiry, error, list_stike, list_value_true, list_value_pred in zip(list_timestamp_expiry, list_error, list_list_stike, list_list_value_true, list_list_value_pred):
            print(timestamp_expiry)
            print('error: ' + str(round(error, 2)))
            for stike, value_true, value_pred in zip(list_stike, list_value_true, list_value_pred):
                ratio = value_pred/value_true
                print(str(stike) + ' ratio: ' + str(round(ratio, 2)))

    @staticmethod
    def pick_option_value_call(result_series_option_chain):
        name_model = 'nlr_pd_normal_call'
        list_list_stike = result_series_option_chain['list_list_stike']
        list_timestamp_expiry = result_series_option_chain['list_str_date_expiry']
        list_error = result_series_option_chain['list_error']
        list_list_value_true = result_series_option_chain['list_list_call_bid']
        list_list_value_pred = result_series_option_chain['dict_model'][name_model]['list_list_value_pred']
        
        for timestamp_expiry, error, list_stike, list_value_true, list_value_pred in zip(list_timestamp_expiry, list_error, list_list_stike, list_list_value_true, list_list_value_pred):
            print(timestamp_expiry)
            print('error: ' + str(round(error, 2)))
            for stike, value_true, value_pred in zip(list_stike, list_value_true, list_value_pred):
                ratio = value_pred/value_true
                print(str(stike) + ' ratio: ' + str(round(ratio, 2)))

  
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
    def plot_analyse_result(result_series_option_chain, list_name_model, list_name_parameter):        
        fig, tuple_axes = plt.subplots(1, len(list_name_parameter))
        for index, name_parameter in enumerate(list_name_parameter):   
            axes = tuple_axes[index]
            for name_model in list_name_model:
                list_timestamp, list_value = ToolsOption.create_series(result_series_option_chain, name_model, name_parameter)
                axes.plot(list_timestamp, list_value)
            axes.set_title(name_parameter)
            axes.legend(list_name_model)
        plt.show()

    @staticmethod
    def plot_compare_result(list_result_series_option_chain, list_tuple_model_parameter):
        plot_count = len(list_tuple_model_parameter)
        fig, tuple_axes = plt.subplots(1, plot_count)
        for index, (name_model, name_parameter) in enumerate(list_tuple_model_parameter):
            axes = tuple_axes[index]
            list_name_symbol = []
            for result_series_option_chain in list_result_series_option_chain:
                list_name_symbol.append(result_series_option_chain['symbol'])
                list_timestamp, list_value = ToolsOption.create_series(result_series_option_chain, name_model, name_parameter)
                axes.plot(list_timestamp, list_value)
            axes.set_title(name_model + ' ' + name_parameter)
            axes.legend(list_name_symbol)
        plt.show()

    @staticmethod
    def compare(list_option_chain):

        list_label = []
        for option_chain in list_option_chain:
            list_label.append(option_chain['symbol'])
        fig, ((axes_0, axes_1), (axes_2, axes_3)) = plt.subplots(2, 2, sharex='all', sharey='all')

        for option_chain in list_option_chain:
            axes_0.plot(option_chain['list_strike'], option_chain['list_call_bid'])
        axes_0.legend(list_label)
        axes_0.set_title('Call bid')
        
        for option_chain in list_option_chain:
            axes_1.plot(option_chain['list_strike'], option_chain['list_put_bid'])
        axes_1.legend(list_label)
        axes_1.set_title('Put bid')

        for option_chain in list_option_chain:
            axes_2.plot(option_chain['list_strike'], option_chain['list_call_ask'])
        axes_2.legend(list_label)
        axes_2.set_title('Call ask')

        for option_chain in list_option_chain:
            axes_3.plot(option_chain['list_strike'], option_chain['list_put_ask'])
        axes_3.legend(list_label)
        axes_3.set_title('Put ask')

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





