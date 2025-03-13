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
cloud = ~np.isnan(df["LWC_mcda (g/m3)"])
variable = ["N_conc_cpc (cm-3)", "N_conc_pops (cm-3)", 'Nd_mcda (cm-3)']

for var in variable:
    print(f"{var}: {df.loc[~cloud, var].mean():.5f} +- {df.loc[~cloud, var].std():.5f}")
    
for var in variable:
    print(f"{var}: {df.loc[cloud, var].mean():.5f} +- {df.loc[cloud, var].std():.5f}")

# %%
variable = ['LWC_mcda (g/m3)', 'MVD_mcda (um)', 'ED_mcda (um)']

for var in variable:
    print(f"{var}: {df[var].median():.5f}")
# %%
cloud = ~np.isnan(df["LWC_mcda (g/m3)"])
variable = ["N_conc_cpc (cm-3)", "N_conc_pops (cm-3)", 'Nd_mcda (cm-3)']

for var in variable:
    print(f"{var}: {df.loc[~cloud, var].median():.5f}")
    
for var in variable:
    print(f"{var}: {df.loc[cloud, var].median():.5f}")

