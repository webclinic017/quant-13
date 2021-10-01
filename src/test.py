import pandas as pd

from backtesting import Backtest, Strategy
from .strategies.crossover import SmaCross
from .strategies.BuyOnEven import BuyOnEven

#Collect Data from CSV base on its Stock name
def datafromcsv(Stock):
    data = pd.read_csv("ressources/testData/"+ Stock + ".csv")
    columns = ['Date', 'Volume', 'Open', 'High', 'Low', 'Close', 'adjclose']
    data.columns = columns
    data = data.set_index("Date")
    data.index= pd.to_datetime(data.index)
    data = data.sort_index()
    return data


bt = Backtest(datafromcsv("AAPL"), BuyOnEven, commission=.002,
              exclusive_orders=True)