import pandas as pd
import numpy as np
import glob
import matplotlib.pyplot as plt
from UAVision.mcda.preprocess import mcda_midbin_all
from UAVision.pops.preprocess import pops_binedges
from UAVision.utils import calculate_midbin
import json
import matplotlib.dates as mdates
import string

# %%
cda = pd.read_csv(r"C:\Users\le\Desktop\Pallas2022\FMI.CDA.b1.20221001.csv", encoding='unicode_escape')
cda['datetime'] = pd.to_datetime(cda['year'].astype(str) + cda['month'].astype(str).str.zfill(2) + cda['day'].astype(str).str.zfill(2) +
                             cda['hour'].astype(str).str.zfill(2) + cda['min'].astype(str).str.zfill(2), format="%Y%m%d%H%M")
cda.replace(-9999.9, np.nan, inplace=True)

# %%
balloon = pd.concat([pd.read_csv(file) for file in
                           glob.glob(r"C:\Users\le\OneDrive - Ilmatieteen laitos\Campaigns\Pace2022\FMI balloon payload\Processed_data\*.csv")],
                           ignore_index=True)
balloon["datetime (utc)"] = pd.to_datetime(balloon["datetime (utc)"])
balloon.rename(columns={"datetime (utc)": "datetime"}, inplace=True)
balloon.replace(-9999.9, np.nan, inplace=True)
balloon = balloon[np.abs(balloon['height_bme (m)']-290) < 50]
balloon = balloon.set_index('datetime').resample('1min').mean()
balloon = balloon.dropna(how='all').reset_index()

# %%
case1 = balloon[(balloon['datetime'] > pd.Timestamp('2022-10-02')) & (balloon['datetime'] < pd.Timestamp('2022-10-03'))]

# %%
df_inter = case1.merge(cda, on='datetime', how='inner')
print(df_inter.shape[0])
# %%
fig, ax = plt.subplots(1, 2, figsize=(9, 4), constrained_layout=True)
ax[0].errorbar(x = df_inter['median volume diameter (µm)'].mean(), y = df_inter['MVD_mcda (um)'].mean(), 
            xerr = df_inter['median volume diameter (µm)'].std(), yerr = df_inter['MVD_mcda (um)'].std(), 
            fmt='.', alpha=0.5)

# Set aspect ratio to 1:1 and add 1:1 reference line
ax[0].set_aspect('equal', 'box')
ax[0].plot([5, 20], [5, 20], '--', color='gray', alpha=0.5, label='1:1 line')
ax[0].set_xlim(5, 20)
ax[0].set_xticks([5, 10, 15, 20])
ax[0].set_ylim(5, 20)
ax[0].set_yticks([5, 10, 15, 20])

ax[0].grid(True, alpha=0.3)
ax[0].legend()
ax[0].set_ylabel('MVD mCDA (um)')
ax[0].set_xlabel('MVD CDA (µm)')

ax[1].errorbar(x = df_inter['effective diameter (µm)'].mean(), y = df_inter['ED_mcda (um)'].mean(), 
            xerr = df_inter['effective diameter (µm)'].std(), yerr = df_inter['ED_mcda (um)'].std(), 
            fmt='.', alpha=0.5)

# Set aspect ratio to 1:1 and add 1:1 reference line
ax[1].set_aspect('equal', 'box')
ax[1].plot([5, 20], [5, 20], '--', color='gray', alpha=0.5, label='1:1 line')
ax[1].set_xlim(5, 20)
ax[1].set_xticks([5, 10, 15, 20])
ax[1].set_ylim(5, 20)
ax[1].set_yticks([5, 10, 15, 20])

ax[1].grid(True, alpha=0.3)
ax[1].legend()
ax[1].set_ylabel('ED mCDA (um)')
ax[1].set_xlabel('ED CDA (µm)')
for n, ax_ in enumerate(ax.flatten()):
    ax_.text(
        -0.0,
        1.05,
        "(" + string.ascii_lowercase[n] + ")",
        transform=ax_.transAxes,
        size=12,
    )
fig.savefig(r"C:\Users\le\OneDrive - Ilmatieteen laitos\PaCE_2022\ESSD special issue\Viet_et_al_2025\Review_answer/CDA_mCDA_intercomp_1002.png",
            dpi=600, bbox_inches='tight')
# %%

case2 = balloon[(balloon['datetime'] > pd.Timestamp('2022-10-04')) & (balloon['datetime'] < pd.Timestamp('2022-10-05'))]

df_inter = case2.merge(cda, on='datetime', how='inner')
print(df_inter.shape[0])

# %%
fig, ax = plt.subplots(1, 2, figsize=(9, 4), constrained_layout=True)
ax[0].errorbar(x = df_inter['median volume diameter (µm)'].mean(), y = df_inter['MVD_mcda (um)'].mean(), 
            xerr = df_inter['median volume diameter (µm)'].std(), yerr = df_inter['MVD_mcda (um)'].std(), 
            fmt='.', alpha=0.5)

# Set aspect ratio to 1:1 and add 1:1 reference line
ax[0].set_aspect('equal', 'box')
ax[0].plot([5, 20], [5, 20], '--', color='gray', alpha=0.5, label='1:1 line')
ax[0].set_xlim(5, 20)
ax[0].set_xticks([5, 10, 15, 20])
ax[0].set_ylim(5, 20)
ax[0].set_yticks([5, 10, 15, 20])

ax[0].grid(True, alpha=0.3)
ax[0].legend()
ax[0].set_ylabel('MVD mCDA (um)')
ax[0].set_xlabel('MVD CDA (µm)')

ax[1].errorbar(x = df_inter['effective diameter (µm)'].mean(), y = df_inter['ED_mcda (um)'].mean(), 
            xerr = df_inter['effective diameter (µm)'].std(), yerr = df_inter['ED_mcda (um)'].std(), 
            fmt='.', alpha=0.5)

# Set aspect ratio to 1:1 and add 1:1 reference line
ax[1].set_aspect('equal', 'box')
ax[1].plot([5, 20], [5, 20], '--', color='gray', alpha=0.5, label='1:1 line')
ax[1].set_xlim(5, 20)
ax[1].set_xticks([5, 10, 15, 20])
ax[1].set_ylim(5, 20)
ax[1].set_yticks([5, 10, 15, 20])

ax[1].grid(True, alpha=0.3)
ax[1].legend()
ax[1].set_ylabel('ED mCDA (um)')
ax[1].set_xlabel('ED CDA (µm)')
for n, ax_ in enumerate(ax.flatten()):
    ax_.text(
        -0.0,
        1.05,
        "(" + string.ascii_lowercase[n] + ")",
        transform=ax_.transAxes,
        size=12,
    )
fig.savefig(r"C:\Users\le\OneDrive - Ilmatieteen laitos\PaCE_2022\ESSD special issue\Viet_et_al_2025\Review_answer/CDA_mCDA_intercomp_1004.png",
        dpi=600, bbox_inches='tight')
# %%
case3 = balloon[(balloon['datetime'] > pd.Timestamp('2022-09-28')) & (balloon['datetime'] < pd.Timestamp('2022-09-29'))]

# %%
cda = pd.read_csv(r"C:\Users\le\Desktop\Pallas2022\FMI.CDA.b1.20220914.csv", encoding='unicode_escape')
cda['datetime'] = pd.to_datetime(cda['year'].astype(str) + cda['month'].astype(str).str.zfill(2) + cda['day'].astype(str).str.zfill(2) +
                             cda['hour'].astype(str).str.zfill(2) + cda['min'].astype(str).str.zfill(2), format="%Y%m%d%H%M")
cda.replace(-999.9, np.nan, inplace=True)
df_inter = case3.merge(cda, on='datetime', how='inner')
print(df_inter.shape[0])
# %%
fig, ax = plt.subplots(1, 2, figsize=(9, 4), constrained_layout=True)
ax[0].errorbar(x = df_inter['median volume diameter (µm)'].mean(), y = df_inter['MVD_mcda (um)'].mean(), 
            xerr = df_inter['median volume diameter (µm)'].std(), yerr = df_inter['MVD_mcda (um)'].std(), 
            fmt='.', alpha=0.5)

# Set aspect ratio to 1:1 and add 1:1 reference line
ax[0].set_aspect('equal', 'box')
ax[0].plot([5, 20], [5, 20], '--', color='gray', alpha=0.5, label='1:1 line')
ax[0].set_xlim(5, 20)
ax[0].set_xticks([5, 10, 15, 20])
ax[0].set_ylim(5, 20)
ax[0].set_yticks([5, 10, 15, 20])

ax[0].grid(True, alpha=0.3)
ax[0].legend()
ax[0].set_ylabel('MVD mCDA (um)')
ax[0].set_xlabel('MVD CDA (µm)')

ax[1].errorbar(x = df_inter['effective diameter (µm)'].mean(), y = df_inter['ED_mcda (um)'].mean(), 
            xerr = df_inter['effective diameter (µm)'].std(), yerr = df_inter['ED_mcda (um)'].std(), 
            fmt='.', alpha=0.5)

# Set aspect ratio to 1:1 and add 1:1 reference line
ax[1].set_aspect('equal', 'box')
ax[1].plot([5, 20], [5, 20], '--', color='gray', alpha=0.5, label='1:1 line')
ax[1].set_xlim(5, 20)
ax[1].set_xticks([5, 10, 15, 20])
ax[1].set_ylim(5, 20)
ax[1].set_yticks([5, 10, 15, 20])

ax[1].grid(True, alpha=0.3)
ax[1].legend()
ax[1].set_ylabel('ED_mcda (um)')
ax[1].set_xlabel('effective diameter (µm)')
for n, ax_ in enumerate(ax.flatten()):
    ax_.text(
        -0.0,
        1.05,
        "(" + string.ascii_lowercase[n] + ")",
        transform=ax_.transAxes,
        size=12,
    )
fig.savefig(r"C:\Users\le\OneDrive - Ilmatieteen laitos\PaCE_2022\ESSD special issue\Viet_et_al_2025\Review_answer/CDA_mCDA_intercomp_0928.png",
            dpi=600, bbox_inches='tight')
# %%
