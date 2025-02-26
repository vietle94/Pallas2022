import pandas as pd
import glob
from UAVision import preprocess
from functools import reduce

bme_path = glob.glob(
    r'C:\Users\le\OneDrive - Ilmatieteen laitos\Campaigns\Pace2022\FMI balloon payload\Raw_data/**/bme*', recursive=True)
bme_path = [x for x in bme_path if 'first_flight' not in x]

cpc_path = glob.glob(
    r'C:\Users\le\OneDrive - Ilmatieteen laitos\Campaigns\Pace2022\FMI balloon payload\Raw_data/**/CPC*', recursive=True)
cpc_path = [x for x in cpc_path if 'first_flight' not in x]

mcda_path = glob.glob(
    r'C:\Users\le\OneDrive - Ilmatieteen laitos\Campaigns\Pace2022\FMI balloon payload\Raw_data/**/minicda_[0-9]*', recursive=True)
mcda_path = [x for x in mcda_path if 'first_flight' not in x]

pops_path = glob.glob(
    r'C:\Users\le\OneDrive - Ilmatieteen laitos\Campaigns\Pace2022\FMI balloon payload\Raw_data/**/HK*', recursive=True)
pops_path = [x for x in pops_path if 'first_flight' not in x]

save_path = r'C:\Users\le\OneDrive - Ilmatieteen laitos\Campaigns\Pace2022\FMI balloon payload\Processed_data/'

bme = pd.concat([preprocess.preprocess_bme(x) for x in bme_path])
cpc = pd.concat([preprocess.preprocess_cpc(x) for x in cpc_path])
pops = pd.concat([preprocess.preprocess_pops(x) for x in pops_path])

mcda = pd.DataFrame({})
for file in mcda_path:
    mcda_time = pd.to_datetime(file[-17:-9])
    if mcda_time < pd.Timestamp('20221003'):
        df = preprocess.preprocess_mcda(file, 'water_0.15-17')
    else:
        df = preprocess.preprocess_mcda(file, 'water_0.6-40')
    mcda = pd.concat([mcda, df], ignore_index=True)

flight_time = pd.read_csv(
    r'C:\Users\le\OneDrive - Ilmatieteen laitos\Campaigns\Pace2022\FMI balloon payload\Raw_data/ground_time.csv')
flight_time['start'] = pd.to_datetime(flight_time['start'])
flight_time['end'] = pd.to_datetime(flight_time['end'])

# replace bad values in pops with -9999.9
pops.set_index('datetime', inplace=True)
pops.loc[(pops.index > pd.Timestamp('2022-09-23 00:00:00')) & \
     (pops.index < pd.Timestamp('2022-10-01 00:00:00'))] = -9999.9
pops.reset_index(inplace=True)

# merge all dataframes
df = reduce(lambda left,right: pd.merge(left,right,on=['datetime'],
        how='outer', sort=True),
            [bme, cpc, pops, mcda]) 
df = df.fillna(-9999.9)

for i, row in flight_time.iterrows():
    df_ = df[((df['datetime'] > row['start']) & (df['datetime'] < row['end']))].copy()
    # df_['datetime'] = df_['datetime'].dt.tz_localize('Europe/Helsinki').dt.tz_convert('UTC')
    df_['datetime'] = df_['datetime'] - pd.Timedelta(hours=2) # we used winter time even though it was summer
    # df_['datetime'] = df_['datetime'].dt.tz_localize('UTC')
    df_ = df_.reset_index(drop=True)
    cloud = preprocess.cloudmask(df_)
    df_.loc[~cloud, ['Nd_mcda (cm-3)', 'LWC_mcda (g/m3)', 'MVD_mcda (um)', 'ED_mcda (um)']] = -9999.9
    save_time = df_.iloc[0].datetime.strftime("%Y%m%d.%H%M")
    df_ = df_.rename(columns={'datetime': 'datetime (utc)'})
    df_.to_csv(
            save_path + 'FMI.TBS.a1.' + save_time + '.csv', index=False)
    print(f'File {save_time} saved')