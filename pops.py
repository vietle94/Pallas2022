import re
import pandas as pd
import glob
import numpy as np

# %%
file_path = glob.glob(
    r'C:\Users\le\OneDrive - Ilmatieteen laitos\Campaigns\Pace2022\FMI balloon payload\Raw_data/**/HK*', recursive=True)
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
df['datetime'] = pd.to_datetime(df['DateTime'], unit='s') + pd.Timedelta('2hour')
df = df.drop(['DateTime'], axis=1)
time_col = df.pop('datetime')
df.insert(0, 'datetime', time_col)

# df = df.set_index('datetime').resample('1min').mean().dropna().reset_index()

# %%
df_ = pd.DataFrame({})
flight_time = pd.read_csv(
    r'C:\Users\le\OneDrive - Ilmatieteen laitos\Campaigns\Pace2022\FMI balloon payload\Raw_data/ground_time.csv')
flight_time['start'] = pd.to_datetime(flight_time['start'])
flight_time['end'] = pd.to_datetime(flight_time['end'])
for i, row in flight_time.iterrows():
    df_ = df_.append(df[((df['datetime'] > row['start']) & (df['datetime'] < row['end']))])
df_ = df_.reset_index(drop=True)

# %%
pop_binedges = '0.119552706	0.140894644	0.169068337	0.204226949	0.227523895	0.253291842	0.279285719	0.35426882	0.604151175	0.705102841	0.785877189	1.100686925	1.117622254	1.765832382	2.690129739	3.014558062 4.392791391'
pop_binedges = np.fromstring(pop_binedges, dtype=float, sep="\t")
pop_midbin = (pop_binedges[1:] + pop_binedges[:-1])/2
dlog_bin = np.log10(pop_binedges[1:]) - np.log10(pop_binedges[:-1])
pop_binlab = ['b0', 'b1', 'b2',
              'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 'b9', 'b10', 'b11', 'b12', 'b13',
              'b14', 'b15']

for particle_size, each_dlog_bin in zip(pop_binlab, dlog_bin):
    df_[particle_size] = df_[particle_size]/(df_[' POPS_Flow']*16.6667) / each_dlog_bin
df_.columns = ['bin' + x[1:] + ' (dN/dlogDp)' if re.search('b[0-9]+', x)
               else x for x in df_.columns]

df_ = df_.drop([' Status', ' PartCt', ' BL', ' BLTH', ' STD', ' TofP', ' POPS_Flow', ' PumpFB', ' LDTemp', ' LaserFB',
                ' LD_Mon', ' Temp', ' BatV', ' Laser_Current', ' Flow_Set',
                'PumpLife_hrs', ' BL_Start', ' TH_Mult', ' nbins', ' logmin', ' logmax',
                ' Skip_Save', ' MinPeakPts', 'MaxPeakPts', ' RawPts'], axis=1)
df_ = df_.rename({' PartCon': 'Particle concentration (1/ccm)', ' P': 'Pressure (hPa)'}, axis=1)


# %%
for id, grp in df_.groupby('flight_ID'):
    suf_time = grp.iloc[0].datetime.strftime("%Y%m%d_%H%M")
    grp.drop(['flight_ID'], axis=1).to_csv(
        save_path + f'PACE' + suf_time + f'_POPS.csv', index=False)
