#!/usr/bin/python3
import sys
import pickle
from collections import namedtuple

def mapper():
    for line in sys.stdin:
        row=Line._make(line)
        if row.STN=='STN':
            continue # Continue to next row if current row is a file heaader
        try:
            country, hemisphere = station_dict[f'{row.STN}-{row.WBAN}'].split(', ')
        except KeyError:
            continue # Continue to next row if current station didn't have geo-spatial info

        # For temperatures I'm mostly interested in the winter/summer changes,
        # since autumn, spring should fall inbetween by default. I'll also
        # consider the equinox months to mark the start of the season. Therefore:
        # if the station is in the northern hemisphere, then I'll consider the
        # months 6,7,8 to be summer and 1,2,12 to be winter. This is reversed
        # in the southern hemisphere. For changes in precipitation I'm interested
        # in year round changes. Finally, I anticipate using the built-in aggregation
        # functions provided by the hadoop streaming API, but will need to preserve
        # some data count information, so that averages can be calculated afterwards

        #Let's start with precipitation:
        print(f'DoubleValueSum:{country}.{row.YEAR}.{row.MONTH}.PRCP\t{row.PRCP}')
        print(f'DoubleValueSum:{country}.{row.YEAR}.{row.MONTH}.PRCP_C\t1')

        #Let's move on to temperatures:
        if int(row.MONTH) in [1,2,6,7,8,12]:
            season=season_dict[f'{hemisphere}-{row.MONTH}']
            print(f'DoubleValueSum:{country}.{row.YEAR}.{season}.MAX_T\t{row.MAX_TEMP}')
            print(f'DoubleValueSum:{country}.{row.YEAR}.{season}.MAX_T_C_C\t1')
            print(f'DoubleValueSum:{country}.{row.YEAR}.{season}.MEAN_T\t{row.MEAN_TEMP}')
            print(f'DoubleValueSum:{country}.{row.YEAR}.{season}.MEAN_T_C_C\t1')
            print(f'DoubleValueSum:{country}.{row.YEAR}.{season}.MIN_T\t{row.MIN_TEMP}')
            print(f'DoubleValueSum:{country}.{row.YEAR}.{season}.MIN_T_C_C\t1')

if __name__== "__main__":
    with open('station_dict.pickle','rb') as f:
        station_dict=pickle.load(f)
    Line = namedtuple('Line','STN, WBAN, YEAR, MONTH, DAY, MEAN_TEMP, MAX_TEMP, MIN_TEMP, PRCP')
    mapper()
    season_dict={}
    for hemisphere in ['N','S']:
        for month in [1,2,6,7,8,12]:
            if hemisphere='N':
                if month in [6,7,8]:
                    season_dict[f'{hemisphere}-{month}']='SUMMER'
                else:
                    season_dict[f'{hemisphere}-{month}']='WINTER'
            else:
                if month in [6,7,8]:
                    season_dict[f'{hemisphere}-{month}']='WINTER'
                else:
                    season_dict[f'{hemisphere}-{month}']='SUMMER'
