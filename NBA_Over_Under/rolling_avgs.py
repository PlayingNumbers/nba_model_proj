# -*- coding: utf-8 -*-
"""
Created on Sat Dec 21 09:26:57 2019

@author: Ken
"""

import pandas as pd

df =pd.read_csv('data_with_stadiums.csv')
df.date = pd.to_datetime(df.date,errors ='coerce')   
df_trimmed = df[['date','away_team','home_team','away_Final','home_Final','OU_close']]

# do calculations here then split to home and away 
home_teams = {}
away_teams = {}

def rolling_avgs(data,team):
    df_chi = data.copy() 
    df_chi = df_chi[(df_chi.home_team == team) | (df_chi.away_team == team)]
    df_chi.date = pd.to_datetime(df_chi.date,errors ='coerce')    
    df_chi.sort_values('date', inplace=True)
    
    df_chi['teamscore'] = df_chi.apply(lambda x: x.away_Final if x.away_team == team else x.home_Final, axis =1)
    df_chi['prev_OU'] = df_chi.OU_close.shift(1)
    df_chi['teamscore_prev'] = df_chi.teamscore.shift(1)
    df_chi['score_r3'] = df_chi.teamscore_prev.rolling(3).mean()
    df_chi['score_r5'] = df_chi.teamscore_prev.rolling(5).mean()
    df_chi['score_r10'] = df_chi.teamscore_prev.rolling(10).mean()
    df_chi['OU_r3'] = df_chi.prev_OU.rolling(3).mean()
    df_chi['OU_r5'] = df_chi.prev_OU.rolling(5).mean()
    
    df_chi_home = df_chi[df_chi.home_team == team][['date','home_team','prev_OU','teamscore_prev','score_r3','score_r5','score_r10','OU_r3','OU_r5']]
    df_chi_away = df_chi[df_chi.away_team == team][['date','away_team','prev_OU','teamscore_prev','score_r3','score_r5','score_r10','OU_r3','OU_r5']]
    df_chi_home.columns = ['date','home_team','prev_OU_home','teamscore_prev_home','score_r3_home','score_r5_home','score_r10_home','OU_r3_home','OU_r5_home']
    df_chi_away.columns = ['date','away_team','prev_OU_away','teamscore_prev_away','score_r3_away','score_r5_away','score_r10_away','OU_r3_away','OU_r5_away']

    return df_chi_home, df_chi_away


for i in df.away_team.unique():
    home_teams[i] = rolling_avgs(df_trimmed,i)[0]
    away_teams[i] = rolling_avgs(df_trimmed,i)[1]


df_list_home = [ v for k,v in home_teams.items()] 
df_new_home = pd.concat(df_list_home ,axis=0)

df_list_away = [ v for k,v in away_teams.items()] 
df_new_away = pd.concat(df_list_away,axis=0)

merged_home = pd.merge(df,df_new_home, on = ['date','home_team'])
merged_away = pd.merge(merged_home,df_new_away, on = ['date','away_team'])

df_final = merged_away.drop(['Unnamed: 0','Unnamed: 0.1'], axis =1)


df_final.to_csv('final_data_scores.csv')











