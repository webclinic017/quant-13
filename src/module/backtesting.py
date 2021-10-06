import numpy as np
import pandas as pd

from datetime import date

from ..indicators import moving_average

class Strategy:
    def __init__(self, data=None, cash=None):
        self.data = data
        self.cash = cash
        self.indicators = dict()
        self.position = Position()
        self.order = None

        # self.init()

    def I(self, indicator_function, data, *args, **kwargs):
        indicator_data = indicator_function(data, *args, **kwargs)
        return indicator_data
    
    def init(self):
        pass

    def next(self):
        pass

    def get_order(self):
        self.order = None
        self.init()
        self.next()
        return self.order

    def sell(self):
        self.order = 'sell'

    def buy(self):
        self.order = 'buy'

class Position:
    """
    Only buy and close state for the moment.
    """
    def __init__(self, position_type='cash', position_value=0):
        self.type = position_type # long,short, cash
        self.value = 0
    def close(self):
        if self.type == 'buy':
            self.type = 'sell'
        if self.type == 'sell':
            self.type = 'buy'

class Backtest:
    def __init__(self, data, strategy, commission=0.022, exclusive_orders=True):
        self.data = data
        self.strategy = strategy()
        self.commission = commission
        self.exclusive_orders = exclusive_orders

        self.creat_output_data_layout()

    def creat_output_data_layout(self):
        self.data["Cash"] = None
        self.data["TradeType"] = None
        self.data["TradeVolume"] = None
        self.data["TradeValue"] = None
        self.data["TradeStock"] = None
        self.data["TradeID"] = None
        self.data["TradePositionList"] = None

    def data_extend_order(self, strat_order, i):
        self.data["TradeType"].iloc[i] = strat_order

    def run(self):
        for i in range(1, len(self.data.index)):
            self.strategy.data = self.data.iloc[:i]
            self.data_extend_order(self.strategy.get_order(), i)
            # print(self.strategy.data)

        self.data.to_csv('test.csv')

    def plot(self):
        pass

def aligator_indicator(green, red, blue):
    try:
        is_red_blue_crossover = red[-2] < blue[-2] and red[-1] > blue[-1]
        is_blue_red_crossover =  red[-2] > blue[-2] and red[-1] < blue[-1]

        green_over_blue = green[-1] > blue[-1]
        blue_over_green = green[-1] < blue[-1]

        green_over_red = green[-1] > red[-1]
        red_over_green = green[-1] < red[-1]

        if is_red_blue_crossover and green_over_blue and green_over_red:
            return True
        if is_blue_red_crossover and blue_over_green and red_over_green:
            return False
        return None
    except IndexError:
        return None

class AligatorIndicator(Strategy):
    def init(self):
        price = self.data.Close
        self.green = self.I(moving_average, price, 5, 3)
        self.red = self.I(moving_average, price, 8, 5)
        self.blue = self.I(moving_average, price, 13, 8)

    def next(self):
        indicator = aligator_indicator(self.green, self.red, self.blue)
        if indicator != None:
            if indicator:
                self.position.close()
                self.buy()
            else:
                self.position.close()
                self.sell()

#Collect Data from CSV base on its Stock name
def datafromcsv(Stock, start_date=np.datetime64(date(2000, 1, 1)), end_date=np.datetime64(date(2020, 1, 1))):
    data = pd.read_csv("ressources/testData/"+ Stock + ".csv")
    columns = ['Date', 'Volume', 'Open', 'High', 'Low', 'Close', 'adjclose']
    data.columns = columns
    data = data.set_index("Date")
    data.index= pd.to_datetime(data.index)
    data = data.sort_index()
    data = data.iloc[ lambda x: x.index > start_date] 
    data = data.iloc[ lambda x: x.index < end_date]
    return data

def run(strategy=AligatorIndicator, strategy_str="AligatorIndicator"):
    bt = Backtest(datafromcsv("AAPL"), strategy, commission=.002,
                exclusive_orders=True)
    stats = bt.run()

    # if not os.path.exists(html_dir):
    #     os.mkdir(html_dir)

    # bt.plot(filename='./' + html_dir + '/' + strategy_str)

# def run():
