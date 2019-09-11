# -*- coding: utf-8 -*-
"""
Reads and stores data from DMI's weather archive:
https://www.dmi.dk/vejrarkiv/

LEGAL DISCLAIMER:

This script is for educational use and the 
original author does not take responsibility 
for any illegal use of this script. You shall 
not use this script for any illegal purposes!

@author: Rasmus Vest Nielsen
"""

import json
import requests
import pandas as pd
import time
import datetime
import locale

# Define date range.
locale.setlocale(locale.LC_ALL, 'dan_DNK') # Months are in danish.
start_dates = pd.date_range(start = '2011-01-01', end  = '2011-03-29', 
                            freq = 'D')
end_dates   = start_dates + datetime.timedelta(days = 1)

locations = ['Thisted', 'Viborg'] #'Aalborg', 

# Define sleep timers to avoid down throttling,
# ip bans, and other nasty stuff.  
sleep_int  = 15 # Number of records in between sleep is activated.
sleep_time = 5  # Time in seconds.

# Define list of data frames to be concatted later on
df_list_windspeed = []
df_list_winddir = []
for location in locations:
    for start, end, i in zip(start_dates, end_dates, 
                             range(0, len(end_dates))):
        # Request url and pass the response into json
        # Original url: 
        # https://www.dmi.dk/dmidk_obsWS/rest/archive/hourly/danmark
        # /wind/Aalborg/2018/Marts/25  // Wind [m/s]
        # https://www.dmi.dk/dmidk_obsWS/rest/archive/hourly
        # /danmark/winddir/Aalborg/2018/Marts/29 // Wind direction [degrees]
        dt = end - start
        
        # Since the timeout for the server is not constant (why not?) 
        # a little fuckery is needed, where the few cases of time outs
        # are catched and corrected.
        try:
            page_windspeed = requests.get('https://www.dmi.dk/dmidk_obsWS/rest/archive/hourly/danmark/wind/{0}/{1}/{2}/{3}'.format(
                location, end.year, end.strftime("%B").capitalize(), end.day))
            
            html_windspeed = page_windspeed.content
            data_windspeed = json.loads(html_windspeed)
            
            # Hourly mean wind intensity
            wind_speed_hourly_mean = pd.DataFrame.from_dict(
                    data_windspeed[0]['dataserie'])
            
            df_list_windspeed.append(wind_speed_hourly_mean)
            
            page_winddir = requests.get('https://www.dmi.dk/dmidk_obsWS/rest/archive/hourly/danmark/winddir/{0}/{1}/{2}/{3}'.format(
                location, end.year, end.strftime("%B").capitalize(), end.day))
            
            html_winddir = page_winddir.content
            data_winddir = json.loads(html_winddir)
            
            # Hourly mean wind intensity
            wind_dir_hourly_mean = pd.DataFrame.from_dict(
                    data_winddir['dataserie'])
            
            df_list_winddir.append(wind_dir_hourly_mean)
        except: # If unregular time out occurs, try again...
            time.sleep(float(sleep_time)) # Time in seconds
            page_windspeed = requests.get('https://www.dmi.dk/dmidk_obsWS/rest/archive/hourly/danmark/wind/{0}/{1}/{2}/{3}'.format(
                location, end.year, end.strftime("%B").capitalize(), end.day))
           
            html_windspeed = page_windspeed.content
            data_windspeed = json.loads(html_windspeed)
            
            # Hourly mean wind intensity
            wind_speed_hourly_mean = pd.DataFrame.from_dict(data_windspeed[0]['dataserie'])
            df_list_windspeed.append(wind_speed_hourly_mean)
            
            page_winddir = requests.get('https://www.dmi.dk/dmidk_obsWS/rest/archive/hourly/danmark/winddir/{0}/{1}/{2}/{3}'.format(
                location, end.year, end.strftime("%B").capitalize(), end.day))
            
            html_winddir = page_winddir.content
            data_winddir = json.loads(html_winddir)
            
            # Hourly mean wind intensity
            wind_dir_hourly_mean = pd.DataFrame.from_dict(
                    data_winddir['dataserie'])
            df_list_winddir.append(wind_dir_hourly_mean)
            
        
        # Print progress on the same line
        print(str(i + 1) + " downloaded out of " + str((len(end_dates))) + 
              " days of data. Sleep for " + str(sleep_time) + " sec every " + 
              str(sleep_int) + " days.         \r",)
    
        # If 'sleep_int' days of records have been downloaded, sleep for 
        # 'sleep_time' sec (trying to prevent DMI's server to block us when 
        # sending too many requests too fast)
        if (i + 1) % int(sleep_int) == 0:
            time.sleep(float(sleep_time)) # Time in seconds
    
            
    # Concatenate list of dataframes        
    df_fin_windspeed = pd.concat(df_list_windspeed)
    df_fin_winddir = pd.concat(df_list_winddir)
    
    # Store time series to disk
    df_fin_windspeed['dateString'] = pd.to_datetime(df_fin_windspeed.dateString)
    
    start_date = '{0}-{1}-{2}'.format(df_fin_windspeed.dateString.iloc[0].year, 
                  df_fin_windspeed.dateString.iloc[0].month,
                  df_fin_windspeed.dateString.iloc[0].day)
    
    end_date   = '{0}-{1}-{2}'.format(df_fin_windspeed.dateString.iloc[-1].year, 
                  df_fin_windspeed.dateString.iloc[-1].month,
                  df_fin_windspeed.dateString.iloc[-1].day)
    
    df_fin_windspeed.to_csv('{0}_wind_speed_{1}_to_{2}.csv'.format(location, 
                            start_date, end_date))
    
    # Concatenate list of dataframes        
    df_fin_windspeed = pd.concat(df_list_windspeed)
    
    # Store time series to disk
    df_fin_winddir['dateString'] = pd.to_datetime(df_fin_winddir.dateString)
    start_date = '{0}-{1}-{2}'.format(df_fin_winddir.dateString.iloc[0].year, 
                  df_fin_winddir.dateString.iloc[0].month,
                  df_fin_winddir.dateString.iloc[0].day)
    
    end_date   = '{0}-{1}-{2}'.format(df_fin_winddir.dateString.iloc[-1].year, 
                  df_fin_winddir.dateString.iloc[-1].month,
                  df_fin_winddir.dateString.iloc[-1].day)
    
    df_fin_winddir.to_csv('{0}_wind_dir_{1}_to_{2}.csv'.format(location, 
                          start_date, end_date))


## Remove extra column and duplicates (I can't remember if this is needed!)
#df_fin = df_fin.drop('delete', axis = 1)
#df_fin = df_fin.drop_duplicates()
