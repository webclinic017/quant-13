import pandas as pd

from backtesting import Strategy
from ..indicators import SMA

def crossover(series1, series2):
    ##print(type(series1))
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
