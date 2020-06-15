# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 10:17:22 2019

@author: Ken
"""

import pandas as pd 
import datetime as dt

df = pd.read_csv('refs_by_game.csv')
df.date = pd.to_datetime(df.date, errors = 'coerce' )
teams = {}

#map to home and away team 

for i in df.away_team.unique():
    teams[i] = df[(df.away_team == i) | (df.home_team == i)]
    

def add_rest(data):    
    data['last_gm'] = data.date.shift(1)
    data['last2_gm'] = data.date.shift(2)
    data['last3_gm'] = data.date.shift(3)
    
    data['since_last'] = (data.date - data.last_gm).dt.days
    data['since2'] = (data.date - data.last2_gm).dt.days
    data['since3'] = (data.date - data.last3_gm).dt.days
    
    data['b2b'] = data.since_last.apply(lambda x: 1 if x ==1 else 0)
    data['threein4'] = data.since2.apply(lambda x: 1 if x ==3 else 0)
    data['fourin5'] = data.since3.apply(lambda x: 1 if x ==5 else 0)
    data['rest2'] = data.since_last.apply(lambda x: 1 if x ==3 else 0)
    data['rest3_plus'] = data.since_last.apply(lambda x: 1 if x >3 else 0)    
    return data.drop(['last_gm','last2_gm','last3_gm','since_last','since2','since3'], axis =1)

for i in teams.keys():
    teams[i] = add_rest(teams[i])
    teams[i]['Team']=i

df_list = [ v for k,v in teams.items()] 
df_new = pd.concat(df_list ,axis=0)

df_to_join_home = df_new[['date','Team','b2b','threein4','fourin5','rest2','rest3_plus']]
df_to_join_home.columns = ['date','Team','b2b_home','threein4_home','fourin5_home','rest2_home','rest3_plus_home']

df_to_join_away = df_new[['date','Team','b2b','threein4','fourin5','rest2','rest3_plus']]
df_to_join_away.columns = ['date','Team','b2b_away','threein4_away','fourin5_away','rest2_away','rest3_plus_away']

df_w_home = pd.merge(df,df_to_join_home, left_on = ['date','home_team'], right_on = ['date','Team'])
df_final = pd.merge(df_w_home, df_to_join_away, left_on =['date','away_team'], right_on =['date','Team'])
df_final['home_team'] = df_final.home_team.apply(lambda x: 'L.A. Clippers' if x == 'LA Clippers' else x)
df_final['away_team'] = df_final.away_team.apply(lambda x: 'L.A. Clippers' if x == 'LA Clippers' else x)


df_final.to_csv('refs_and_rest.csv')