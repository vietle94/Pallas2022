import pandas as pd
import glob
import matplotlib.pyplot as plt
import numpy as np
import json
import string

data_path = r'C:\Users\le\OneDrive - Ilmatieteen laitos\Campaigns\Pace2022\FMI balloon payload\Processed_data/'
pops_binedges = np.loadtxt('pops_binedges.txt')
pops_midbin = (pops_binedges[1:] + pops_binedges[:-1])/2
with open('mcda_midbin_all.txt', 'r') as file: 
    mcda_midbin_all = json.loads(file.read())

# %%
for file in glob.glob(data_path + '*.csv'):
    df = pd.read_csv(file)
    df['datetime (utc)'] = pd.to_datetime(df['datetime (utc)'])
    df.replace(-9999.9, np.nan, inplace=True)
    df = df.reset_index(drop=True)
    if df['datetime (utc)'][0] < pd.Timestamp('20221003'):
        size = 'PSL_0.15-17'
    else:
        size = 'PSL_0.6-40'
    print(size)
    cda_midbin = np.array(mcda_midbin_all[size], dtype=float)
    cda_midbin = cda_midbin[81:]

    lower_bound = np.max([pops_midbin.min(), cda_midbin.min()])
    upper_bound = np.min([pops_midbin.max(), cda_midbin.max()])

    cda_mask = (cda_midbin > lower_bound) & (cda_midbin < upper_bound)
    cda_col = np.array([x for x in df.columns if '_mcda (cm-3)' in x and 'Nd' not in x])
    cda_overlap = df[cda_col[cda_mask]].sum(axis=1)

    pops_mask = (pops_midbin > lower_bound) & (pops_midbin < upper_bound)
    pops_col = np.array([x for x in df.columns if '_pops (cm-3)' in x and 'N_conc' not in x])
    pops_overlap = df[pops_col[pops_mask]].sum(axis=1)
    fig, ax = plt.subplots(3, 1, figsize=(9, 6), sharex=True)
    ax[0].plot(df['datetime (utc)'], df['height_bme (m)'], '.')
    ax[0].set_ylabel('Height (m)')
    # ax[0].set_ylim(0, 200)
    ax[1].plot(df['datetime (utc)'], df['flow_rate_pops (cm3/s)'], '.')
    ax[1].set_ylim(0, 10)
    ax[1].set_ylabel('Flow rate (cm$^3$/s)')
    # ax[2].plot(df['datetime (utc)'], cda_overlap, '.', label='mCDA')
    # ax[2].plot(df['datetime (utc)'], df['N_conc_cpc (cm-3)'], '.', label='CPC')
    # ax[2].plot(df['datetime (utc)'], pops_overlap, '.', label='POPS')
    ax[2].plot(df['datetime (utc)'], df['N_conc_cpc (cm-3)'], '.', label='CPC')
    ax[2].plot(df['datetime (utc)'], df['N_conc_pops (cm-3)'], '.', label='POPS')
    ax[2].plot(df['datetime (utc)'], 
        df[[x for x in df.columns if '_mcda (cm-3)' in x and 'Nd' not in x]].sum(axis=1), '.', label='mCDA')
    ax[2].set_ylabel(r'N (cm$^{-3}$)')
    ax[2].set_yscale('log')
    ax[2].set_ylim(1e-2, 4e3)
    ax[2].legend(loc='lower right')
    ax[2].set_xlabel('Time (Hour, UTC)')
    for n, ax_ in enumerate(ax.flatten()):
        ax_.grid()
        ax_.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m-%d\n%H:%M'))
        ax_.text(
            -0.0,
            1.05,
            "(" + string.ascii_lowercase[n] + ")",
            transform=ax_.transAxes,
            size=12,
        )

# %%
# file = [file for file in glob.glob(data_path + '*.csv') if '20220922' in file][0]
file = [file for file in glob.glob(data_path + '*.csv') if '20220920' in file][0]
df = pd.read_csv(file)
df['datetime (utc)'] = pd.to_datetime(df['datetime (utc)'])
df.replace(-9999.9, np.nan, inplace=True)
df = df.reset_index(drop=True)
if df['datetime (utc)'][0] < pd.Timestamp('20221003'):
    size = 'PSL_0.15-17'
else:
    size = 'PSL_0.6-40'
print(size)
cda_midbin = np.array(mcda_midbin_all[size], dtype=float)
cda_midbin = cda_midbin[81:]
save_date = df['datetime (utc)'].dt.strftime('%Y%m%d').values[0]

# %%
fig, ax = plt.subplots(3, 1, sharex=True, figsize=(9, 6), constrained_layout=True)

ax[0].plot(df['datetime (utc)'], df['height_bme (m)'], '.')
ax[0].set_ylabel('Height (m)')
# ax[0].set_ylim(0, 200)
ax[1].plot(df['datetime (utc)'], df['flow_rate_pops (cm3/s)'], '.')
ax[1].set_ylim(0, 10)
ax[1].set_ylabel('Flow rate (cm$^3$/s)')
# ax[2].plot(df['datetime (utc)'], cda_overlap, '.', label='mCDA')
# ax[2].plot(df['datetime (utc)'], df['N_conc_cpc (cm-3)'], '.', label='CPC')
# ax[2].plot(df['datetime (utc)'], pops_overlap, '.', label='POPS')
ax[2].plot(df['datetime (utc)'], df['N_conc_cpc (cm-3)'], '.', label='CPC')
ax[2].plot(df['datetime (utc)'], df['N_conc_pops (cm-3)'], '.', label='POPS')
ax[2].plot(df['datetime (utc)'], 
    df[[x for x in df.columns if '_mcda (cm-3)' in x and 'Nd' not in x]].sum(axis=1), '.', label='mCDA')
ax[2].set_ylabel(r'N (cm$^{-3}$)')
ax[2].set_yscale('log')
ax[2].set_ylim(1e-2, 4e3)
ax[2].legend(loc='lower right')
ax[2].set_xlabel('Time (Hour, UTC)')
for n, ax_ in enumerate(ax.flatten()):
    ax_.grid()
    ax_.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%H:%M'))
    ax_.text(
        -0.0,
        1.05,
        "(" + string.ascii_lowercase[n] + ")",
        transform=ax_.transAxes,
        size=12,
    )
fig.savefig(rf"C:\Users\le\OneDrive - Ilmatieteen laitos\PaCE_2022\ESSD special issue\Viet_et_al_2025\Ver2\Editor_reply/cpc_pops_mcda_{save_date}.png",
            dpi=300, bbox_inches='tight')

# # %%
# fig, ax = plt.subplots(3, 1, sharex=True, figsize=(9, 6), constrained_layout=True)

# ax[0].plot(df['datetime (utc)'], df['height_bme (m)'], '.')
# ax[0].set_ylabel('Height (m)')
# # ax[0].set_ylim(0, 200)
# ax[1].plot(df['datetime (utc)'], df['flow_rate_pops (cm3/s)'], '.')
# ax[1].set_ylim(0, 10)
# ax[1].set_ylabel('Flow rate (cm$^3$/s)')
# # ax[2].plot(df['datetime (utc)'], cda_overlap, '.', label='mCDA')
# # ax[2].plot(df['datetime (utc)'], df['N_conc_cpc (cm-3)'], '.', label='CPC')
# # ax[2].plot(df['datetime (utc)'], pops_overlap, '.', label='POPS')
# ax[2].plot(df['datetime (utc)'], df['N_conc_cpc (cm-3)'], '.', label='CPC')
# ax[2].plot(df['datetime (utc)'], df['N_conc_pops (cm-3)'], '.', label='POPS')
# ax[2].plot(df['datetime (utc)'], 
#     df[[x for x in df.columns if '_mcda (cm-3)' in x and 'Nd' not in x]].sum(axis=1), '.', label='mCDA')
# ax[2].set_ylabel(r'N (cm$^{-3}$)')
# ax[2].set_yscale('log')
# ax[2].set_ylim(1e-2, 4e3)
# ax[2].legend(loc='lower right')
# ax[2].set_xlabel('Time (Hour, UTC)')
# for n, ax_ in enumerate(ax.flatten()):
#     ax_.grid()
#     ax_.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%H:%M'))
#     ax_.text(
#         -0.0,
#         1.05,
#         "(" + string.ascii_lowercase[n] + ")",
#         transform=ax_.transAxes,
#         size=12,
#     )
# # ax[0].set_xlim(pd.Timestamp('2022-09-22 09:00'), pd.Timestamp('2022-09-22 09:10'))
# ax[0].set_xlim(pd.Timestamp('2022-09-20 07:10'), pd.Timestamp('2022-09-20 07:30'))
# fig.savefig(rf"C:\Users\le\OneDrive - Ilmatieteen laitos\PaCE_2022\ESSD special issue\Viet_et_al_2025\Ver2\Editor_reply/cpc_pops_mcda_zoomed_{save_date}.png", dpi=300, bbox_inches='tight')

# %%
fig, ax = plt.subplots(figsize=(9, 3), constrained_layout=True)


# ax[2].plot(df['datetime (utc)'], cda_overlap, '.', label='mCDA')
# ax[2].plot(df['datetime (utc)'], df['N_conc_cpc (cm-3)'], '.', label='CPC')
# ax[2].plot(df['datetime (utc)'], pops_overlap, '.', label='POPS')
ax.plot(df['datetime (utc)'], df['N_conc_cpc (cm-3)'], '.', label='CPC')
ax.plot(df['datetime (utc)'], df['N_conc_pops (cm-3)'], '.', label='POPS')
ax.plot(df['datetime (utc)'], 
    df[[x for x in df.columns if '_mcda (cm-3)' in x and 'Nd' not in x]].sum(axis=1), '.', label='mCDA')
ax.set_ylabel(r'N (cm$^{-3}$)')
ax.set_yscale('log')
ax.set_ylim(1e-2, 4e3)
ax.legend(loc='lower right')
ax.set_xlabel('Time (Hour, UTC)')
ax.grid()
ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%H:%M'))
# ax[0].set_xlim(pd.Timestamp('2022-09-22 09:00'), pd.Timestamp('2022-09-22 09:10'))
ax.set_xlim(pd.Timestamp('2022-09-20 08:00'), pd.Timestamp('2022-09-20 08:10'))
fig.savefig(rf"C:\Users\le\OneDrive - Ilmatieteen laitos\PaCE_2022\ESSD special issue\Viet_et_al_2025\Ver2\Editor_reply/cpc_pops_mcda_zoomed_{save_date}.png", dpi=300, bbox_inches='tight')

# %%
t0 = pd.Timestamp('2022-09-22 08:30')
# t0 = pd.Timestamp('2022-09-20 07:30')
fig, ax = plt.subplots(2, 3, sharex=True, sharey=True, figsize=(9, 6))
for i, ax_ in enumerate(ax.flatten()):
    # t0 += pd.Timedelta('5min')
    # t1 = t0 + pd.Timedelta('5min')
    t0 += pd.Timedelta('30min')
    t1 = t0 + pd.Timedelta('5min')
    df_test = df.loc[(df['datetime (utc)'] < t1) & 
        (df['datetime (utc)'] > t0)]
    df_test = df_test.set_index('datetime (utc)').mean(axis=0)
    ax_.plot(cda_midbin, df_test[[x for x in df_test.index if '_mcda (dN/dlogDp)' in x]].T, '.', label='mCDA')
    ax_.plot(pops_midbin, df_test[[x for x in df_test.index if '_pops (dN/dlogDp)' in x]].T, '.', label='POPS')
    ax_.set_xscale('log')
    ax_.set_yscale('log')
    ax_.grid()
    ax_.set_ylim(1e-3, 1e3)
    ax_.legend()
    ax_.set_title(f'{t0.strftime("%H:%M")} - {t1.strftime("%H:%M")}')
    ax_.text(
        -0.0,
        1.05,
        "(" + string.ascii_lowercase[i] + ")",
        transform=ax_.transAxes,
        size=12,
    )
ax[0, 0].set_ylabel(r'dN/dlogDp (cm$^{-3}$)')
ax[1, 0].set_ylabel(r'dN/dlogDp (cm$^{-3}$)')
ax[1, 0].set_xlabel('Size (µm)')
ax[1, 1].set_xlabel('Size (µm)')
ax[1, 2].set_xlabel('Size (µm)')
fig.savefig(fr"C:\Users\le\OneDrive - Ilmatieteen laitos\PaCE_2022\ESSD special issue\Viet_et_al_2025\Ver2\Editor_reply/pops_mcda_{save_date}.png", dpi=300, bbox_inches='tight')
