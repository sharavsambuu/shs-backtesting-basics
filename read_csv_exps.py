#%%
import configparser
import pandas as pd


#%%
config = configparser.ConfigParser()
config.read("config.ini")
print(config.sections())
csv_path = config.get('XAUUSD', 'csv_path')
print(f"path : {csv_path}")


#%%
df = pd.read_csv(f"{csv_path}", header=None, names=[
    'Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'DuplicatedVolume', 'Spread'
])
df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
df.set_index('Datetime', inplace=True)
df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
df.dropna(inplace=True)
df


#%%
df.iloc[-100:]['Close'].plot()


#%%



