import pandas as pd
import numpy as np
import glob
import matplotlib.pyplot as plt
from scipy import stats

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
balloon = pd.concat([pd.read_csv(file) for file in
                           glob.glob(r"C:\Users\le\OneDrive - Ilmatieteen laitos\Campaigns\Pace2022\FMI balloon payload\Processed_data/*.csv")],
                           ignore_index=True)
balloon["datetime (utc)"] = pd.to_datetime(balloon["datetime (utc)"])
balloon.rename(columns={"datetime (utc)": "datetime"}, inplace=True)
balloon.replace(-9999.9, np.nan, inplace=True)
balloon = balloon.set_index('datetime').resample('1min').mean().reset_index()
balloon = balloon[np.abs(balloon['height_bme (m)']-290) < 50]

# %%
# df = station.merge(balloon, on='datetime', how='inner').merge(station_dmps, on='datetime', how='inner')
df = balloon.merge(station, on='datetime', how='inner')
# df_inter = df[np.abs(df['press_bme (hPa)'] - df['P']) < 5]
df_inter = df.copy()

# %%



# %%
fig, ax = plt.subplots(figsize=(4.5, 4), constrained_layout=True)
ax.plot(df_inter['T'], df_inter['temp_bme (C)'], '.')
ax.set_ylabel(r"Payload temperature (°C)")
ax.grid()
ax.set_aspect('equal', 'box')
ax.set_xlabel(r"Station temperature (°C)")

# Plot 1:1 line
x_11 = np.array([-5, 15])
ax.plot(x_11, x_11, 'k--', alpha=0.5, label='1:1 line')

# Compute and display fit, R², and p-value
_x = df_inter['T'].to_numpy()
_y = df_inter['temp_bme (C)'].to_numpy()
mask = np.isfinite(_x) & np.isfinite(_y)
if mask.any():
    x = _x[mask]
    y = _y[mask]

    # Linear regression (Pearson): slope, intercept, r, p
    res = stats.linregress(x, y)
    m = res.slope
    b = res.intercept
    r2 = res.rvalue * res.rvalue
    pval = res.pvalue

    # Plot best-fit line across the same span as 1:1
    x_fit = np.array([-5, 15])
    y_fit = m * x_fit + b
    label = f"y = {m:.3g}x {b:.3g}\n$R^2$ = {r2:.2f}; p = {pval:.2g}"
    ax.plot(x_fit, y_fit, '-', color='tab:red', label=label)

    ax.legend(loc='upper left', framealpha=0.8, fancybox=True)

fig.savefig(r"C:\Users\le\OneDrive - Ilmatieteen laitos\PaCE_2022\ESSD special issue\Viet_et_al_2025\Review_answer/Review_resources/T_intercomp.png",
            dpi=600, bbox_inches='tight')


# %%
df_rh = df_inter[~df_inter['ED_mcda (um)'].notna()]
fig, ax = plt.subplots(figsize=(4.5, 4), constrained_layout=True)
ax.plot(df_rh['RH'], df_rh['rh_bme (%)'], '.')
ax.set_ylabel(r"Payload relative humidity (%)")
ax.grid()
ax.set_aspect('equal', 'box')
ax.set_xlabel(r"Station relative humidity (%)")

# Plot 1:1 line
x_11 = np.array([60, 100])
ax.plot(x_11, x_11, 'k--', alpha=0.5, label='1:1 line')
    
# Compute and display fit, R², and p-value
_x = df_rh['RH'].to_numpy()
_y = df_rh['rh_bme (%)'].to_numpy()
mask = np.isfinite(_x) & np.isfinite(_y)
if mask.any():
    x = _x[mask]
    y = _y[mask]

    # Linear regression (Pearson): slope, intercept, r, p
    res = stats.linregress(x, y)
    m = res.slope
    b = res.intercept
    r2 = res.rvalue * res.rvalue
    pval = res.pvalue

    # Plot best-fit line across the same span as 1:1
    x_fit = np.array([60, 100])
    y_fit = m * x_fit + b
    label = f"y = {m:.3g}x {b:.3g}\n$R^2$ = {r2:.2f}; p = {pval:.2g}"
    ax.plot(x_fit, y_fit, '-', color='tab:red', label=label)

    ax.legend(loc='upper left', framealpha=0.8, fancybox=True)
fig.savefig(r"C:\Users\le\OneDrive - Ilmatieteen laitos\PaCE_2022\ESSD special issue\Viet_et_al_2025\Review_answer/Review_resources/rh_intercomp.png",
            dpi=600, bbox_inches='tight')
# %%
