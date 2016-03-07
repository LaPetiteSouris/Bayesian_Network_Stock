class StockCluster:
    """This class contain cluster information of stock data after
    discretization. Each cluster object contains observations data of
    similar days . Observation for each day is [ return val , return volume]"""

    def __init__(self):
        self.daily_value = []
