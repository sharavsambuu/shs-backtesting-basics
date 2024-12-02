#%%
import warnings
warnings.filterwarnings("ignore")
def action_with_warnings():
    warnings.warn("should not appear")
with warnings.catch_warnings(record=True):
    action_with_warnings()
import configparser
import mplfinance as mpf
import pandas     as pd


#%%
config = configparser.ConfigParser()
config.read("config.ini")
csv_path = config.get('XAUUSD', 'csv_path')

df = pd.read_csv(f"{csv_path}", header=None, names=[
    'Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'DuplicatedVolume', 'Spread'
])
df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
df.set_index('Datetime', inplace=True)
df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
df.dropna(inplace=True)

df


#%%
plot_df = df.iloc[-1000:]
mpf.plot(plot_df, type='candle', style='binance')


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


#%%


#%%

