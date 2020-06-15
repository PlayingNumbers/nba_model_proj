# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 19:30:11 2019

@author: Ken
"""

import pandas as pd
import matplotlib.pyplot as plt
df_noref = pd.read_csv('data_final_no_refs.csv')
df_ref = pd.read_csv('data_final_refs.csv')
df_ref['constant'] =1

df_ref['line_movement'] = df_ref.line_close - df_ref.line_open
df_ref['OU_movement'] = df_ref.OU_close - df_ref.OU_open
df_ref.dropna(inplace=True)
for i in df_ref.columns:
    print("'"+i+"'"+',')



#simple linear regression for year
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error
import math

#multiple linear regression 
from statsmodels.stats.outliers_influence import variance_inflation_factor
import statsmodels.api as sm


#actual regression 
X3 = pd.get_dummies(df_ref[['constant',
                                'b2b_home',
                                'threein4_home',
                                'fourin5_home',
                                'rest2_home',
                                'rest3_plus_home',
                                'b2b_away',
                                'threein4_away',
                                'fourin5_away',
                                'rest2_away',
                                'rest3_plus_away',
                                'away_traveled',
                                'time_diff',
                                'home_ML',
                                'home_2H',
                                'away_ML',
                                'away_2H',
                                'OU_open',
                                'OU_close',
                                'line_open',
                                'line_close',
                                'OU_2H',
                                'line_2H',
                                'line_movement',
                                'OU_movement']])




y3 = df_ref.actual_score.values

X_train3, X_test3, y_train3, y_test3 = train_test_split(X3, y3, test_size=0.3, random_state=0)

reg_sm3 = sm.OLS(y_train3, X_train3).fit()
reg_sm3.summary()

y_hat3 = reg_sm3.predict(X_test3)

rmse3 = math.sqrt(mean_squared_error(y_hat3,y_test3))

plt.scatter(y_hat3,y_test3)


from statsmodels.stats.outliers_influence import variance_inflation_factor

# get refs
X3 = df_ref[['constant',
                                'b2b_home',
                                'threein4_home',
                                'fourin5_home',
                                'rest2_home',
                                'rest3_plus_home',
                                'b2b_away',
                                'threein4_away',
                                'fourin5_away',
                                'rest2_away',
                                'rest3_plus_away',
                                'away_traveled',
                                'time_diff',
                                'home_ML',
                                #'home_2H',
                                'away_ML',
                                #'away_2H',
                                'OU_open',
                                #'OU_close',
                                'line_open',
                                #'line_close',
                                'OU_2H',
                                'line_2H',
                                'line_movement',
                                'OU_movement']]




y3 = df_ref.actual_score.values

X_train3, X_test3, y_train3, y_test3 = train_test_split(X3, y3, test_size=0.3, random_state=0)

reg_sm3 = sm.OLS(y_train3, X_train3).fit()
reg_sm3.summary()

y_hat3 = reg_sm3.predict(X_test3)

rmse3 = math.sqrt(mean_squared_error(y_hat3,y_test3))

plt.scatter(y_hat3,y_test3)


pd.Series([variance_inflation_factor(X3.values,i) for i in range(X3.shape[1])],index=X3.columns)


from sklearn.ensemble import RandomForestRegressor

rf = RandomForestRegressor(n_estimators = 300)
rf.fit(X_train3,y_train3)
ypred_rf = rf.predict(X_test3)
rf.score(X_test3,y_test3)


#withrefs
X = df_ref.drop(['Unnamed: 0','date','away_team','home_team','actual_score','line_2H',
                'OU_2H','line_open','line_close','OU_close','away_ML','away_2H','home_2H','home_ML','away_Final','home_Final'], axis=1)

Y = df_ref.actual_score.values
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=0)

reg_sm3 = sm.OLS(y_train, X_train).fit()
reg_sm3.summary()









#cross validation 5 fold 
from sklearn.model_selection import cross_val_score 
import numpy as np
reg4 = LinearRegression().fit(X_train3, y_train3)
reg4.score(X_test3,y_test3)

reg4 = LinearRegression()
scores = cross_val_score(reg4,X3,y3, cv=5, scoring = 'neg_mean_absolute_error')
np.abs(scores)

reg4 =  RandomForestRegressor(n_estimators = 300)
scores = cross_val_score(reg4,X3,y3, cv=5, scoring = 'neg_mean_absolute_error')
np.abs(scores)



reg4 = LinearRegression()
scores = cross_val_score(reg4,X3,y3, cv=5, scoring = 'neg_mean_absolute_error')
np.sqrt(np.abs(scores))


Xdf = df_ref.drop(['Unnamed: 0','date','away_team','home_team','line_2H',
                'OU_2H','line_open','line_close','OU_close','away_2H','home_2H','away_Final','home_Final', 'constant'], axis=1)

X_train, X_test, y_train, y_test = train_test_split(Xdf.drop('actual_score',axis=1), Xdf[['actual_score']], test_size=0.3, random_state=0)

df_trn = X_train.copy()
df_trn['actual_score'] = y_train
df_trn.columns
from fastai.tabular import *

procs = [Categorify, Normalize]
dep_var = 'actual_score'
cont_names = ['away_traveled', 'time_diff', 'home_ML', 'away_ML','OU_open', 'line_movement', 'OU_movement']
cat_names = [i for i in df_trn.columns if i not in cont_names+['actual_score']]
embed = {i:1 for i in cat_names}
valid_idx = range(len(df_trn)-600, len(df_trn))
df_trn.columns = df_trn.columns.astype(str)
df_trn.to_csv('ai_train.csv')
df_trn[cat_names] = df_trn[cat_names].replace(0,'No')
df_trn[cat_names].replace(1,'Yes')

path = 'Users/Ken/Documents/NBA_Over_Under/ai_train.csv'

db1 = TabularList.from_df(path=path, df=df_trn, cat_names=cat_names, cont_names=cont_names, procs=procs)
db2 = db1.split_from_df(col='actual_score')
db3 = db2.label_from_df(cols=dep_var, label_cls=FloatList)
db= db3.databunch()

learn = tabular_learner(db, layers =[200,100], emb_szs =embed, metrics =mean_absolute_error)
learn.fit_one_cycle(1,1e-2)


data = (TabularList.from_df(df_trn, path='.', cat_names=cat_names, cont_names=cont_names, procs=procs)
                        .split_by_idx(list(range(0,200)))
                        .label_from_df(cols=dep_var, label_cls=FloatList)
                        .databunch())

learn = tabular_learner(data, layers=[1000, 200, 15], metrics=mean_absolute_error, emb_drop=0.1, callback_fns=ShowGraph)
learn.lr_find()
learn.fit_one_cycle(1, max_lr=slice(1e-03))


