import pandas as pd

from backtesting import Backtest, Strategy
# from backtesting.lib import crossover

##from backtesting.test import SMA

data = pd.read_csv("ressources/testData/DD.csv")

columns = ['date', 'Volume', 'Open', 'High', 'Low', 'Close', 'adjclose']
data.columns = columns

print(data.columns)

def SMA(data, n):
    return pd.Series(data).rolling(n).mean()

def crossover(series1, series2):
    print(type(series1))
    series1 = (
        series1.values if isinstance(series1, pd.Series) else
        (series1, series1) if isinstance(series1, (int, float, complex)) and not isinstance(series1, bool) else
        series1)
    series2 = (
        series2.values if isinstance(series2, pd.Series) else
        (series2, series2) if isinstance(series1, (int, float, complex)) and not isinstance(series1, bool) else
        series2)
    try:
        return series1[-2] < series2[-2] and series1[-1] > series2[-1]
    except IndexError:
        return False


class SmaCross(Strategy):
    def init(self):
        price = self.data.Close
        self.ma1 = self.I(SMA, price, 10)
        self.ma2 = self.I(SMA, price, 20)

    def next(self):
        if crossover(self.ma1, self.ma2):
            self.position.close()
            self.buy()
        elif crossover(self.ma2, self.ma1):
            self.position.close()
            self.sell()


bt = Backtest(data, SmaCross, commission=.002,
              exclusive_orders=True)
stats = bt.run()
bt.plot()

def run():
    print("Successfull")

# import numpy as np
# import pandas as pd

# class Trader:
#     def __init__(self, dataID):
#         self.dataID = dataID
#         self.data = pd.read_csv(self.dataID)
# def run():
#     trader = Trader("ressources/testData/DD.csv")
#     print(trader.data)
#     print(trader.data.columns)
#     return trader