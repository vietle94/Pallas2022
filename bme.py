import pandas as pd
import glob
import numpy as np

# %%
file_path = glob.glob(
    r'C:\Users\le\OneDrive - Ilmatieteen laitos\Campaigns\Pace2022\FMI balloon payload\Raw_data/**/bme*', recursive=True)
save_path = r'C:\Users\le\OneDrive - Ilmatieteen laitos\Campaigns\Pace2022\FMI balloon payload\Processed_data/'
file_path = [x for x in file_path if 'first_flight' not in x]

# %%
df = pd.DataFrame({})
for i, file in enumerate(file_path):
    df_ = pd.read_csv(file)
    df_['flight_ID'] = i + 1
    df_ = df_.dropna(axis=0)
    df = df.append(df_, ignore_index=True)

# %%
df = df.dropna(axis=0)
df = df.reset_index(drop=True)
df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'])
df = df.drop(['date', 'time'], axis=1)
df = df.set_index('datetime').resample('1min').mean().dropna().reset_index()

# %%
df.to_csv(save_path + 'bme.csv', index=False)
