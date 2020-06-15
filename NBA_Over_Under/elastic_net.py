# -*- coding: utf-8 -*-
"""
Created on Sat Feb 15 09:47:51 2020

@author: Ken
"""

import pandas as pd 

df_ref = pd.read_csv('final_data_scores.csv')


df_ref['constant'] =1

df_ref['line_movement'] = df_ref.line_close - df_ref.line_open
df_ref['OU_movement'] = df_ref.OU_close - df_ref.OU_open
df_ref.dropna(inplace=True)
for i in df_ref.columns:
    print("'"+i+"'"+',')


from sklearn.model_selection import train_test_split,GridSearchCV
from sklearn.linear_model import LinearRegression, Lasso
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.linear_model import ElasticNet
import math

#multiple linear regression 

# Home model 
from statsmodels.stats.outliers_influence import variance_inflation_factor
import statsmodels.api as sm


X = df_ref.drop(['Unnamed: 0','date','away_team','home_team','actual_score','line_2H',
                'OU_2H','line_close','OU_close','away_ML','away_2H','home_2H','home_ML','away_Final','home_Final'], axis=1)

Y = df_ref.home_Final.values

e_net = ElasticNet(random_state = 0, l1_ratio=0)
e_net.fit(X,Y)
e_net.score(X,Y)

