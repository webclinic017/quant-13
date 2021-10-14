import pandas as pd
import numpy as np
from backtesting import Strategy


def isModuloZero(data, mod):
    isModArray = [index % mod == 0 for index,ele in enumerate(data)]
    
    return pd.Series(isModArray)

class BuyOnEven(Strategy):
    n = 141
    def init(self):
        self.ind= self.I(isModuloZero,self.data.index, self.n)
    def next(self):
        if True:
            ## only buy on even days
            if np.floor(self.data.index.day[0]) % 2 == 0:
                self.buy()
            else:
                self.sell()
        
        