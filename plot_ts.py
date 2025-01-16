import pandas as pd
import glob
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LogNorm
import json

data_path = r'C:\Users\le\OneDrive - Ilmatieteen laitos\Campaigns\Pace2022\FMI balloon payload\Processed_data/'
with open('mcda_sizes.txt', 'r') as file: 
    mcda_sizes = json.loads(file.read())
# %%
fig, ax = plt.subplots(1, 21, sharey=True, figsize=(10, 4))
fig.subplots_adjust(wspace=0)
for file, (i, ax_) in zip(glob.glob(data_path + '*.csv'),
                     enumerate(ax.flatten())):
    df = pd.read_csv(file)
    df['datetime'] = pd.to_datetime(df['datetime'])
    df.replace(-9999.9, np.nan, inplace=True)
    grp_avg = df.set_index('datetime').resample('5min').mean().reset_index()

    if df['datetime'][0] < pd.Timestamp('20221003', tz='UTC'):
        size = 'water_0.15-17'
    else:
        size = 'water_0.6-40'
    cda_midbin = np.array(mcda_sizes[size], dtype=float)
    cda_midbin = cda_midbin[81:]
    p = ax_.pcolormesh(grp_avg['datetime'],
                            cda_midbin,
                            grp_avg[[x for x in df.columns if '_mcda (dN/dlogDp)' in x]].T,
                            norm=LogNorm(vmax=10, vmin=0.01),
                            cmap='jet')
    ax_.set_yscale('log')
    ax_.set_xticks([])
    ax_.set_xlabel(df.iloc[0].datetime.strftime('%d/%m\n %H:%M'), size=7)

ax[0].set_ylabel(r'Size ($\mu m$)')
fig.colorbar(p, ax=ax, orientation='horizontal', label=r'dN/dlogDp ($cm^{-3}$)', aspect=50)
fig.savefig(r"C:\Users\le\OneDrive - Ilmatieteen laitos\My_articles\2024\Pallas/mcda_ts.png", dpi=600,
            bbox_inches='tight')
# %%
pop_binedges = '0.119552706	0.140894644	0.169068337	0.204226949	0.227523895	0.253291842	0.279285719	0.35426882	0.604151175	0.705102841	0.785877189	1.100686925	1.117622254	1.765832382	2.690129739	3.014558062 4.392791391'
pop_binedges = np.fromstring(pop_binedges, dtype=float, sep="\t")
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
fig, ax = plt.subplots(3, 21, sharey='row', sharex='col', figsize=(10, 6.5))
fig.subplots_adjust(wspace=0, hspace=0.1)

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

ax[0, 0].set_ylabel('N_conc_cpc(1/ccm)')
ax[1, 0].set_ylabel('N_conc_pops (1/ccm)')
ax[2, 0].set_ylabel('Nd_mcda (1/ccm)')
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

    ax0.plot(df['datetime'], df['LWC_mcda (g/m3)'], '.',
                markeredgecolor='none', markersize=2.0)
    ax0.grid()
    ax0.set_xticks([])
    ax0.set_yscale('log')

    ax1.plot(df['datetime'], df['MVD_mcda (um)'], '.',
                 markeredgecolor='none', markersize=2.0)
    ax1.grid()
    ax1.set_xticks([])
    ax1.set_yscale('log')
    ax1.set_ylim(1e0, 1e3)

    ax2.plot(df['datetime'], df['ED_mcda (um)'], '.',
                 markeredgecolor='none', markersize=2.0)
    ax2.grid()
    ax2.set_xticks([])
    ax2.set_xlabel(df.iloc[0].datetime.strftime('%d/%m\n %H:%M'), size=7)
    ax2.set_yscale('log')
    ax2.set_ylim(1e0, 1e3)

ax[0, 0].set_ylabel('LWC_mcda (g/m3)')
ax[1, 0].set_ylabel('MVD_mcda (um)')
ax[2, 0].set_ylabel('ED_mcda (um)')
fig.savefig(r"C:\Users\le\OneDrive - Ilmatieteen laitos\My_articles\2024\Pallas/cloud_properties_ts.png", dpi=600,
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