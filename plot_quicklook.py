from matplotlib.colors import LogNorm
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import string
import pytz
import json

pop_binedges = np.loadtxt('pops_binedges.txt')
pop_midbin = (pop_binedges[1:] + pop_binedges[:-1])/2

with open('mcda_midbin_all.txt', 'r') as file: 
    mcda_midbin_all = json.loads(file.read())

def plot_quicklook(df):

    if df['datetime'][0] < pd.Timestamp('20221003', tz='UTC'):
        size = 'water_0.15-17'
    else:
        size = 'water_0.6-40'
    cda_midbin = np.array(mcda_midbin_all[size], dtype=float)
    cda_midbin = cda_midbin[81:]
    fig, ax = plt.subplot_mosaic([
        ['press', 'mcda'],
        ['temp', 'mcda'],
        ['RH', 'pop'],
        ['cpc', 'pop']
    ],
    figsize=(9, 6), sharex=True, constrained_layout=True)

    ax['press'].plot(df['datetime'], df['press_bme (hPa)'], '.')
    ax['press'].set_ylabel('press_bme (hPa)')
    ax['press'].grid()

    ax['temp'].plot(df['datetime'], df['temp_bme (C)'], '.')
    ax['temp'].set_ylabel(r'temp_bme (C)')
    ax['temp'].grid()

    ax['RH'].plot(df['datetime'], df['rh_bme (%)'], '.')
    ax['RH'].set_ylabel(r'rh_bme (%)')
    ax['RH'].grid()

    ax['cpc'].plot(df['datetime'], df['N_conc_cpc(1/ccm)'], '.')
    ax['cpc'].set_ylabel(r'N_conc_cpc(1/ccm)')
    ax['cpc'].grid()
    ax['cpc'].set_yscale('log')

    grp_avg = df.set_index('datetime').resample('5min').mean().reset_index()
    p = ax['mcda'].pcolormesh(grp_avg['datetime'],
                              cda_midbin,
                              grp_avg[[x for x in df.columns if '_mcda (dN/dlogDp)' in x]].T,
                              norm=LogNorm(vmax=10, vmin=0.01),
                              cmap='jet')
    ax['mcda'].set_yscale('log')
    ax['mcda'].set_ylabel(r'Size ($\mu m$)')
    cbar = fig.colorbar(p, ax=ax['mcda'])
    cbar.ax.set_ylabel(r'dN/dlogDp ($cm^{-3}$) miniCDA', rotation=90)

    p = ax['pop'].pcolormesh(grp_avg['datetime'],
                             pop_midbin,
                             grp_avg[[x for x in df.columns if '_pops (dN/dlogDp)' in x]].T,
                             norm=LogNorm(vmax=10, vmin=0.01),
                             cmap='jet')
    ax['pop'].set_yscale('log')
    ax['pop'].set_xlim(ax['mcda'].get_xlim())
    ax['pop'].set_ylabel(r'Size ($\mu m$)')
    cbar = fig.colorbar(p, ax=ax['pop'])
    cbar.ax.set_ylabel(r'dN/dlogDp ($cm^{-3}$) POP', rotation=90)

    ax['cpc'].set_xlabel('Time (UTC)')
    ax['pop'].set_xlabel('Time (UTC)')

    for n, (_, ax_) in enumerate(ax.items()):
        ax_.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M', tz=pytz.timezone('UTC')))
        ax_.xaxis.set_tick_params(labelbottom=True)
        ax_.text(-0.0, 1.05, '(' + string.ascii_lowercase[n] + ')',
            transform=ax_.transAxes, size=12)
    return fig

file_path = r'C:\Users\le\OneDrive - Ilmatieteen laitos\Campaigns\Pace2022\FMI balloon payload\Processed_data/'

file_list = glob.glob(file_path + '*.csv')
for file in file_list:
    df = pd.read_csv(file)
    df['datetime'] = pd.to_datetime(df['datetime'])
    df = df.replace(-9999.9, np.nan)
    fig = plot_quicklook(df)
    save_time = df.datetime[0].strftime("%Y%m%d_%H%M")
    fig.savefig(file_path + 'quicklook' + save_time + '.png', dpi=500)
    plt.close()
    print(f'Plot {save_time} saved')