#!/usr/bin/python3

import pandas as pd
import pickle, os

# When we run the mapper process we want a dictionary to be able to
# look up the station's country code as well as whether it's in the
# northern or southern hemisphere (since the seasons are reversed)
# I'll also be filtering out stations that doesn't have geo-spatial
# information

df = pd.read_csv(os.path.join('..','isd-history.csv'))
station_dict={}
for i, row in df.iterrows():
    if row['LAT']==0 and row['LON']==0:
        continue
    if row['LAT']==None or row['LON']==None:
        continue
    station_id = '{USAF}-{WBAN}'.format(**row)
    hemisphere = 'N' if row['LAT']>=0 else 'S'
    station_dict[station_id] = '{}, {}'.format(row['CTRY'], hemisphere)
with open('station-dict.pickle','wb') as f:
    pickle.dump(station_dict, f, -1)
