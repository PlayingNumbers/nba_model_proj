# -*- coding: utf-8 -*-
"""
Created on Sat Dec 21 09:12:36 2019

@author: Ken
"""

import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv('data_final_no_refs.csv')
df_ref = pd.read_csv('data_final_refs.csv')

df.home_team.unique()

city_dict = {'L.A. Lakers': 'L.A.','L.A. Clippers': 'L.A.','Brooklyn':'New York'}

df['Home_City'] = df.home_team.apply(lambda x: city_dict[x] if x in city_dict.keys() else x)

pivoted = pd.pivot_table(df,index = ['date','home_team'], values='away_team',columns='Home_City', aggfunc='count').reset_index().fillna(0)

with_stadiums = pd.merge(df_ref,pivoted, on=['date','home_team'])

with_stadiums.to_csv('data_with_stadiums.csv')