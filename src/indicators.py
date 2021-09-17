import pandas as pd

def SMA(data, n):
    return pd.Series(data).rolling(n).mean()