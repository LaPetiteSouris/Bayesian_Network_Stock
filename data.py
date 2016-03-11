import datetime as date
import pandas.io.data as web
from sklearn.cluster import AgglomerativeClustering
import math
import numpy as np
from stockcluster import StockCluster


class Data:
    """ Data class, which contains all stock data neccessary for
    Bayes network
    :param: stock index. For example, by default is ALU-Alcatel Lucent
    Attributes :
                 volume      Historical sale volume
                 stock_price Historical closing value
                 rt          stock return value  rt=(ln(Pt)-ln(Pt-1)) *100.
                             Pt is historical closing value on day t
                 vt          volume return value  rt=(ln(Vt)-ln(Vt-1)) *100.
                             Vt is historical volume on day t
                 cluster_objects_vectors  vector containing
                  cluster object discrizied from raw stock value

    """

    def __init__(self, stock='ALU'):
        self.rt = []
        self.vt = []
        self.volume = []
        self.stock_price = []
        self.cluster_objects_vectors = []
        self.load_yahoo_finance_data(stock)
        self.get_raw_return_value()
        self.discretization()

    def load_yahoo_finance_data(self, stock):
        ''' This function load Finance data about a stock
        from Yahoo Finance API, then return trainng features, target label
        and training result.
        :param:  stock index. Eg :'ALU'
        :return: None
        '''
        start = date.datetime(2000, 1, 1)
        # last_date = date.datetime.today()
        last_date = date.datetime.today()
        result = web.DataReader(stock, 'yahoo', start, last_date)
        # Adj closing point of the index
        cls_point = result.loc[:, ['Close']]
        vol = result.loc[:, ['Volume']]
        self.volume = self.convert_data_to_array(vol)
        self.stock_price = self.convert_data_to_array(cls_point)

    def convert_data_to_array(self, data):
        length = len(data.index)
        data_value_array = []
        for i in range(0, length - 1):
            data_val = data.iloc[i].values[0]
            data_value_array.append(data_val)
        return data_value_array

    def get_raw_return_value(self):
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
                    vt = (math.log(self.volume[i]) -
                          math.log(self.volume[i - 1])) - 100
                    self.rt.append(rt)
                    self.vt.append(vt)
        except IndexError:
            print "Stock data is empty !"

    def discretization(self):
        ''' This method discretize data using Ward clustering method
        :param: none
        :return: clustered data using Ward
        '''
        print "Start discretization"
        ward = self.ward_clustering()
        for i in range(6):
            clus = StockCluster(ward, self.rt, self.vt, i)
            self.cluster_objects_vectors.append(clus)

    def ward_clustering(self):
        ''' This method clustering data using Ward clustering method
        :param: none
        :return: clustered data using Ward
        '''
        ward = AgglomerativeClustering(n_clusters=6, linkage='ward')
        # data matrix, each line is observation of 1 day
        # columns are features : return value| return closing volume
        data_to_be_clustered = np.array([self.rt, self.vt])
        data_to_be_clustered = np.transpose(data_to_be_clustered)
        ward.fit(data_to_be_clustered)
        return ward
