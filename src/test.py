import numpy as np
import pandas as pd

class Trader:
    def __init__(self, dataID):
        self.dataID = dataID
        self.data = pd.read_csv(self.dataID)
def run():
    trader = Trader("ressources/testData/DD.csv")
    print(trader.data)
    print(trader.data.columns)
    return trader