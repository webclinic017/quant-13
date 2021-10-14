import numpy as np
import pandas as pd

from datetime import date
from abc import abstractmethod, ABCMeta

from ..indicators import moving_average

class Strategy(metaclass=ABCMeta):
    def __init__(self, data=None, cash=None):
        self.data = data
        self.cash = cash
        self.indicators = dict()
        self._broker = Broker(self.cash, self.data)
        self.position = self._broker.position
        self.order = None

        # self.init()

    def I(self, indicator_function, data, *args, **kwargs):
        indicator_data = indicator_function(data, *args, **kwargs)
        return indicator_data
    

    ## init nad next will be inited in the strategy defined by the user
    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def next(self):
        pass

    def get_order(self):
        self.order = None
        self.init()
        self.next()
        self._broker.process_orders()
        return self.trades

    def buy(self, *,
            size: float = None,
            limit: float = None,
            stop: float = None,
            sl: float = None,
            tp: float = None):

        return self._broker.new_order(size, "buy", limit, stop, sl, tp)

    def sell(self, *,
             size: float = None,
             limit: float = None,
             stop: float = None,
             sl: float = None,
             tp: float = None):

        return self._broker.new_order(-size, "sell", limit, stop, sl, tp)

    @property
    def position(self):
        return self._broker.position

    @property
    def orders(self):
        return self._broker.orders

    @property
    def trades(self):
        return self._broker.trades

class Position:

    def __init__(self, broker):
        self._broker = broker

    def close(self):
        for trade in self._broker.trades:
            trade.close()


class Order:
    def __init__(self , broker, size, order_type):
        self.__broker = broker
        self._size = size
        self._order_type = order_type
    def cancel(self):
        self.__broker.orders.remove(self)

class Trade:
    def __init__(self, broker, size, prize, trade_type):
        self.__broker = broker
        self._size = size
        self._prize = prize
        self._trade_type = trade_type

#    def close(self):
#         if self._trade_type == 'buy':
#             order = self.__broker.new_order(self._size,"sell")
#         if self._trade_type == 'sell':
#             order = self.__broker.new_order(self._size,"buy")
#         #Warning!!!! order can be None
#         self.__broker.orders.insert(0, order)
    
    @property
    def value(self):
        return abs(self._size)*self._prize
    
        

class Broker:
    def __init__(self, *, data, cash):
        self.orders = []
        self.trades = []
        self._exclusive_orders = None
        self._data = data
        self._cash = cash
        self.position = Position(self)
        

    def new_order(self, size, order_type, limit, stop, sl, tp):
        ## Args should be changend in the fuure for more functionality
        order = Order(self, size,  order_type)
        if self._exclusive_orders:
            for order in self.orders:
                order.cancel()
            for trade in self.trades:
                trade.close() 
        
        self.orders.append(order)
        return order

    def process_orders(self):
        data = self._data
        try:
            _open, high, low = data.Open[-1], data.High[-1], data.Low[-1]
            old_close = data.Close[-2]
        except IndexError:
            return

        for order in list(self.orders):
            ##needs to be a integer dont know how ?!
            size = int(order._size)
            self.open_trade(size, _open, order._order_type)
            self.orders.remove(order)


    def open_trade(self, size, price, trade_type):
        trade = Trade(self, size, price, trade_type)
        self.trades.append(trade)
        return trade





    
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
            trades = self.strategy.get_order()
            if len(trades = 0):
                out = ""
            else:
                out = trades[0]._trade_type
            self.data_extend_order(out, i)
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
