import xarray as xr
import glob
import pandas as pd
from UAVision.preprocess import pops_binedges, calculate_midbin, mcda_midbin_all
import re

csv_dir = r'C:\Users\le\OneDrive - Ilmatieteen laitos\Campaigns\Pace2022\FMI balloon payload\Processed_data/'
csv_files = glob.glob(csv_dir + '*.csv')
pops_midbin = calculate_midbin(pops_binedges)
for file in csv_files:
    df = pd.read_csv(file)
    df['datetime (utc)'] = pd.to_datetime(df['datetime (utc)'])
    df = df.rename(columns={'datetime (utc)': 'datetime'})
    save_time = df.iloc[0]["datetime"].strftime("%Y%m%d.%H%M")
    if df['datetime'][0] < pd.Timestamp('20221003'):
        size = 'water_0.15-17'
        mcda_midbin = mcda_midbin_all[size]
        mcda_midbin = mcda_midbin[81:]
    else:
        size = 'water_0.6-40'
        mcda_midbin = mcda_midbin_all[size]
        mcda_midbin = mcda_midbin[81:]

    if df['datetime'][0] < pd.Timestamp('20220924'):
        platform = "Helikites"
    else:
        platform = "Aerostat"

    df_xr = xr.Dataset.from_dataframe(df.set_index('datetime'))
    df_xr["conc_pops (cm-3)"] = xr.concat(
            [df_xr[f"bin{x}_pops (cm-3)"] for x in range(1, 17)], pops_midbin
        ).T
    df_xr["conc_pops_dNdlogDp"] = xr.concat(
            [df_xr[f"bin{x}_pops (dN/dlogDp)"] for x in range(1, 17)], pops_midbin
        ).T
    df_xr = df_xr.rename({"concat_dim": "pops_midbin"})

    df_xr["conc_mcda (cm-3)"] = xr.concat(
            [df_xr[f"bin{x}_mcda (cm-3)"] for x in range(1, 176)], mcda_midbin
        ).T
    df_xr["conc_mcda_dNdlogDp"] = xr.concat(
            [df_xr[f"bin{x}_mcda (dN/dlogDp)"] for x in range(1, 176)], mcda_midbin
        ).T
    df_xr = df_xr.rename({"concat_dim": "mcda_midbin"})
    df_xr = df_xr[['temp_bme (C)',
                    'press_bme (hPa)',
                    'rh_bme (%)',
                    'N_conc_cpc (cm-3)',
                    'press_cpc (hPa)',
                    'N_conc_pops (cm-3)',
                    'press_pops (hPa)',
                    'flow_rate_pops (l/m)',
                    'conc_pops (cm-3)',
                    'conc_pops_dNdlogDp',
                    'conc_mcda (cm-3)',
                    'conc_mcda_dNdlogDp',
                    'pm1_mcda',
                    'pm25_mcda',
                    'pm10_mcda',
                    'Nd_mcda (cm-3)',
                    'LWC_mcda (g/m3)',
                    'MVD_mcda (um)',
                    'ED_mcda (um)']]
    df_xr = df_xr.rename({x:re.sub(r" \(.*\)", "", x) for x in list(df_xr.data_vars)})

    df_xr['datetime'].attrs = {'long_name': 'datetime in UTC', '_FillValue': -9999.9, 'processing_level': 'b1'}
    df_xr['pops_midbin'].attrs = {'units': 'µm', 'long_name': 'centers of the size bins from POPS', '_FillValue': -9999.9, 'processing_level': 'b1'}
    df_xr['mcda_midbin'].attrs = {'units': 'µm', 'long_name': 'centers of the size bins from mCDA', '_FillValue': -9999.9, 'processing_level': 'b1'}
    df_xr['temp_bme'].attrs = {'units': 'degree Celsius', 'long_name': 'Temperature measured by BME280', '_FillValue': -9999.9, 'processing_level': 'b1'}
    df_xr['press_bme'].attrs = {'units': 'hPa', 'long_name': 'Pressure measured by BME280', '_FillValue': -9999.9, 'processing_level': 'b1'}
    df_xr['rh_bme'].attrs = {'units': '%', 'long_name': 'Relative humidity measured by BME280', '_FillValue': -9999.9, 'processing_level': 'b1'}
    df_xr['N_conc_cpc'].attrs = {'units': 'cm-3', 'long_name': 'Total particle concentration measured by CPC', '_FillValue': -9999.9, 'processing_level': 'b1'}
    df_xr['press_cpc'].attrs = {'units': 'hPa', 'long_name': 'Inlet pressure measured by CPC', '_FillValue': -9999.9, 'processing_level': 'b1'}
    df_xr['N_conc_pops'].attrs = {'units': 'cm-3', 'long_name': 'Total particle concentration measured by POPS', '_FillValue': -9999.9, 'processing_level': 'b1'}
    df_xr['press_pops'].attrs = {'units': 'hPa', 'long_name': 'Inlet pressure measured by POPS', '_FillValue': -9999.9, 'processing_level': 'b1'}
    df_xr['flow_rate_pops'].attrs = {'units': 'L/m', 'long_name': 'Inlet flow rate measured by POPS', '_FillValue': -9999.9, 'processing_level': 'b1'}
    df_xr['conc_pops'].attrs = {'units': 'cm-3', 'long_name': 'Particle concentration measured by POPS', '_FillValue': -9999.9, 'processing_level': 'b1'}
    df_xr['conc_pops_dNdlogDp'].attrs = {'units': 'cm-3', 'long_name': 'Normalized particle concentration measured by POPS in dN/dlogDp', '_FillValue': -9999.9, 'processing_level': 'b1'}
    df_xr['conc_mcda'].attrs = {'units': 'cm-3', 'long_name': 'Particle concentration measured by mCDA', '_FillValue': -9999.9, 'processing_level': 'b1'}
    df_xr['conc_mcda_dNdlogDp'].attrs = {'units': 'cm-3', 'long_name': 'Particle concentration measured by mCDA in dN/dlogDp', '_FillValue': -9999.9, 'processing_level': 'b1'}
    df_xr['pm1_mcda'].attrs = {'units': 'µg cm−3', 'long_name': 'Particulate Matter with diameters less than 1µm measured by mCDA', '_FillValue': -9999.9, 'processing_level': 'b1'}
    df_xr['pm25_mcda'].attrs = {'units': 'µg cm−3', 'long_name': 'Particulate Matter with diameters less than 2.5µm measured by mCDA', '_FillValue': -9999.9, 'processing_level': 'b1'}
    df_xr['pm10_mcda'].attrs = {'units': 'µg cm−3', 'long_name': 'Particulate Matter with diameters less than 10µm measured by mCDA', '_FillValue': -9999.9, 'processing_level': 'b1'}
    df_xr['Nd_mcda'].attrs = {'units': 'cm-3', 'long_name': 'Total cloud droplet concentration measured by mCDA', '_FillValue': -9999.9, 'processing_level': 'b1'}
    df_xr['LWC_mcda'].attrs = {'units': 'g m−3', 'long_name': 'Liquid water content measured by mCDA', '_FillValue': -9999.9, 'processing_level': 'b1'}
    df_xr['MVD_mcda'].attrs = {'units': 'µm', 'long_name': 'Median volume diameter measured by mCDA', '_FillValue': -9999.9, 'processing_level': 'b1'}
    df_xr['ED_mcda'].attrs = {'units': 'µm', 'long_name': 'Effective droplet diameter measured by mCDA', '_FillValue': -9999.9, 'processing_level': 'b1'}

    df_xr.attrs['platform_name'] = platform
    df_xr.attrs['institution'] = "Finnish Meteorological Institute"
    df_xr.attrs['source'] = "PaCE2022 campaign"
    df_xr.attrs['processing_level'] = "b1"
    df_xr.attrs['created by'] = "Viet Le"

    df_xr.to_netcdf(csv_dir + "FMI.DBP.b1." + save_time + ".nc")
    print(f"Saved {save_time}.nc")
