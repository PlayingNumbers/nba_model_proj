# -*- coding: utf-8 -*-
"""
Created on Sat Dec 21 11:42:01 2019

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



#simple linear regression for year
from sklearn.model_selection import train_test_split,GridSearchCV
from sklearn.linear_model import LinearRegression, Lasso
from sklearn.metrics import mean_squared_error, mean_absolute_error
import math

#multiple linear regression 
from statsmodels.stats.outliers_influence import variance_inflation_factor
import statsmodels.api as sm


X = df_ref.drop(['Unnamed: 0','date','away_team','home_team','actual_score','line_2H',
                'OU_2H','line_open','line_close','OU_close','away_ML','away_2H','home_2H','home_ML','away_Final','home_Final'], axis=1)

Y = df_ref.actual_score.values
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=0)

reg_sm3 = sm.OLS(y_train, X_train).fit_regularized(alpha=0.2, L1_wt=0.5)
reg_sm3.summary()

pd.Series([variance_inflation_factor(X.values,i) for i in range(X.shape[1])],index=X.columns)


# lasso regression
for i in range(1000):
    clf = Lasso(alpha =(i/100))
    clf.fit(X_train,y_train)
    print(clf.score(X_test,y_test))

clf = Lasso(alpha = .1)
clf.fit(X_train,y_train)
print(clf.score(X_train,y_train))

from sklearn.model_selection import cross_val_score 
import numpy as np

for i in range(10):
    clf = Lasso(alpha =(i/10))
    scores = cross_val_score(clf,X,Y, cv=5, scoring = 'neg_mean_squared_error').mean()
    print('alpha + ' + str(i) +': '+ str(np.sqrt(np.abs(scores))))
    
    
# random forest 
# gradient boosted 
from sklearn.ensemble import RandomForestRegressor
rf = RandomForestRegressor(n_estimators = 300)
rf.fit(X_train,y_train)
ypred_rf = rf.predict(X_test)
rf.score(X_test,y_test)


scores = cross_val_score(rf,X,Y, cv=5, scoring = 'neg_mean_squared_error').mean()
print('rf '+ str(np.sqrt(np.abs(scores))))

import xgboost as xgb
import graphviz
data_dmatrix = xgb.DMatrix(data=X,label=Y)



params = {'min_child_weight':[4,5], 'gamma':[i/10.0 for i in range(3,6)],  'subsample':[i/10.0 for i in range(6,11)],
'colsample_bytree':[i/10.0 for i in range(6,11)], 'max_depth': [i for i in range(1,100,2)]}

params = {'min_child_weight':[4,5], 'gamma':[i/10.0 for i in range(3,6)],  'subsample':[i/10.0 for i in range(6,11)],
'colsample_bytree':[i/10.0 for i in range(6,11)], 'max_depth': [2,3,4]}

xgb_reg = xgb.XGBRegressor(nthread=-1)

grid=GridSearchCV(xgb_reg,params,scoring= rmse_scorer())
grid.fit(X_train,y_train)
grid.best_score_
grid.best_estimator_.score(X_test,y_test)

from sklearn.metrics import r2_score, mean_squared_error, make_scorer
import math 
def rmse(y_true,y_pred):
    return np.sqrt(abs(mean_squared_error(y_true,y_pred)))

def rmse_scorer():
    return make_scorer(rmse,greater_is_better=False)


    




cv_results = xgb.cv(dtrain=data_dmatrix, params=params, nfold=3,
                    num_boost_round=100,early_stopping_rounds=20,metrics="rmse", as_pandas=True, seed=123)




xg_reg = xgb.train(params=params, dtrain=data_dmatrix, num_boost_round=10)

xgb.plot_importance(xg_reg)
plt.rcParams['figure.figsize'] = [5, 5]
plt.show()
