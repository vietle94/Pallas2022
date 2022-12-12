import pandas as pd
import glob
import numpy as np

# %%
file_path = glob.glob(
    r'C:\Users\le\OneDrive - Ilmatieteen laitos\Campaigns\Pace2022\FMI balloon payload\Raw_data/**/HK*', recursive=True)
save_path = r'C:\Users\le\OneDrive - Ilmatieteen laitos\Campaigns\Pace2022\FMI balloon payload\Processed_data/'
file_path = [x for x in file_path if 'first_flight' not in x]

# %%
df = pd.concat([pd.read_csv(x) for x in file_path])

# %%
df = df.dropna(axis=0)
df = df.reset_index(drop=True)
df['datetime'] = pd.to_datetime(df['DateTime'], unit='s')
df = df.drop(['DateTime'], axis=1)
df = df.set_index('datetime').resample('1min').mean().dropna().reset_index()

# %%
df.to_csv(save_path + 'POPS.csv', index=False)
