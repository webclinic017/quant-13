import pandas as pd
import os

from backtesting import Backtest, Strategy
from .strategies.crossover import SmaCross
from .strategies.BuyOnEven import BuyOnEven

html_dir = "html"

#Collect Data from CSV base on its Stock name
def datafromcsv(Stock):
    data = pd.read_csv("ressources/testData/"+ Stock + ".csv")
    columns = ['Date', 'Volume', 'Open', 'High', 'Low', 'Close', 'adjclose']
    data.columns = columns
    data = data.set_index("Date")
    data.index= pd.to_datetime(data.index)
    data = data.sort_index()
    return data

def run(strategy=SmaCross, strategy_str="SmaCross"):
    bt = Backtest(datafromcsv("AAPL"), strategy, commission=.002,
                exclusive_orders=True)
    stats = bt.run()

    if not os.path.exists(html_dir):
        os.mkdir(html_dir)

    bt.plot(filename='./' + html_dir + '/' + strategy_str)