import xarray as xr
import glob
import pandas as pd
import numpy as np

save_dir = r"C:\Users\le\OneDrive - Ilmatieteen laitos\PaCE2022ESSD\cvs\Viet/"
csv_dir = r'C:\Users\le\OneDrive - Ilmatieteen laitos\PaCE2022ESSD\cvs/'
csv_files = glob.glob(csv_dir + '*.csv')

instrument = 'CAPS'
CAPS = [file for file in csv_files if "CAPS" in file]
CAPS_midbin = np.array([0.61, 0.68, 0.75, 0.82, 0.89, 0.96, 1.03, 1.1, 1.17, 1.25, 1.5, 2, 2.5, 3, 3.5, 4, 5, 6.5, 7.2, 7.9, 10.2, 12.5, 15, 20, 25, 30, 35, 40, 45, 50])
for file in CAPS:
    df = pd.read_csv(file, encoding='unicode_escape')
    df.rename(columns={'min': 'minute'}, inplace=True)
    df['datetime'] = pd.to_datetime(df[['year', 'month', 'day', 'hour', 'minute']])
    save_time = file.split('.')[-2]
    # %%
    df_xr = xr.Dataset.from_dataframe(df.set_index('datetime'))
    df_xr["dN/dlogDp"] = xr.concat(
                [df_xr[f"dN/dlogDp (cm-3) b{x}"] for x in range(1, 31)], CAPS_midbin
            ).T
    df_xr = df_xr.rename({"concat_dim": "bin"})

    df_xr = df_xr[['datetime',
                'dN/dlogDp',
                'number concentration (cm-3)',
                'liquid water content (g m-3)',
                'median volume diameter (µm)',
                'effective diameter (µm)',
                'Temp 570m (C)',
                'Dew point temp (C)',
                'Humidity 570m (%)',
                'Pressure (hPa)',
                'Wind speed (m/s)',
                'Wind dir (deg)',
                'Sun rad 1 (W/m2)',
                'Sun rad 2 (umol/s/m2)',
                'FD12P visibility (m)']]
    df_xr = df_xr.rename({'dN/dlogDp':'conc_bin',
                        'number concentration (cm-3)':'Nd',
                        'liquid water content (g m-3)':'LWC',
                        'median volume diameter (µm)':'MVD',
                        'effective diameter (µm)':'ED',
                        'Temp 570m (C)':'T',
                        'Dew point temp (C)':'Td',
                        'Humidity 570m (%)':'RH',
                        'Pressure (hPa)':'P',
                        'Wind speed (m/s)':'Ws',
                        'Wind dir (deg)':'Wd',
                        'Sun rad 1 (W/m2)':'sun_radiation_1',
                        'Sun rad 2 (umol/s/m2)':'sun_radiation_2',
                        'FD12P visibility (m)':'visibility'})

    df_xr['datetime'].attrs = {'long_name': 'datetime in UTC', '_FillValue': -9999.9, 'processing_level': 'b1'}
    df_xr['bin'].attrs = {'units': '(µm)', 'long_name': 'mid bin', '_FillValue': -9999.9, 'processing_level': 'b1'}
    df_xr['conc_bin'].attrs = {'units': 'dN/dlogDp (cm-3)', 'long_name': 'xxxxxxxx', '_FillValue': -9999.9, 'processing_level': 'b1'}
    df_xr['Nd'].attrs = {'units': '(cm-3)', 'long_name': 'number concentration', '_FillValue': -9999.9, 'processing_level': 'b1'}
    df_xr['LWC'].attrs = {'units': '(g m-3)', 'long_name': 'liquid water content', '_FillValue': -9999.9, 'processing_level': 'b1'}
    df_xr['MVD'].attrs = {'units': '(µm)', 'long_name': 'median volume diameter', '_FillValue': -9999.9, 'processing_level': 'b1'}
    df_xr['ED'].attrs = {'units': '(µm)', 'long_name': 'effective diameter', '_FillValue': -9999.9, 'processing_level': 'b1'}
    df_xr['T'].attrs = {'units': '(C)', 'long_name': 'Temp 570m', '_FillValue': -9999.9, 'processing_level': 'b1'}
    df_xr['Td'].attrs = {'units': '(C)', 'long_name': 'Dew point temp', '_FillValue': -9999.9, 'processing_level': 'b1'}
    df_xr['RH'].attrs = {'units': '(%)', 'long_name': 'Humidity 570m', '_FillValue': -9999.9, 'processing_level': 'b1'}
    df_xr['P'].attrs = {'units': '(hPa)', 'long_name': 'Pressure', '_FillValue': -9999.9, 'processing_level': 'b1'}
    df_xr['Ws'].attrs = {'units': '(m/s)', 'long_name': 'Wind speed', '_FillValue': -9999.9, 'processing_level': 'b1'}
    df_xr['Wd'].attrs = {'units': '(deg)', 'long_name': 'Wind dir', '_FillValue': -9999.9, 'processing_level': 'b1'}
    df_xr['sun_radiation_1'].attrs = {'units': '(W/m2)', 'long_name': 'Sun rad 1', '_FillValue': -9999.9, 'processing_level': 'b1'}
    df_xr['sun_radiation_2'].attrs = {'units': '(umol/s/m2)', 'long_name': 'Sun rad 2', '_FillValue': -9999.9, 'processing_level': 'b1'}
    df_xr['visibility'].attrs = {'units': '(m)', 'long_name': 'FD12P visibility', '_FillValue': -9999.9, 'processing_level': 'b1'}


    df_xr.attrs['platform_name'] = "Sammaltunturi" # check this please
    df_xr.attrs['institution'] = "Finnish Meteorological Institute"
    df_xr.attrs['source'] = "PaCE2022 campaign"
    df_xr.attrs['processing_level'] = "b1"
    df_xr.attrs['created by'] = "Viet Le"

    df_xr.to_netcdf(save_dir + f"FMI.{instrument}.b1." + save_time + ".nc")
    print(f"Saved {save_time}.nc")

# %%
