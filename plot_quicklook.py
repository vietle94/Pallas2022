from matplotlib.colors import LogNorm
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import string
import json

pops_binedges = np.loadtxt('pops_binedges.txt')
pops_midbin = (pops_binedges[1:] + pops_binedges[:-1])/2

with open('mcda_midbin_all.txt', 'r') as file: 
    mcda_midbin_all = json.loads(file.read())

def plot_quicklook(df):

    if df['datetime (utc)'][0] < pd.Timestamp('20221003'):
        size = 'water_0.15-17'
    else:
        size = 'water_0.6-40'
    cda_midbin = np.array(mcda_midbin_all[size], dtype=float)
    cda_midbin = cda_midbin[81:]
    fig, ax = plt.subplot_mosaic([
        ['press', 'mcda'],
        ['temp', 'mcda'],
        ['RH', 'pops'],
        ['cpc', 'pops']
    ],
    figsize=(9, 6), sharex=True, constrained_layout=True)

    ax['press'].plot(df['datetime (utc)'], df['height_bme (m)'], '.')
    ax['press'].set_ylabel(r'Height a.g.l $(m)$')
    ax['press'].grid()

    ax['temp'].plot(df['datetime (utc)'], df['temp_bme (C)'], '.')
    ax['temp'].set_ylabel(r'$T$ $(\degree C)$')
    ax['temp'].grid()

    ax['RH'].plot(df['datetime (utc)'], df['rh_bme (%)'], '.', label="Ambient")
    ax['RH'].plot(df['datetime (utc)'], df['rh_pops (%)'], '.', label="Internal_POPS")
    ax['RH'].set_ylabel(r'$RH$ $(\%)$')
    ax['RH'].grid()
    ax['RH'].legend()

    ax['cpc'].plot(df['datetime (utc)'], df['N_conc_cpc (cm-3)'], '.')
    ax['cpc'].set_ylabel(r'$N$ ($cm^{-3}$)')
    ax['cpc'].grid()
    ax['cpc'].set_yscale('log')

    grp_avg = df.set_index('datetime (utc)').resample('5min').mean().reset_index()
    p = ax['mcda'].pcolormesh(grp_avg['datetime (utc)'],
                              cda_midbin,
                              grp_avg[[x for x in df.columns if '_mcda (dN/dlogDp)' in x]].T,
                              norm=LogNorm(vmax=10, vmin=0.01),
                              cmap='jet')
    ax['mcda'].set_yscale('log')
    ax['mcda'].set_ylabel(r'Size ($\mu m$)')
    cbar = fig.colorbar(p, ax=ax['mcda'])
    cbar.ax.set_ylabel(r'dN/dlogDp ($cm^{-3}$)', rotation=90)

    p = ax['pops'].pcolormesh(grp_avg['datetime (utc)'],
                             pops_midbin,
                             grp_avg[[x for x in df.columns if '_pops (dN/dlogDp)' in x]].T,
                             norm=LogNorm(vmax=10, vmin=0.01),
                             cmap='jet')
    ax['pops'].set_yscale('log')
    ax['pops'].set_xlim(ax['mcda'].get_xlim())
    ax['pops'].set_ylabel(r'Size ($\mu m$)')
    cbar = fig.colorbar(p, ax=ax['pops'])
    cbar.ax.set_ylabel(r'dN/dlogDp ($cm^{-3}$)', rotation=90)

    ax['cpc'].set_xlabel('Time (Hour, UTC)')
    ax['pops'].set_xlabel('Time (Hour, UTC)')

    for n, (_, ax_) in enumerate(ax.items()):
        ax_.xaxis.set_major_formatter(mdates.DateFormatter('%H'))
        ax_.xaxis.set_major_locator(mdates.HourLocator(interval=1))
        ax_.xaxis.set_major_locator
        ax_.xaxis.set_tick_params(labelbottom=True)
        ax_.text(-0.0, 1.05, '(' + string.ascii_lowercase[n] + ')',
            transform=ax_.transAxes, size=12)
    return fig, ax

file_path = r'C:\Users\le\OneDrive - Ilmatieteen laitos\Campaigns\Pace2022\FMI balloon payload\Processed_data/'

file_list = glob.glob(file_path + '*.csv')
for file in file_list:
    df = pd.read_csv(file)
    df['datetime (utc)'] = pd.to_datetime(df['datetime (utc)'])
    df = df[df['winch_contamination'] < 1]
    df = df.reset_index(drop=True)
    df = df.replace(-9999.9, np.nan)
    fig, _ = plot_quicklook(df)
    save_time = df['datetime (utc)'][0].strftime("%Y%m%d_%H%M")
    fig.savefig(file_path + 'quicklook' + save_time + '.png', dpi=500)
    plt.close()
    print(f'Plot {save_time} saved')