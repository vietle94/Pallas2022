import pandas as pd
import numpy as np
import glob
import matplotlib.pyplot as plt

# %%
file_dir = r"C:\Users\le\OneDrive - Ilmatieteen laitos\PaCE_2022\Station data\Meteorology/"
files = glob.glob(file_dir + "Sammal_AWS_2022[01][90]*.csv")

df = pd.concat([pd.read_csv(x, encoding='unicode_escape') for x in files], ignore_index=True)
df['datetime'] = pd.to_datetime(df['Read time (UTC+2)'], format='mixed') - pd.Timedelta(hours=2)

# %%
df = df[(df['datetime'] > pd.Timestamp('2022-09-17')) & (df['datetime'] < pd.Timestamp('2022-10-11'))]

# %%
fig, ax = plt.subplots(figsize=(9, 4))
ax.plot(df['datetime'], df['Wind speed (m/s)'], '.')
ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%d/%m'))
ax.grid()
# %%
df['Wind speed (m/s)'].mean()