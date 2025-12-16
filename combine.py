import pandas as pd
import glob
import UAVision.bme.preprocess as bme_preprocess
import UAVision.cpc.preprocess as cpc_preprocess
import UAVision.mcda.preprocess as mcda_preprocess
import UAVision.pops.preprocess as pops_preprocess
from functools import reduce
import numpy as np
import metpy.calc as mpcalc
from metpy.units import units

# %%

def preprocess_mcda(file, size):
    """
    mCDA processing, calculate derived parameters as well
    file: path to mcda csv file (string)
    size: size category string, one of the following
      ['PSL_0.6-40', 'PSL_0.15-17', 'water_0.6-40', 'water_0.15-17'] OR
      an array-like of mid-bin values (list/tuple/ndarray)
      If an array-like is provided, it must be length 256.
    return: processed dataframe
    """
    # accept an array-like of mid_bin values as well as a size key string
    if isinstance(size, (list, tuple, np.ndarray, pd.Series)):
        mid_bin = np.asarray(size, dtype=float)
        if mid_bin.ndim != 1 or mid_bin.size != 256:
            raise ValueError(
                "When providing an array-like 'size', it must be one-dimensional with length 256."
            )
    elif isinstance(size, str):
        if size not in mcda_preprocess.mcda_midbin_all:
            raise KeyError(
                f"size '{size}' not found. Valid keys: {list(mcda_preprocess.mcda_midbin_all.keys())}"
            )
        mid_bin = np.array(mcda_preprocess.mcda_midbin_all[size], dtype=float)
        mid_bin = mid_bin[81:]
    else:
        raise TypeError("size must be a key string or an array-like of 256 mid-bin values")

    # calculate size dlog_bin
    print(size)
    binedges = np.append(
        np.append(
            mid_bin[0] - (-mid_bin[0] + mid_bin[1]) / 2,
            (mid_bin[:-1] + mid_bin[1:]) / 2,
        ),
        (mid_bin[-1] - mid_bin[-2]) / 2 + mid_bin[-1],
    )
    dlog_bin = np.log10(binedges[1:]) - np.log10(binedges[:-1])

    # Load file
    df = pd.read_csv(file, skiprows=1, header=None, dtype=str)
    df = df.iloc[:, np.r_[0, 82:257, -6:0]]
    df = df.dropna(axis=0)
    df = df.reset_index(drop=True)
    df.columns = np.arange(df.columns.size)
    df[0] = pd.to_datetime(df[0], format="%Y%m%d%H%M%S")

    dndlog_label = ["bin" + str(x) + "_mcda (dN/dlogDp)" for x in range(1, 176)]
    conc_label = ["bin" + str(x) + "_mcda (cm-3)" for x in range(1, 176)]
    pm_label = [
        "pcount_mcda",
        "pm1_mcda",
        "pm25_mcda",
        "pm4_mcda",
        "pm10_mcda",
        "pmtot_mcda",
    ]
    df.columns = np.r_[["datetime"], conc_label, pm_label]

    # Convert hex to int
    df[conc_label] = df[conc_label].map(
        lambda x: int(x, base=16)
    )
    # Convert to float
    df = df.set_index("datetime").astype("float").reset_index() 
    # Bin counts
    df_bins = df[conc_label].copy().to_numpy().astype(float)
    # Calculate concentration cm-3
    df[conc_label] = df[conc_label] / 10 / 46.67  # 10s averaged, 2.8L/min flow = 46.67 ccm/s

    # Calculate dN/dlogDp
    dndlog = df[conc_label] / dlog_bin
    dndlog.columns = dndlog_label
    df = pd.concat([df, dndlog], axis=1)    
    # Calculate CDNC
    df["Nd_mcda (cm-3)"] = df_bins.sum(axis=1) / 10 / 46.67
    # Calculate LWC
    conc_perbin = df_bins / 10 / (2.8e-3 / 60)
    lwc_perbin = conc_perbin * 1e6 * np.pi / 6 * (mid_bin * 1e-6) ** 3
    lwc_sum = lwc_perbin.sum(axis=1)
    df["LWC_mcda (g/m3)"] = lwc_sum
    # Calculate MVD
    p_lwc_perbin = np.divide(
        lwc_perbin,
        lwc_sum[:, np.newaxis],
        out=np.zeros_like(lwc_perbin),
        where=lwc_sum[:, np.newaxis] != 0,
    )
    cumsum_lwc_perbin = p_lwc_perbin.cumsum(axis=1)
    cumsum_lwc_perbin[df_bins == 0] = np.nan
    # find imin and imax, they contain the point where cumsum_lwc_perbin == 0.5
    imax = np.argmax((cumsum_lwc_perbin > 0.5), axis=1)
    imin = (
        cumsum_lwc_perbin.shape[1]
        - np.argmax(cumsum_lwc_perbin[:, ::-1] < 0.5, axis=1)
        - 1
    )
    # The MVD formula is based on this where max is first non-zero bin cumsum > 0.5 and
    # min is last non-zero bin cumsum < 0.5
    # (0.5 - cum_min) / (cum_max - cum_min) = (bx - bmin) / (bmax - bmin)
    cum_min = cumsum_lwc_perbin[np.arange(len(cumsum_lwc_perbin)), imin]
    cum_max = cumsum_lwc_perbin[np.arange(len(cumsum_lwc_perbin)), imax]
    bmin = mid_bin[imin]
    bmax = mid_bin[imax]
    df["MVD_mcda (um)"] = bmin + (0.5 - cum_min) / (cum_max - cum_min) * (bmax - bmin)
    # Calculate ED
    top = (conc_perbin * mid_bin**3).sum(axis=1)
    bottom = (conc_perbin * mid_bin**2).sum(axis=1)
    df["ED_mcda (um)"] = np.divide(
        top, bottom, out=np.zeros_like(top), where=bottom != 0
    )
    # Drop columns
    df = df.drop(["pcount_mcda", "pm4_mcda", "pmtot_mcda"], axis=1)
    return df


def calc_dewpoint(temp_array, rh_array):
    """Calculate dewpoint for entire arrays at once"""
    dewpoints = mpcalc.dewpoint_from_relative_humidity(
        temp_array * units.degC,
        rh_array * units.percent
    )
    return dewpoints.magnitude  # Return numeric values without units

def calc_rh(temp_array, dp_array):
    """Calculate dewpoint for entire arrays at once"""
    rh = mpcalc.relative_humidity_from_dewpoint(
        temp_array * units.degC,
        dp_array * units.degC
    ).to('percent')
    return rh.magnitude  # Return numeric values without units

# %%
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

bme = pd.concat([bme_preprocess.preprocess_bme(x) for x in bme_path])
cpc = pd.concat([cpc_preprocess.preprocess_cpc(x) for x in cpc_path])
pops = pd.concat([pops_preprocess.preprocess_pops(x) for x in pops_path])

mcda = pd.DataFrame({})
for file in mcda_path:
    mcda_time = pd.to_datetime(file[-17:-9])
    if mcda_time < pd.Timestamp('20221003'):
        df = preprocess_mcda(file, 'water_0.15-17')
    else:
        df = preprocess_mcda(file, 'water_0.6-40')
    mcda = pd.concat([mcda, df], ignore_index=True)

flight_time = pd.read_csv(
    r'C:\Users\le\OneDrive - Ilmatieteen laitos\Campaigns\Pace2022\FMI balloon payload\Raw_data/ground_time.csv')
flight_time['start'] = pd.to_datetime(flight_time['start'])
flight_time['end'] = pd.to_datetime(flight_time['end'])

# replace bad values in pops with -9999.9
pops['datetime'] = pops['datetime'] + pd.Timedelta(hours=2) # POPS is in UTC, the rest is in UTC+2
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
    df_['datetime'] = df_['datetime'] - pd.Timedelta(hours=2) # we used winter time even though it was summer
    rh_pops = calc_rh(df_['temp_pops (C)'].to_numpy(), calc_dewpoint(df_['temp_bme (C)'].to_numpy(), 
                            df_['rh_bme (%)'].to_numpy()))
    temp_pops_index = df_.columns.get_loc('temp_pops (C)')
    df_.insert(temp_pops_index + 1, 'rh_pops (%)', rh_pops)
    df_.loc[(df_['rh_pops (%)'] < 0) | (df_['rh_pops (%)'] > 100), 'rh_pops (%)'] = -9999.9
    df_ = df_.reset_index(drop=True)
    cloud = mcda_preprocess.cloudmask(df_)
    df_.loc[~cloud, ['Nd_mcda (cm-3)', 'LWC_mcda (g/m3)', 'MVD_mcda (um)', 'ED_mcda (um)']] = -9999.9
    df_ = df_.fillna(-9999.9)
    save_time = df_.iloc[0].datetime.strftime("%Y%m%d.%H%M")
    df_ = df_.rename(columns={'datetime': 'datetime (utc)'})
    df_.to_csv(
            save_path + 'FMI.TBS.b1.' + save_time + '.csv', index=False)
    print(f'File {save_time} saved')