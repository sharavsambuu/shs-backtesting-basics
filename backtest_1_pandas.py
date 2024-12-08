import warnings
warnings.filterwarnings("ignore")
def action_with_warnings():
    warnings.warn("should not appear")
with warnings.catch_warnings(record=True):
    action_with_warnings()
import configparser
import time
import talib
import numpy           as np
import pandas          as pd
from   multiprocessing import Pool
from   itertools       import product
from   functools       import partial


WORKER_COUNT = 8
SYMBOL       = "XAUUSD"


def read_1min_bars(symbol):
    start_time = time.time()
    config = configparser.ConfigParser()
    config.read("config.ini")
    csv_path = config.get(symbol, 'csv_path')
    df_ = pd.read_csv(f"{csv_path}", header=None, names=[
        'Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'DuplicatedVolume', 'Spread'
    ])
    df_['Datetime'] = pd.to_datetime(df_['Date'] + ' ' + df_['Time'])
    df_.set_index('Datetime', inplace=True)
    df_ = df_[['Open', 'High', 'Low', 'Close', 'Volume']]
    df_.dropna(inplace=True)
    print(f"Read {csv_path}, elapsed : {time.time()-start_time}")
    return df_


def calculate_indicators(df, params):
    p_ma_fast, p_ma_slow, p_atr_window = params
    df['fast_ma'] = talib.SMA(df['Close'], timeperiod=p_ma_fast)
    df['slow_ma'] = talib.SMA(df['Close'], timeperiod=p_ma_slow)
    df['slow_ma'] = talib.ATR(df['High'], df['Low'], df['Close'], timeperiod=p_atr_window)
    return df


def backtest_worker(
    df_, 
    params
    ):
    p_timeframe, p_ma_fast, p_ma_slow, p_atr_window, p_tp_mult, p_sl_mult, p_exit_n_bar = params
    print(f"#### Backtesting parameters :")
    print(f"Timeframe   : {p_timeframe}"  )
    print(f"MA fast     : {p_ma_fast}"    )
    print(f"MA slow     : {p_ma_slow}"    )
    print(f"ATR window  : {p_atr_window}" )
    print(f"TP mult     : {p_tp_mult}"    )
    print(f"SL mult     : {p_sl_mult}"    )
    print(f"Exit N bars : {p_exit_n_bar}" )
    print("\n")

    df = df_.resample(p_timeframe).agg({'Open':'first', 'High':'max', 'Low':'min', 'Close':'last', 'Volume': 'sum'})
    df.dropna(inplace=True)

    df = calculate_indicators(df, (p_ma_fast, p_ma_slow, p_atr_window))




    print(df)



    return df

if __name__=="__main__":
    start_time = time.time()


    df_ = read_1min_bars(symbol=SYMBOL)

    l_timeframe  = list(['30Min'])
    l_ma_fast    = list(np.arange(10,  30+10, 10, dtype=np.int32))
    l_ma_slow    = list(np.arange(90, 120+10, 10, dtype=np.int32))
    l_atr_window = [14]
    l_tp_mult    = list(np.arange(1.0, 1.0+0.5, 0.5, dtype=np.float32))
    l_sl_mult    = list(np.arange(1.0, 1.0+0.5, 0.5, dtype=np.float32))
    l_exit_n_bar = list(np.arange(1, 2, 1))
    params  = list(product(
        l_timeframe,
        l_ma_fast,
        l_ma_slow,
        l_atr_window,
        l_tp_mult,
        l_sl_mult,
        l_exit_n_bar
    ))


    pool = Pool(processes=WORKER_COUNT)
    try:
        results = pool.map(partial(backtest_worker, df_), params)
    except KeyboardInterrupt:
        pool.terminate()
    finally:
        pool.close()
        pool.join()


    print(f"Backtest pandas elapsed : {time.time()-start_time}")
    pass