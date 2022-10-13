# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 10:44:05 2022

@author: Johann
"""

import json
import pandas as pd
import plotly.express as px
import os

with open('countries.geo.json','rt') as f:
    geojson = json.load(f)
    
df_temp = pd.read_csv('Temperature regressions.csv')
country_code_lookups = pd.read_csv('Countrycodes.csv', usecols=['FIPS_GEC','ISO_3166_3'])
country_code_lookups.columns=['ISO3','FIPS']


for season in ['WINTER','SUMMER']:
    for variable in ['MIN_T_AVG','MEAN_T_AVG','MAX_T_AVG']:
        temp_visual=[]
        for i, row in df_temp.loc[(df_temp.Season==season) & (df_temp.Variable==variable)].iterrows():
            try:
                iso3=country_code_lookups.loc[country_code_lookups.FIPS==row.Country, 'ISO3'].values[0]
            except IndexError:
                continue
            temp_visual.append([iso3, row.Slope*10, row.p])
        df_visual = pd.DataFrame(temp_visual, columns=['ISO3','slope','p'])
        
        fig = px.choropleth_mapbox(df_visual, geojson=geojson, 
                                   locations='ISO3', color='slope',
                                   range_color=[-0,0.7],
                                   mapbox_style="carto-positron",
                                   hover_data={'slope':':.2f',
                                               'p':':.4f'},
                                   labels={'slope': 'Rate of warming per decade',
                                           'p': 'p statistic'},
                                   zoom=2)
        
        with open(os.path.join('..','visuals',f'{season}-{variable}.html'),'wt') as f:
            f.write(fig.to_html(include_plotlyjs='cdn'))
            

df_precip = pd.read_csv('Precipitation regressions.csv')

precip_visual=[]
month_dict={1:'Jan',
            2:'Feb',
            3:'Mar',
            4:'Apr',
            5:'May',
            6:'Jun',
            7:'Jul',
            8:'Aug',
            9:'Sep',
            10:'Oct',
            11:'Nov',
            12:'Dec'}
for i, row in df_precip.iterrows():
    try:
        iso3=country_code_lookups.loc[country_code_lookups.FIPS==row.Country, 'ISO3'].values[0]
    except IndexError:
        continue
    precip_visual.append([iso3, row.Month, row.Slope, row.p])
df_visual = pd.DataFrame(precip_visual, columns=['ISO3', 'month','slope','p'])
df_visual['month_text'] = df_visual.month.map(month_dict)

fig = px.choropleth_mapbox(df_visual, geojson=geojson, 
                           locations='ISO3', color='slope',
                           animation_frame='month',
                           range_color=[-0.05,0.11],
                           mapbox_style="carto-positron",
                           hover_data={'slope':':.3f',
                                       'p':':.4f',
                                       'month_text':True,
                                       'ISO3':True},
                           labels={'slope': 'Change in rainfall (mm/yr)',
                                   'p': 'p statistic',
                                   'month_text':'Month',
                                   'ISO3':'Country'},
                           zoom=2)
fig["layout"].pop("updatemenus")
with open(os.path.join('..','visuals','Precipitation.html'),'wt') as f:
    f.write(fig.to_html(include_plotlyjs='cdn'))
    
    
    
