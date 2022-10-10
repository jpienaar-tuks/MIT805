#!/usr/bin/python3

import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from os import path

df = pd.read_csv(path.join('..','isd-history.csv'))
df['bogus']=((df['LAT']!=0)|(df['LON']!=0))
df2=df.loc[df['bogus'],:]
ax = plt.axes(projection=ccrs.PlateCarree())
ax.stock_img()
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS)

plt.scatter(df2['LON'],df2['LAT'], s=0.1, color='red', transform=ccrs.PlateCarree())
plt.show()

import os, re
import numpy as np

files = os.listdir(path.join('..','gsod_all_years'))
stn_str = re.compile(r'([A0-9]+)-(\d+)-(\d+).op.gz')
stns = []
for f in files:
    stns.append(stn_str.match(f).groups())

df = pd.DataFrame(stns, columns=['WMO','WBAN','year'])
counts = df.groupby('year').count()['WMO']
counts.index = pd.to_numeric(counts.index)

plt.plot(counts)
plt.title('Station count by year')
plt.xticks(ticks=np.arange(1910, 2030, 10))
plt.show()


