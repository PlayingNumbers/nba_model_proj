# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 14:06:00 2019

@author: Ken
"""

import pandas as pd
import re

df = pd.read_csv('games_refs_by_date.csv')

df['away_team'] = df.gameAndRefs.apply(lambda x: x.split('@')[0].strip())

unique_teams = list(df['away_team'].unique())
unique_teams.sort()

def home_parser(string,team_list):
    for i in team_list:
        if i in string:
            return i
        
def home_parser2(string,team_list):
    for i in team_list:
        if string.find(i) >= 0:
            return i
        
def remove_char(char,list_in):
    lst = list_in
    lst.remove(char)
    return lst

df['home_team'] = df.gameAndRefs.apply(lambda x: home_parser2(x.split('@')[1],unique_teams).strip())

df['teams'] = df.away_team + ' @ ' + df.home_team

df['correct_teams'] = df.apply(lambda x: 1 if x.gameAndRefs.startswith(x.teams) else 0, axis =1)

df['refs'] = df.apply(lambda x: x.gameAndRefs.replace(str(x.teams),"").strip(), axis =1)

df['refs_individual'] = df.refs.apply(lambda x: re.sub("[\(\[].*?[\)\]]", ",", x))
df['refs_list'] = df.refs_individual.apply(lambda x: remove_char('',[i.strip() for i in x.split(',')]))

df_exploded = df.explode('refs_list')

df_penultimate = df_exploded[['date','away_team','home_team','teams','refs_list','correct_teams']]
df_final = pd.pivot_table(df_penultimate, index = ['date','away_team','home_team','teams'], columns = 'refs_list',values = 'correct_teams', aggfunc = 'count').reset_index()

df_final.to_csv('refs_by_game.csv')
"""
list(df['refs_list'])

refs = []
for i in list(df['refs_list']):
    for j in i:
        refs.append(j)
refs.remove('')

refs_dedup = list(set(refs))
refs_dedup.remove('')
"""

#fix miami and washington 