import pandas as pd
import numpy as np
import glob
import matplotlib.pyplot as plt

# %%
station = pd.concat([pd.read_csv(file) for file in
                     glob.glob("C:/Users/le/OneDrive - Ilmatieteen laitos/PaCE_2022/Station data/Meteorology/Sammal_AWS_2022[01][90]*.csv")],
                      ignore_index=True)
station = station.rename(columns={'Read time (UTC+2)': 'datetime',
                                  'Temp 570m (C)': 'T',
                                  'Humidity 570m (%)': 'RH',
                                  'Pressure (hPa)': 'P'})
station = station[['datetime', 'T', 'RH', 'P']]
station = station.dropna()
station['datetime'] = pd.to_datetime(station['datetime'], format='mixed')
station['datetime'] = station['datetime'] - pd.Timedelta(hours=2)  # we used winter time even though it was summer
station = station.set_index('datetime').resample('1min').mean().reset_index()

# %%
# station_cpc = pd.concat([pd.read_csv(file, encoding='unicode_escape') for file in
#                            glob.glob(r"C:\Users\le\Downloads\cpc_pm25_PaCE2022\FMI.CPC.b1*.csv")],
#                            ignore_index=True)
# station_cpc['datetime'] = pd.to_datetime(station_cpc['datetime'])
# station_cpc = station_cpc.set_index('datetime').resample('1min').mean().reset_index()
# station_cpc.dropna(inplace=True)

# %%
station_dmps = pd.concat([pd.read_csv(file, encoding='unicode_escape') for file in
                           glob.glob(r"C:\Users\le\Downloads\dmps_pm25_PaCE2022\FMI.DMPS.c1*.csv")],
                           ignore_index=True)
station_dmps['datetime'] = pd.to_datetime(station_dmps['datetime'])
station_dmps = station_dmps.set_index('datetime').resample('1min').mean().reset_index()
station_dmps.dropna(inplace=True)

# %%
balloon = pd.concat([pd.read_csv(file) for file in
                           glob.glob(r"C:\Users\le\OneDrive - Ilmatieteen laitos\Campaigns\Pace2022\FMI balloon payload\Processed_data/*.csv")],
                           ignore_index=True)
balloon["datetime (utc)"] = pd.to_datetime(balloon["datetime (utc)"])
balloon.rename(columns={"datetime (utc)": "datetime"}, inplace=True)
balloon.replace(-9999.9, np.nan, inplace=True)
balloon = balloon.set_index('datetime').resample('1min').mean().reset_index()

# %%
df = station.merge(balloon, on='datetime', how='inner').merge(station_dmps, on='datetime', how='inner')
df_inter = df[np.abs(df['press_bme (hPa)'] - df['P']) < 5]

# %%
fig, ax = plt.subplots(figsize=(4.5, 4), constrained_layout=True)
ax.plot([0, 2500], [0, 2500], '--', color='gray')
ax.plot(df_inter['total'], df_inter['N_conc_cpc (cm-3)'], '.')
ax.set_ylabel(r"Payload CPC concentration $(cm^{-3})$")
ax.grid()
ax.set_aspect('equal', 'box')
ax.set_xlabel(r"Station DMPS concentration $(cm^{-3})$")
fig.savefig(r"C:\Users\le\OneDrive - Ilmatieteen laitos\PaCE_2022\ESSD special issue\Viet_et_al_2025\Review_answer/Review_resources/cpc_intercomp.png",
            dpi=600, bbox_inches='tight')
