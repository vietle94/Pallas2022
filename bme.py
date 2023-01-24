import pandas as pd
import glob

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
time_col = df.pop('datetime')
df.insert(0, 'datetime', time_col)

# df = df.set_index('datetime').resample('1min').mean().dropna().reset_index()

# %%
flight_time = pd.read_csv(
    r'C:\Users\le\OneDrive - Ilmatieteen laitos\Campaigns\Pace2022\FMI balloon payload\Raw_data/ground_time.csv')
flight_time['start'] = pd.to_datetime(flight_time['start'])
flight_time['end'] = pd.to_datetime(flight_time['end'])
for i, row in flight_time.iterrows():
    condition = df[(df['flight_ID'] == i+1) &
                   ((df['datetime'] < row['start']) | (df['datetime'] > row['end']))]
    df = df.drop(condition.index)
df = df.reset_index(drop=True)
df = df.rename({'temp_bme': 'Temperature (C)', 'press_bme': 'Pressure (hPa)',
               'rh_bme': 'Relative humidity (%)'}, axis=1)

# %%
for id, grp in df.groupby('flight_ID'):
    suf_time = grp.iloc[0].datetime.strftime("%Y%m%d_%H%M")
    grp.drop(['flight_ID'], axis=1).to_csv(
        save_path + f'PACE' + suf_time + f'_BME.csv', index=False)
