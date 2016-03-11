import numpy as np


class StockCluster:
    '''This class contain cluster information of stock data after
    discretization. Each cluster object contains observations data of
    similar days . Observation for each day is [ return val , return volume]
    :param: ward_cluster object, array of
     closing prices, array of volume, label(label of current object)
    '''

    def __init__(self, ward, closing_price, volume, label):
        self.daily_value = []
        self.ward_labels = ward.labels_
        self.data = np.zeros((self.ward_labels.shape[0], 2))
        self.closing_price = closing_price
        self.volume = volume
        self.label = label
        self.get_cluster()

    def get_cluster(self):
        ''' This function parse labels vector return from Ward object
        to get a StockCluster object, which stores observations belong
        to that cluster.
        :param: none
        :return: none
        '''
        for i in range(len(self.ward_labels)):
            if self.ward_labels[i] == self.label:
                self.data[i, 0] = self.closing_price[i]
                self.data[i, 1] = self.volume[i]
