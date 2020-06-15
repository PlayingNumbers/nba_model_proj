# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 20:07:30 2019

@author: Ken
"""
import pandas as pd 
import matplotlib.pyplot as plt 
import geopandas as gpd 
from geopy.distance import distance


dist_times = pd.read_csv('distance_and_time.csv')
dist_times_home = dist_times.copy()
dist_times_home.columns = ['City','Home_Lat_Long','Home_Time_Zone']

dist_times_away = dist_times.copy()
dist_times_away.columns = ['City','Away_Lat_Long','Away_Time_Zone']

df = pd.read_csv('refs_and_rest.csv')

data_home = pd.merge(df,dist_times_home, left_on = 'home_team', right_on='City')
data_home_away = pd.merge(data_home,dist_times_away, left_on = 'away_team',right_on = 'City')


def distance_miles(dist1,dist2):
    try: return distance(dist1,dist2).miles
    except: return -1

data_home_away['away_traveled'] = data_home_away.apply(lambda x: distance_miles(x.Away_Lat_Long,x.Home_Lat_Long), axis=1)
data_home_away['time_diff'] = data_home_away.Home_Time_Zone - data_home_away.Away_Time_Zone

data_home_away.columns

df_out = data_home_away.drop(['Unnamed: 0', 'Unnamed: 0.1','teams','City_x','City_y','Away_Lat_Long','Home_Lat_Long','Team_x','Team_y','Home_Time_Zone','Away_Time_Zone'], axis =1)

df_out.to_csv('data_distance_timezone.csv')