import pandas as pd

from backtesting import Backtest, Strategy
from .strategies.crossover import SmaCross

data = pd.read_csv("ressources/testData/DD.csv")

columns = ['date', 'Volume', 'Open', 'High', 'Low', 'Close', 'adjclose']
data.columns = columns

bt = Backtest(data, SmaCross, commission=.002,
              exclusive_orders=True)
