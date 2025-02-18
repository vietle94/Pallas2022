import pandas as pd
import numpy as np
import glob

files_path = r'C:\Users\le\OneDrive - Ilmatieteen laitos\Campaigns\Pace2022\FMI balloon payload\Processed_data/'
files = glob.glob(files_path + '*.csv')
df = pd.concat([pd.read_csv(file) for file in files], ignore_index=True)

df.replace(-9999.9, np.nan, inplace=True)

# %%
variable = ['LWC_mcda (g/m3)', 'MVD_mcda (um)', 'ED_mcda (um)']

for var in variable:
    print(f"{var}: {df[var].mean():.5f} +- {df[var].std():.5f}")

# %%
variable = ["N_conc_cpc(1/ccm)", "N_conc_pops (1/ccm)", 'Nd_mcda (1/ccm)']

for var in variable:
    print(f"{var}: {df[var].mean():.5f} +- {df[var].std():.5f}")
