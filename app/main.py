# import libraries
# ================

# for date and time opeations
from datetime import datetime, timedelta
# for file and folder operations
import os
# for regular expression opeations
import re
# for listing files in a folder
import glob
# for getting web contents
import requests 
# storing and analysing data
import pandas as pd
# numerical analysis
import numpy as np


# dataset
# ======

confirmed = pd.read_csv('../data/time_series_covid19_confirmed_global.csv')
deaths = pd.read_csv('../data/time_series_covid19_deaths_global.csv')
recovered = pd.read_csv('../data/time_series_covid19_recovered_global.csv')
confirmed_us = pd.read_csv('../data/time_series_covid19_confirmed_us.csv')
deaths_us = pd.read_csv('../data/time_series_covid19_deaths_us.csv')


# print(confirmed_df.head())
# print(deaths_df.head())
# print(recovered_df.head())
# print(confirmed_us_df.head())
# print(deaths_us_df.head())


# print(confirmed_df.columns)
# print(deaths_df.columns)
# print(recovered_df.columns)
# print(confirmed_us_df.columns)
# print(deaths_us_df.columns)


# extract date columns
dates = confirmed.columns[4:]

# melt dataframes into longer format
# ==================================
confirmed_long = confirmed.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], 
                            value_vars=dates, var_name='Date', value_name='Confirmed')
confirmed_long.rename(columns={'Province/State' : 'Province_State', 'Country/Region' : 'Country_Region'}, inplace=True)

deaths_long = deaths.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], 
                            value_vars=dates, var_name='Date', value_name='Deaths')
deaths_long.rename(columns={'Province/State' : 'Province_State', 'Country/Region' : 'Country_Region'}, inplace=True)                          

recovered_long = recovered.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], 
                            value_vars=dates, var_name='Date', value_name='Recovered')
recovered_long.rename(columns={'Province/State' : 'Province_State', 'Country/Region' : 'Country_Region'}, inplace=True)
recovered_long = recovered_long[recovered_long['Country_Region']!='Canada']

confirmed_us_long = confirmed_us.melt(id_vars=['Province_State', 'Country_Region', 'Lat', 'Long_'], 
                            value_vars=dates, var_name='Date', value_name='Confirmed')
confirmed_us_long.rename(columns={'Long_' : 'Long'}, inplace=True)

deaths_us_long = deaths_us.melt(id_vars=['Province_State', 'Country_Region', 'Lat', 'Long_'], 
                            value_vars=dates, var_name='Date', value_name='Deaths')  
deaths_us_long.rename(columns={'Long_' : 'Long'}, inplace=True)                                                                                   


confirmed_all = confirmed_long.append(confirmed_us_long)
deaths_all = deaths_long.append(deaths_us_long)


# print(confirmed_all.shape)
# print(deaths_all.shape)
# print(recovered_long.shape)

# print(confirmed.columns)
# print(deaths.columns)
# print(recovered.columns)

# merge dataframes
# ================

master_table = pd.merge(left=confirmed_all, right=deaths_all, how='left',
                      on=['Province_State', 'Country_Region', 'Date', 'Lat', 'Long'])
master_table = pd.merge(left=master_table, right=recovered_long, how='left',
                      on=['Province_State', 'Country_Region', 'Date', 'Lat', 'Long'])


# Convert to proper date format
master_table['Date'] = pd.to_datetime(master_table['Date'])

# fill na with 0
master_table['Recovered'] = master_table['Recovered'].fillna(0)

# convert to int datatype
master_table['Recovered'] = master_table['Recovered'].astype('int')

print(master_table.head())
print(master_table.tail(10))


print(master_table.groupby('Date')['Confirmed'].sum())
print(master_table.groupby('Date')['Deaths'].sum())
# print(master_table['Deaths'].sum())
# print(master_table['Recovered'].sum())