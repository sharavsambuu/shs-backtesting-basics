import warnings
warnings.filterwarnings("ignore")
def action_with_warnings():
    warnings.warn("should not appear")
with warnings.catch_warnings(record=True):
    action_with_warnings()
import configparser
import time
import pandas as pd


WORKER_COUNT = 8
TIMEFRAME    = "30Min"


def read_1min_bars(symbol):
    config = configparser.ConfigParser()
    config.read("config.ini")
    csv_path = config.get(symbol, 'csv_path')
    print(f"reading from {csv_path}")
    df_ = pd.read_csv(f"{csv_path}", header=None, names=[
        'Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'DuplicatedVolume', 'Spread'
    ])
    df_['Datetime'] = pd.to_datetime(df_['Date'] + ' ' + df_['Time'])
    df_.set_index('Datetime', inplace=True)
    df_ = df_[['Open', 'High', 'Low', 'Close', 'Volume']]
    df_.dropna(inplace=True)
    return df_


if __name__=="__main__":
    start_time = time.time()

    df_ = read_1min_bars(symbol="XAUUSD")
    df = df_.resample(TIMEFRAME).agg({'Open':'first', 'High':'max', 'Low':'min', 'Close':'last', 'Volume': 'sum'})
    df.dropna(inplace=True)

    print(df)


    print(f"Backtest pandas elapsed : {time.time()-start_time}")
    pass