# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 20:23:05 2019

@author: Ken
"""

import pandas as pd 
import numpy as np
df = pd.read_csv('data_distance_timezone.csv').fillna(0)

xls = pd.ExcelFile('nba odds 2015-16.xlsx')
df_1516 = pd.read_excel(xls, 'Sheet1')

xls = pd.ExcelFile('nba odds 2016-17.xlsx')
df_1617 = pd.read_excel(xls, 'Sheet1')

xls = pd.ExcelFile('nba odds 2017-18.xlsx')
df_1718 = pd.read_excel(xls, 'Sheet1')

xls = pd.ExcelFile('nba odds 2018-19.xlsx')
df_1819 = pd.read_excel(xls, 'Sheet1')

xls = pd.ExcelFile('nba odds 2019-20 (1).xlsx')
df_1920 = pd.read_excel(xls, 'Sheet1')

################################################################################
#function 
################################################################################

def format_data(dataframe,year):
    df = dataframe.copy()
    df['Date'] = df.Date.apply(lambda x: str(x)+year if len(str(x)) >= 4 else str(x)+str(int(year)+1))
    df['Date'] = df.Date.apply(lambda x: '0'+str(x) if len(str(x))<=7 else str(x))
    df['Date_str'] = df.Date.apply(lambda x: str(x)[-4:]+'-'+str(x)[:2]+'-'+str(x)[2:4])
    
    df['Open'] = df.apply(lambda x: 0 if str(x.Open).lower() == 'pk' else x.Open, axis =1)
    df['Close'] = df.apply(lambda x: 0 if str(x.Close).lower() == 'pk' else x.Close, axis =1)
    df[df.Open == 'pk']
    df['2H'] = df['2H'].apply(lambda x: 0 if x == 'pk' else x)
    
    dict_teams = {'GoldenState':'Golden State',
                  'LAClippers':'L.A. Clippers',
                  'LA Clippers':'L.A. Clippers',
                  'LALakers':'L.A. Lakers',
                  'NewOrleans':'New Orleans',
                  'NewYork':'New York',
                  'OklahomaCity':'Oklahoma City',
                  'SanAntonio':'San Antonio'}
    df.Team = df.Team.apply(lambda x: dict_teams[x] if x in dict_teams.keys() else x)
    
    
    home = df[df.VH == 'H']
    away = df[df.VH == 'V']
    
    hcols = ['Date','Rot','VH']
    for i in home.columns[3:]:
        hcols.append('home_'+i)
        
    home.columns = hcols
    
    acols = ['Date','Rot','VH']
    for i in away.columns[3:]:
        acols.append('away_'+i)
        
    away.columns = acols
    return home,away

################################################################################
#
################################################################################
h1516,away1516 = format_data(df_1516,'2015')
h1617,away1617 = format_data(df_1617,'2016')
h1718,away1718 = format_data(df_1718,'2017')
h1819,away1819 = format_data(df_1819,'2018')
h1920,away1920 = format_data(df_1920,'2019')

df_homes = pd.concat([h1516,h1617,h1718,h1819,h1920])
df_aways = pd.concat([away1516,away1617,away1718,away1819,away1920])
df_homes.Rot = df_homes.Rot-1
#df_test = df[['date','away_team','home_team']]
sample_merge_h = pd.merge(df,df_homes, left_on =['date','home_team'], right_on = ['home_Date_str','home_Team'])
sample_merge_a = pd.merge(sample_merge_h,df_aways, left_on =['date','away_team'], right_on = ['away_Date_str','away_Team'])

df_manip = sample_merge_a.drop(['Date_x','VH_x','Date_y','VH_y'], axis =1)
df_manip.home_Open = df_manip.apply(lambda x: x.home_Close if '-' in str(x.home_Open) else x.home_Open, axis =1)
df_manip.home_Close =df_manip.home_Close.astype(float)
df_manip.away_Open =df_manip.away_Open.astype(float)
df_manip.away_Close =df_manip.away_Close.astype(float)
df_manip.away_Open = df_manip.away_Open.apply(lambda x: 195.5 if x >1000 else x)

df_manip['OU_open'] = df_manip.apply(lambda x: max(x.home_Open,x.away_Open),axis =1)
df_manip['OU_close'] = df_manip.apply(lambda x: max(x.home_Close,x.away_Close),axis =1)
df_manip['line_open'] = df_manip.apply(lambda x: min(x.home_Open,x.away_Open) if min(x.home_Open,x.away_Open) == x.away_Open else -min(x.home_Open,x.away_Open),axis =1)
df_manip['line_close'] = df_manip.apply(lambda x: min(x.home_Close,x.away_Close) if min(x.home_Close,x.away_Close) == x.away_Close else -min(x.home_Close,x.away_Close),axis =1)
df_manip['OU_2H'] = df_manip.apply(lambda x: max(x.home_2H,x.away_2H),axis =1)
df_manip['line_2H'] = df_manip.apply(lambda x: min(x.home_2H,x.away_2H) if min(x.home_2H,x.away_2H) == x.away_2H else -min(x.home_2H,x.away_2H),axis =1)
df_manip['actual_score'] = df_manip.home_Final + df_manip.away_Final

df_final = df_manip.drop(['Unnamed: 0','Rot_x','Rot_y','home_1st','home_2nd','home_3rd','home_4th',
                          'away_1st','away_2nd','away_3rd','away_4th','home_Date_str','away_Date_str',
                          'home_Team','away_Team','home_Open','home_Close','away_Open','away_Close'], axis =1)

df_final.to_csv('data_final_refs.csv')


# no refs 
df_homes = pd.concat([h1516,h1617,h1718,h1819,h1920])
df_aways = pd.concat([away1516,away1617,away1718,away1819,away1920])
df_homes.Rot = df_homes.Rot-1
df_test = df[['date','away_team','home_team']]
sample_merge_h = pd.merge(df_test,df_homes, left_on =['date','home_team'], right_on = ['home_Date_str','home_Team'])
sample_merge_a = pd.merge(sample_merge_h,df_aways, left_on =['date','away_team'], right_on = ['away_Date_str','away_Team'])

df_manip = sample_merge_a.drop(['Date_x','VH_x','Date_y','VH_y'], axis =1)
df_manip.home_Open = df_manip.apply(lambda x: x.home_Close if '-' in str(x.home_Open) else x.home_Open, axis =1)
df_manip.home_Close =df_manip.home_Close.astype(float)
df_manip.away_Open =df_manip.away_Open.astype(float)
df_manip.away_Close =df_manip.away_Close.astype(float)
df_manip.away_Open = df_manip.away_Open.apply(lambda x: 195.5 if x >1000 else x)

df_manip['OU_open'] = df_manip.apply(lambda x: max(x.home_Open,x.away_Open),axis =1)
df_manip['OU_close'] = df_manip.apply(lambda x: max(x.home_Close,x.away_Close),axis =1)
df_manip['line_open'] = df_manip.apply(lambda x: min(x.home_Open,x.away_Open) if min(x.home_Open,x.away_Open) == x.away_Open else -min(x.home_Open,x.away_Open),axis =1)
df_manip['line_close'] = df_manip.apply(lambda x: min(x.home_Close,x.away_Close) if min(x.home_Close,x.away_Close) == x.away_Close else -min(x.home_Close,x.away_Close),axis =1)
df_manip['OU_2H'] = df_manip.apply(lambda x: max(x.home_2H,x.away_2H),axis =1)
df_manip['line_2H'] = df_manip.apply(lambda x: min(x.home_2H,x.away_2H) if min(x.home_2H,x.away_2H) == x.away_2H else -min(x.home_2H,x.away_2H),axis =1)
df_manip['actual_score'] = df_manip.home_Final + df_manip.away_Final

df_final = df_manip.drop(['Rot_x','Rot_y','home_1st','home_2nd','home_3rd','home_4th',
                          'away_1st','away_2nd','away_3rd','away_4th','home_Date_str','away_Date_str',
                          'home_Team','away_Team','home_Open','home_Close','away_Open','away_Close'], axis =1)


df_final.to_csv('data_final_no_refs.csv')









################################################################################
#
################################################################################
df_1516 = df_1516[(df_1516.Open != 'pk') | (df_1516.Close != 'pk')]
df_1516['Date'] = df_1516.Date.apply(lambda x: str(x)+'2015')
df_1516['Date'] = df_1516.Date.apply(lambda x: '0'+str(x) if len(str(x))<=7 else str(x))
df_1516['Date_str'] = df_1516.Date.apply(lambda x: str(x)[-4:]+'-'+str(x)[:2]+'-'+str(x)[2:4])

df_1516['Open'] = df_1516.apply(lambda x: x.Close if x.Open == 'pk' else x.Open, axis =1)
df_1516['Close'] = df_1516.apply(lambda x: x.Open if x.Close == 'pk' else x.Close, axis =1)
df_1516[df_1516.Open == 'pk']
df_1516['2H'] = df_1516['2H'].apply(lambda x: 0 if x == 'pk' else x)

team_names1 = list(df.away_team.unique())
team_names2 = list(df_1516.Team.unique())

set(team_names1)-set(team_names2)
set(team_names2)-set(team_names1)

dict_teams = {'GoldenState':'Golden State',
              'LAClippers':'L.A. Clippers',
              'LA Clippers':'L.A. Clippers',
              'LALakers':'L.A. Lakers',
              'NewOrleans':'New Orleans',
              'NewYork':'New York',
              'OklahomaCity':'Oklahoma City',
              'SanAntonio':'San Antonio'}
dict_teams['GoldenState']
df_1516.Team = df_1516.Team.apply(lambda x: dict_teams[x] if x in dict_teams.keys() else x)


home_1516 = df_1516[df_1516.VH == 'H']
away_1516 = df_1516[df_1516.VH == 'V']

hcols = ['Date','Rot','VH']
for i in home_1516.columns[3:]:
    hcols.append('home_'+i)
    
home_1516.columns = hcols

acols = ['Date','Rot','VH']
for i in away_1516.columns[3:]:
    acols.append('away_'+i)
    
away_1516.columns = acols

df_test = df[['date','away_team','home_team']]

sample_merge_h = pd.merge(df_test,home_1516, left_on =['date','home_team'], right_on = ['home_Date_str','home_Team'])
sample_merge_a = pd.merge(sample_merge_h,away_1516, left_on =['date','away_team'], right_on = ['away_Date_str','away_Team'])