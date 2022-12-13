import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
%matplotlib qt

# %%
save_path = r'C:\Users\le\OneDrive - Ilmatieteen laitos\Campaigns\Pace2022\FMI balloon payload\Processed_data/'
bme = pd.read_csv(save_path + 'bme.csv')
cpc = pd.read_csv(save_path + 'cpc.csv')
minicda = pd.read_csv(save_path + 'minicda.csv')
POPS = pd.read_csv(save_path + 'POPS.csv')

# %%
flight_time = pd.read_csv(
    r'C:\Users\le\OneDrive - Ilmatieteen laitos\Campaigns\Pace2022\FMI balloon payload\Raw_data/ground_time.csv')
flight_time['start'] = pd.to_datetime(flight_time['start'])
flight_time['end'] = pd.to_datetime(flight_time['end'])

# %%
POPS['datetime'] = pd.to_datetime(POPS['datetime'])
bme['datetime'] = pd.to_datetime(bme['datetime'])
minicda['datetime'] = pd.to_datetime(minicda['datetime'])
cpc['datetime'] = pd.to_datetime(cpc['datetime'])

# %%
bme['bme_data'] = True
cpc['cpc_data'] = True
minicda['minicda_data'] = True
POPS['POPS_data'] = True

# %%
df = bme.merge(cpc, how='outer', on=['datetime', 'flight_ID'])
df = df.merge(minicda, how='outer', on=['datetime', 'flight_ID'])
df = df.merge(POPS, how='left', on='datetime')
df = df.sort_values('datetime')
df = df.reset_index(drop=True)
df['datetime'] = pd.to_datetime(df['datetime'])

for i, row in flight_time.iterrows():
    condition = df[(df['flight_ID'] == i+1) &
                   ((df['datetime'] < row['start']) | (df['datetime'] > row['end']))]
    df = df.drop(condition.index)
df = df.reset_index(drop=True)
grp = df.groupby('flight_ID')

# %%
fig, ax = plt.subplots(figsize=(16, 9))
ax.bar(grp['datetime'].first().index - 0.3, grp['bme_data'].sum()/60, width=0.2,
       label='BME')
ax.bar(grp['datetime'].first().index - 0.1, grp['cpc_data'].sum()/60, width=0.2,
       label='CPC')
ax.bar(grp['datetime'].first().index + 0.1, grp['minicda_data'].sum()/60, width=0.2,
       label='miniCDA')
ax.bar(grp['datetime'].first().index + 0.3, grp['POPS_data'].sum()/60, width=0.2,
       label='POPS')
ax.legend()
ax.set_xticks(np.arange(1, 22))
timelabel = [x.strftime("%d/%m\n%H:%M") for x in grp['datetime'].first()]
ax.set_xticklabels(timelabel)
ax.set_xlabel('Starting time (UTC+2)')
ax.set_ylabel('Hours of data')
ax.grid()
fig.tight_layout()
fig.savefig(save_path + 'available_data_balloon.png', dpi=500, bbox_inches='tight')
