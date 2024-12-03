#%%
import warnings
warnings.filterwarnings("ignore")
def action_with_warnings():
    warnings.warn("should not appear")
with warnings.catch_warnings(record=True):
    action_with_warnings()
import configparser
import time
import mplfinance as mpf
import pandas     as pd


#%%
start_time = time.time()
config = configparser.ConfigParser()
config.read("config.ini")
csv_path = config.get('XAUUSD', 'csv_path')
print(f"reading from {csv_path}")

df_ = pd.read_csv(f"{csv_path}", header=None, names=[
    'Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'DuplicatedVolume', 'Spread'
])
df_['Datetime'] = pd.to_datetime(df_['Date'] + ' ' + df_['Time'])
df_.set_index('Datetime', inplace=True)
df_ = df_[['Open', 'High', 'Low', 'Close', 'Volume']]
df_.dropna(inplace=True)

print(df_)

print(f"elapsed : {time.time()-start_time}")


#%%
df_


#%%
plot_df = df_.iloc[-1000:]
mpf.plot(plot_df, type='candle', style='binance')


#%%


#%%
start_time = time.time()
df = df_.resample('30Min').agg({'Open':'first', 'High':'max', 'Low':'min', 'Close':'last', 'Volume': 'sum'})
df.dropna(inplace=True)
print(df)
print(f"elapsed : {time.time()-start_time}")

#%%


#%%


#%%


#%%


#%%


#%%


#%%


#%%


#%%


#%%


#%%


#%%


#%%


#%%


#%%


#%%


#%%


#%%


#%%


#%%


#%%


#%%


#%%


#%%


#%%


#%%


#%%


#%%


#%%


#%%

