import pandas as pd
import glob
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LogNorm
import json
import preprocess
import string

data_path = r'C:\Users\le\OneDrive - Ilmatieteen laitos\Campaigns\Pace2022\FMI balloon payload\Processed_data/'
with open('mcda_midbin_all.txt', 'r') as file: 
    mcda_midbin_all = json.loads(file.read())

# %%
pop_binedges = np.loadtxt('pops_binedges.txt')
pop_midbin = (pop_binedges[1:] + pop_binedges[:-1])/2

fig, ax = plt.subplots(2, 21, sharey='row', sharex='col', figsize=(10, 6))
fig.subplots_adjust(wspace=0, hspace=0)

for file, ax0_, (i, ax_) in zip(glob.glob(data_path + '*.csv'),
                          ax[0, :].flatten(),
                          enumerate(ax[1, :].flatten())):
    df = pd.read_csv(file)
    df['datetime'] = pd.to_datetime(df['datetime'])
    df.replace(-9999.9, np.nan, inplace=True)

    ax0_.plot(df['datetime'], df['N_conc_cpc(1/ccm)'], '.')
    ax0_.grid()
    ax0_.set_yscale('log')

    p = ax_.pcolormesh(df['datetime'],
                            pop_midbin,
                            df[[x for x in df.columns if '_pops (dN/dlogDp)' in x]].T,
                            norm=LogNorm(vmax=10, vmin=0.01),
                            cmap='jet')
    ax_.set_yscale('log')
    ax_.set_xticks([])
    # ax_.set_xlabel(f"#{i+1}")
    ax_.set_xlabel(df.iloc[0].datetime.strftime('%d/%m\n %H:%M'), size=7)

ax[1, 0].set_ylabel(r'Size ($\mu m$)')
ax[0, 0].set_ylabel(r'N_conc_cpc(1/ccm)')
fig.colorbar(p, ax=ax, orientation='horizontal', label=r'dN/dlogDp ($cm^{-3}$)', aspect=50)
fig.savefig(r"C:\Users\le\OneDrive - Ilmatieteen laitos\My_articles\2024\Pallas/pops_ts.png", dpi=600,
            bbox_inches='tight')

# %%
fig, ax = plt.subplots(3, 21, sharey='row', sharex='col', figsize=(10, 6))
fig.subplots_adjust(wspace=0, hspace=0.2)

for file, ax_cpc, ax_pops, ax_mcda  in zip(glob.glob(data_path + '*.csv'),
                          ax[0, :].flatten(),
                          ax[1, :].flatten(),
                          ax[2, :].flatten()):
    df = pd.read_csv(file)
    df['datetime'] = pd.to_datetime(df['datetime'])
    df.replace(-9999.9, np.nan, inplace=True)

    ax_cpc.plot(df['datetime'], df['N_conc_cpc(1/ccm)'], '.',
                markeredgecolor='none', markersize=1.0)
    ax_cpc.grid()
    ax_cpc.set_xticks([])
    ax_cpc.set_yscale('log')
    ax_cpc.set_ylim(1e1, 1e4)

    ax_pops.plot(df['datetime'], df['N_conc_pops (1/ccm)'], '.',
                 markeredgecolor='none', markersize=1.0)
    ax_pops.grid()
    ax_pops.set_xticks([])
    ax_pops.set_yscale('log')
    ax_pops.set_ylim(top=1e3)

    ax_mcda.plot(df['datetime'], df['Nd_mcda (1/ccm)'], '.',
                 markeredgecolor='none', markersize=2.0)
    ax_mcda.grid()
    ax_mcda.set_xticks([])
    ax_mcda.set_xlabel(df.iloc[0].datetime.strftime('%d/%m\n %H:%M'), size=7)
    ax_mcda.set_yscale('log')

for n, ax_ in enumerate(ax[:, 0].flatten()):
    ax_.text(-0.0, 1.05, '(' + string.ascii_lowercase[n] + ')',
        transform=ax_.transAxes, size=12)

ax[0, 0].set_ylabel(r'$N$ ($cm^{-3}$)')
ax[1, 0].set_ylabel(r'$N$ ($cm^{-3}$)')
ax[2, 0].set_ylabel(r'$N_d$ ($cm^{-3}$)')
fig.savefig(r"C:\Users\le\OneDrive - Ilmatieteen laitos\My_articles\2024\Pallas/conc_ts.png", dpi=600,
            bbox_inches='tight')

# %%
fig, ax = plt.subplots(3, 21, sharey='row', sharex='col', figsize=(10, 6.5))
fig.subplots_adjust(wspace=0, hspace=0.1)

for file, ax0, ax1, ax2  in zip(glob.glob(data_path + '*.csv'),
                          ax[0, :].flatten(),
                          ax[1, :].flatten(),
                          ax[2, :].flatten()):
    df = pd.read_csv(file)
    df['datetime'] = pd.to_datetime(df['datetime'])
    df.replace(-9999.9, np.nan, inplace=True)

    ax0.plot(df['datetime'], df['press_bme (hPa)'], '.',
                markeredgecolor='none', markersize=2.0)
    ax0.grid()
    ax0.set_xticks([])

    ax1.plot(df['datetime'], df['temp_bme (C)'], '.',
                 markeredgecolor='none', markersize=2.0)
    ax1.grid()
    ax1.set_xticks([])

    ax2.plot(df['datetime'], df['rh_bme (%)'], '.',
                 markeredgecolor='none', markersize=2.0)
    ax2.grid()
    ax2.set_xticks([])
    ax2.set_xlabel(df.iloc[0].datetime.strftime('%d/%m\n %H:%M'), size=7)

ax[0, 0].set_ylabel('press_bme (hPa)')
ax[1, 0].set_ylabel('temp_bme (C)')
ax[2, 0].set_ylabel('rh_bme (%)')
fig.savefig(r"C:\Users\le\OneDrive - Ilmatieteen laitos\My_articles\2024\Pallas/meteorology_ts.png", dpi=600,
            bbox_inches='tight')

# %%
fig, ax = plt.subplots(4, 21, sharey='row', sharex='col', figsize=(10, 10))
fig.subplots_adjust(wspace=0, hspace=0.2)

for file, ax0, ax1, ax2, ax3  in zip(glob.glob(data_path + '*.csv'),
                          ax[0, :].flatten(),
                          ax[1, :].flatten(),
                          ax[2, :].flatten(),
                          ax[3, :].flatten()):
    df = pd.read_csv(file)
    df['datetime'] = pd.to_datetime(df['datetime'])
    df.replace(-9999.9, np.nan, inplace=True)
    if df['datetime'][0] < pd.Timestamp('20221003', tz='UTC'):
        size = 'water_0.15-17'
    else:
        size = 'water_0.6-40'
    cda_midbin = preprocess.mcda_midbin_all[size]
    cda_midbin = cda_midbin[81:]
    df.dropna(subset=[x for x in df.columns if '_mcda (dN/dlogDp)' in x], inplace=True)
    df.reset_index(drop=True, inplace=True)

    ax0.plot(df['datetime'], df['LWC_mcda (g/m3)'], '.',
                markeredgecolor='none', markersize=2.0)
    ax0.grid()
    ax0.set_xticks([])
    ax0.set_yscale('log')

    p = ax3.pcolormesh(df.datetime, cda_midbin,
                         df[[x for x in df.columns if '_mcda (dN/dlogDp)' in x]].T,
                         norm=LogNorm(vmax=10, vmin=0.01), cmap='jet')
    ax3.set_yscale('log')
    ax3.grid()
    ax3.set_xlabel(df.iloc[0].datetime.strftime('%d/%m\n %H:%M'), size=7)
    ax3.set_xticks([])
    
    ax1.plot(df['datetime'], df['MVD_mcda (um)'], '.',
                 markeredgecolor='none', markersize=2.0)
    ax1.grid()
    ax1.set_xticks([])
    ax1.set_yscale('log')
    ax1.set_ylim(ax3.get_ylim())

    ax2.plot(df['datetime'], df['ED_mcda (um)'], '.',
                 markeredgecolor='none', markersize=2.0)
    ax2.grid()
    ax2.set_xticks([])
    ax2.set_yscale('log')
    ax2.set_ylim(ax3.get_ylim())

for n, ax_ in enumerate(ax[:, 0].flatten()):
    ax_.text(-0.0, 1.05, '(' + string.ascii_lowercase[n] + ')',
        transform=ax_.transAxes, size=12)

fig.colorbar(p, ax=ax, orientation='horizontal', label=r'dN/dlogDp ($cm^{-3}$)', aspect=50, pad=0.05)
ax[0, 0].set_ylabel(r'LWC $(g/m^3)$')
ax[1, 0].set_ylabel(r'MVD $(\mu m)$')
ax[2, 0].set_ylabel(r'ED $(\mu m)$')
ax[3, 0].set_ylabel(r'Size ($\mu m$)')

fig.savefig(r"C:\Users\le\OneDrive - Ilmatieteen laitos\My_articles\2024\Pallas/cloud_properties_ts.png", dpi=600,
            bbox_inches='tight')