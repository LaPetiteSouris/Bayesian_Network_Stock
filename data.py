import datetime as date
import pandas.io.data as web


class data:
    def __init__(self, stock):
        self.stock_price = self.load_yahoo_finance_data(stock)

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
        return cls_point

    def discretization(self):
        ''' This method discretize data using Ward clustering method
        :param: none
        :return: clustered data using Ward
        '''
