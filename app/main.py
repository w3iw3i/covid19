# Import libraries
# ================

# for date and time opeations
from datetime import datetime, timedelta
# for file and folder operations
import os
import sys
from pathlib import Path
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



# Read in dataset
# ======

path = Path(__file__).parent
confirmed = pd.read_csv((path / './data/time_series_covid19_confirmed_global.csv').resolve())
deaths = pd.read_csv((path / './data/time_series_covid19_deaths_global.csv').resolve())
recovered = pd.read_csv((path / './data/time_series_covid19_recovered_global.csv').resolve())
# confirmed_us = pd.read_csv('../data/time_series_covid19_confirmed_us.csv')
# deaths_us = pd.read_csv('../data/time_series_covid19_deaths_us.csv')

# extract date columns
dates = confirmed.columns[4:]

# melt dataframes into longer format
# ==================================
confirmed_long = confirmed.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], 
                            value_vars=dates, var_name='Date', value_name='Confirmed')

deaths_long = deaths.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], 
                            value_vars=dates, var_name='Date', value_name='Deaths')                         

recovered_long = recovered.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], 
                            value_vars=dates, var_name='Date', value_name='Recovered')
# recovered_long = recovered_long[recovered_long['Country_Region']!='Canada']

# confirmed_us_long = confirmed_us.melt(id_vars=['Province_State', 'Country_Region', 'Lat', 'Long_'], 
#                             value_vars=dates, var_name='Date', value_name='Confirmed')
# confirmed_us_long.rename(columns={'Long_' : 'Long'}, inplace=True)

# deaths_us_long = deaths_us.melt(id_vars=['Province_State', 'Country_Region', 'Lat', 'Long_'], 
#                             value_vars=dates, var_name='Date', value_name='Deaths')  
# deaths_us_long.rename(columns={'Long_' : 'Long'}, inplace=True)                                                                                   


# merge dataframes
# ================

master_table = pd.merge(left=confirmed_long, right=deaths_long, how='left',
                      on=['Province/State', 'Country/Region', 'Date', 'Lat', 'Long'])
master_table = pd.merge(left=master_table, right=recovered_long, how='left',
                      on=['Province/State', 'Country/Region', 'Date', 'Lat', 'Long'])
master_table.rename(columns={'Province/State' : 'State', 'Country/Region' : 'Country'}, inplace=True)


# Convert to proper date format
master_table['Date'] = pd.to_datetime(master_table['Date'])

# fill na with 0
master_table['Recovered'] = master_table['Recovered'].fillna(0)

# convert to int datatype
master_table['Recovered'] = master_table['Recovered'].astype('int')

# Active Case = confirmed - deaths - recovered
master_table['Active'] = master_table['Confirmed'] - master_table['Deaths'] - master_table['Recovered']

# print(master_table.head())
# print(master_table.tail(10))


# print(master_table.groupby('Date')['Confirmed'].sum())
# print(master_table.groupby('Date')['Deaths'].sum())
# # print(master_table['Deaths'].sum())
# # print(master_table['Recovered'].sum())


# # fixing Country names
# # ====================

# renaming countries, regions, provinces
master_table['Country'] = master_table['Country'].replace('Korea, South', 'South Korea')

# Greenland
master_table.loc[master_table['State'] =='Greenland', 'Country'] = 'Greenland'

# Mainland china to China
master_table['Country'] = master_table['Country'].replace('Mainland China', 'China')


# filling missing values 
# ======================
# fill missing province/state value with ''
master_table[['State']] = master_table[['State']].fillna('')

# fill missing numerical values with 0
cols = ['Confirmed', 'Deaths', 'Recovered', 'Active']
master_table[cols] = master_table[cols].fillna(0)


print(master_table.info())
print(master_table)


master_latest = master_table.loc[master_table['Date'] == '2021-07-06']

master_latest.to_csv('master_latest.csv')