# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 10:14:57 2022

@author: Johann
"""
import pandas as pd
import os
from scipy.stats import linregress

precip_data=[]
temperature_data=[]

with open(os.path.join('..','hadoop output','part-00000'),'rt') as f:
    for line in f.readlines():
        prefix, value = line.split('\t')
        fields = prefix.split('.')
        if 'PRCP' in line:
            precip_data.append(fields+[value])
        else:
            temperature_data.append(fields+[value])
df_temp = pd.DataFrame(temperature_data, columns=['Country','Year','Season','Variable','Value'])
df_temp['Year']=df_temp['Year'].astype('int32')
df_temp['Value']=df_temp['Value'].astype('float')

df_temp_pivot = df_temp.pivot(index=['Country','Year','Season'], columns='Variable',values='Value')
df_temp_pivot['MAX_T_AVG'] = df_temp_pivot['MAX_T']/df_temp_pivot['MAX_T_C']
df_temp_pivot['MEAN_T_AVG'] = df_temp_pivot['MEAN_T']/df_temp_pivot['MEAN_T_C']
df_temp_pivot['MIN_T_AVG'] = df_temp_pivot['MIN_T']/df_temp_pivot['MIN_T_C']
df_temp_pivot = df_temp_pivot.drop(['MAX_T','MAX_T_C','MEAN_T','MEAN_T_C','MIN_T','MIN_T_C'],axis=1).unstack()
df_temp_pivot.stack().to_csv('temp.csv')

df_precip = pd.DataFrame(precip_data, columns=['Country','Year','Month','Variable','Value'])
df_precip['Year']=df_precip['Year'].astype('int32')
df_precip['Month']=df_precip['Month'].astype('int32')
df_precip['Value']=df_precip['Value'].astype('float')

df_precip_pivot = df_precip.pivot(index=['Country','Year','Month'],columns='Variable',values='Value')
df_precip_pivot['PRCP_AVG'] = df_precip_pivot['PRCP']/df_precip_pivot['PRCP_C']
df_precip_pivot = df_precip_pivot.drop(['PRCP','PRCP_C'], axis=1).unstack()
df_precip_pivot.stack().to_csv('precip.csv')

# Precip regressions
precip_regressions=[]
for country in df_precip_pivot.index.levels[0]:
    for month in range(1,13):
        x = df_precip_pivot.loc[country].index.values
        y = df_precip_pivot.loc[country,('PRCP_AVG',month)].values
        m, c, r, p, *rest = linregress(pd.DataFrame(zip(x,y)).dropna())
        precip_regressions.append([country, month, m, r**2, p])
pd.DataFrame(precip_regressions,columns=['Country','Month','Slope','R2','p']).to_csv('Precipitation regressions.csv',index=False)
        
# Temperature regressions
temp_regressions=[]
for country in df_temp_pivot.index.levels[0]:
    for season in ['WINTER','SUMMER']:
        for variable in ['MIN_T_AVG','MEAN_T_AVG','MAX_T_AVG']:
            x = df_temp_pivot.loc[country].index.values
            y = df_temp_pivot.loc[country,(variable,season)].values
            m, c, r, p, *rest = linregress(pd.DataFrame(zip(x,y)).dropna())
            temp_regressions.append([country, season, variable, m, r**2, p])
pd.DataFrame(temp_regressions,columns=['Country','Season','Variable','Slope','R2','p']).to_csv('Temperature regressions.csv',index=False)