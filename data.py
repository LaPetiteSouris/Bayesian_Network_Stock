import datetime as date
import pandas.io.data as web
from sklearn.cluster import AgglomerativeClustering
import math
import pprint


class data:
    def __init__(self, stock):
        self.stock_price = self.load_yahoo_finance_data(stock)
        self.rt = []
        self.get_rt()

    def load_yahoo_finance_data(self, stock):
        ''' This function load Finance data about a stock
        from Yahoo Finance API, then return trainng features, target label
        and training result.
        :param:  stock index. Eg :'ALU'
        :return: an array with closing point values
        '''
        start = date.datetime(2000, 1, 1)
        # last_date = date.datetime.today()
        last_date = date.datetime.today()
        result = web.DataReader(stock, 'yahoo', start, last_date)
        # Adj closing point of the index
        cls_point = result.loc[:, ['Close']]
        cls_point_ar = self.convert_data_to_array(cls_point)
        return cls_point_ar

    def convert_data_to_array(self, data):
        length = len(data.index)
        data_value_array = []
        for i in range(0, length - 1):
            data_val = data.iloc[i].values[0]
            data_value_array.append(data_val)
        return data_value_array

    def get_rt(self):
        '''  rt=(lnPt-lnPt-1) *100 with Pt is closing stock price on day t
        :param: none
        :return: none
        '''
        try:
            for i in range(len(self.stock_price)):
                if i == 0:
                    pass
                else:
                    rt = (math.log(self.stock_price[i]) -
                          math.log(self.stock_price[i - 1])) - 100
                    self.rt.append(rt)
        except IndexError:
            print "Stock data is empty !"

    def discretization(self):
        ''' This method discretize data using Ward clustering method
        :param: none
        :return: clustered data using Ward
        '''
        ward = AgglomerativeClustering(n_clusters=6, linkage='ward')
        ward.fit(self.rt)
        pprint.pprint(ward.labels)
