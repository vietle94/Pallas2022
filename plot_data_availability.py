import pandas as pd
import glob
import matplotlib.pyplot as plt
import numpy as np

data_path = r'C:\Users\le\OneDrive - Ilmatieteen laitos\Campaigns\Pace2022\FMI balloon payload\Processed_data/'

df = pd.DataFrame({})
for i, file in enumerate(glob.glob(data_path + '*.csv')):
    df_file = pd.read_csv(file)
    df_file['flight_id'] = i + 1
    df = pd.concat([df, df_file], ignore_index=True)

df['datetime'] = pd.to_datetime(df['datetime'])
df.replace(-9999.9, np.nan, inplace=True)

df[[x for x in df.columns if "_mcda" in x]] = df[[x for x in df.columns if "_mcda" in x]].ffill(limit_area='inside')

x_tick_label = df.groupby('flight_id').first().datetime.dt.strftime('%d/%m\n %H:%M')
df_count = df[["temp_bme (C)", "N_conc_cpc(1/ccm)", "N_conc_pops (1/ccm)", "pm10_mcda", 'flight_id']]
df_count = df_count.groupby("flight_id").count()

fig, ax = plt.subplots(1, 1, figsize=(8, 4), constrained_layout=True)
x = 1.2*df_count.index
ax.bar(x - 0.3, df_count['temp_bme (C)']/3600, label='BME', width=0.2)
ax.bar(x - 0.1, df_count['N_conc_cpc(1/ccm)']/3600, label='CPC', width=0.2)
ax.bar(x + 0.1, df_count['N_conc_pops (1/ccm)']/3600, label='POPS', width=0.2)
ax.bar(x + 0.3, df_count['pm10_mcda']/3600, label='mCDA', width=0.2)
ax.set_ylabel('Data availability (hours)')
ax.legend()
ax.set_xticks(x)
ax.set_xticklabels(x_tick_label, size=7)
ax.grid()
ax.set_xlabel('Flight time (UTC)')
fig.savefig(r"C:\Users\le\OneDrive - Ilmatieteen laitos\My_articles\2024\Pallas/data_availability.png", dpi=600,
            bbox_inches='tight')
