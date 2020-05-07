# -*- coding: utf-8 -*-
"""JantaHackTime_v1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1IUNaPLQIGC15F4TF12Tp5qksUB7F8FOA
"""

!wget https://www.dropbox.com/sh/d1mq9gcs9ighksw/AADPVBR6Ulryl0zQtdKiOBLxa?dl=0

!ls

from zipfile import ZipFile
file_name="AADPVBR6Ulryl0zQtdKiOBLxa?dl=0"

with ZipFile(file_name,'r') as zip:
  zip.extractall()
  print("done")

!pip install chart_studio

# Commented out IPython magic to ensure Python compatibility.
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from keras import optimizers
from keras.utils import plot_model
from keras.models import Sequential, Model
from keras.layers.convolutional import Conv1D, MaxPooling1D
from keras.layers import Dense, LSTM, RepeatVector, TimeDistributed, Flatten
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import chart_studio.plotly as py
import plotly.graph_objs as go


# %matplotlib inline
warnings.filterwarnings("ignore")


# Set seeds to make the experiment more reproducible.




train=pd.read_csv("train_6BJx641.csv",parse_dates=['datetime'])
test=pd.read_csv("test_pavJagI.csv",parse_dates=['datetime'])
sample=pd.read_csv("sample_submission_bYgKb77.csv")
train.drop('ID',axis=1,inplace=True)
test.drop('ID',axis=1,inplace=True)

train.shape, test.shape, sample.shape

train.dtypes

from plotly.offline import init_notebook_mode, iplot
daily_consumption= go.Scatter(x=train['datetime'], y=train['electricity_consumption'])
layout = go.Layout(title='Dailyconsumption', xaxis=dict(title='Date'), yaxis=dict(title='Electricity Consumption'))
fig = go.Figure(data=[daily_consumption], layout=layout)
iplot(fig)

from sklearn import preprocessing
le = preprocessing.LabelEncoder()

train['var2'] = le.fit_transform(train['var2'])
test['var2'] = le.fit_transform(test['var2'])

train.columns

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns
import gc
from sklearn.metrics import mean_squared_error
import statsmodels.api as sm
import lightgbm as lgb
plt.style.use('ggplot')
# %matplotlib inline
seed = 433

def date_time_feat(df,column):
    "Extract date time feature"
    df['day'] = df[column].dt.day
    df['dayofweek'] = df[column].dt.dayofweek
    df['month'] = df[column].dt.month
    df['year'] = df[column].dt.year
    
    df['is_month_end'] = df[column].dt.is_month_end.astype('int8')
    df['is_month_start'] = df[column].dt.is_month_start.astype('int8')
    df['weekofyear'] = df[column].dt.weekofyear
    df['date'] = df[column].str[0:11]

train.dtypes

import datetime as dt
df=train
column='datetime'
df['day'] = df[column].dt.day
df['dayofweek'] = df[column].dt.dayofweek
df['month'] = df[column].dt.month
df['year'] = df[column].dt.year
    
df['is_month_end'] = df[column].dt.is_month_end.astype('int8')
df['is_month_start'] = df[column].dt.is_month_start.astype('int8')

df['date'] = df[column].dt.normalize()

df=test
df['day'] = df[column].dt.day
df['dayofweek'] = df[column].dt.dayofweek
df['month'] = df[column].dt.month
df['year'] = df[column].dt.year
    
df['is_month_end'] = df[column].dt.is_month_end.astype('int8')
df['is_month_start'] = df[column].dt.is_month_start.astype('int8')
df['weekofyear'] = df[column].dt.weekofyear
df['date'] = df[column].dt.normalize()

test.head()

f,ax = plt.subplots(1,3,figsize=(14,4))
sns.distplot(train['electricity_consumption'],ax =ax[0])
sns.distplot(np.log(train['electricity_consumption']+1),ax=ax[1], color='b')
sns.boxenplot(train['electricity_consumption'],ax =ax[2])

(train
 .groupby(['month',])
 .agg({'electricity_consumption':['sum',]})
 .unstack()
 .plot(kind='bar',cmap='viridis'))

(train
 .groupby(['month','year'])
 .agg({'electricity_consumption':'mean'})
 .unstack()
 .plot(figsize=(14,5)))

(train
 .groupby(['dayofweek','year'])
 .agg({'electricity_consumption':'mean'})
 .unstack()
 .plot(figsize=(14,5)))

(train
.groupby(['day'])
.agg({'electricity_consumption':['mean','max']})
.plot(figsize=(14,4),kind='bar',stacked=True,cmap='coolwarm'))

(train.groupby('month')
.agg({'electricity_consumption':['min','mean','max']})
 .plot(figsize=(14,4),kind='bar',stacked=True))

(train
 .groupby(['var2','month'])
 .agg({'electricity_consumption':['sum']})
 .unstack()
 .plot(figsize=(14,3),kind='box',stacked=True,cmap='viridis'))
plt.xticks(rotation=90);

(train
 .groupby(['var2','dayofweek'])
 .agg({'electricity_consumption':['sum']})
 .unstack()
 .plot(figsize=(14,3),kind='box',stacked=True,cmap='viridis'))
plt.xticks(rotation=90);

(train
 .groupby(['var2','year'])
 .agg({'electricity_consumption':['sum']})
 .unstack()
 .plot(figsize=(14,3),kind='box',stacked=True,cmap='viridis'))
plt.xticks(rotation=90);

plt.figure(figsize=(14,5))
train['electricity_consumption'].head(1000).plot(color='darkgray')
train['electricity_consumption'].head(1000).rolling(window=23).mean().plot(label='mean')
#train['electricity_consumption'].head(1000).rolling(window=12).median().plot(label='median')
train['electricity_consumption'].head(1000).rolling(window=7).min().plot(label='min',color='g')
train['electricity_consumption'].head(1000).rolling(window=7).max().plot(label='max',color='b')
train['electricity_consumption'].head(1000).rolling(window=7).std().plot(label='std',color='yellow')
plt.legend()
#plt.savefig('Rolli

# Expanding window
plt.figure(figsize=(14,5))
train['electricity_consumption'].head(1000).plot(color='darkgray')
train['electricity_consumption'].head(1000).expanding().mean().plot(label='mean')
#train['sales'].head(1000).rolling(window=12).median().plot(label='median')
train['electricity_consumption'].head(1000).expanding().min().plot(label='min',color='g')
train['electricity_consumption'].head(1000).expanding().max().plot(label='max',color='b')
train['electricity_consumption'].head(1000).expanding().std().plot(label='std',color='yellow')
plt.legend()

def calc_stats(df, end,window,groupby=None,aggregates='mean',value='sales'):
    
    # dates
    last_date = pd.to_datetime(end) - pd.Timedelta(days=1)
    first_date = pd.to_datetime(end) - pd.Timedelta(days= window)
    # Aggregate
    df1 = df[(df.date >=first_date) & (df.date<= last_date) ]
    df_agg = df1.groupby(groupby)[value].agg(aggregates)
    # Change name of columns
    df_agg.name =  str(end).split(' ')[0]+'_' + '_'.join(groupby)+'_'+aggregates+'_'+ str(window)
    return df_agg.reset_index()

#sales_by_store_item
def sales_by_store_item(df, end, aggregates='mean', value='electricity_consumption'):
    
    print('Adding sales by store item')
    data = calc_stats(df,end, window=1,aggregates=aggregates, 
                      groupby=['var2'], value=value)
    print('window 1 added')
    
    for window in  [3,7,14,28,90,180,365]:
        agg = calc_stats(df,end, window=window, aggregates=aggregates,
                         groupby=['var2'], value=value )
        data = pd.merge(data,agg)
        print('window %d added'% window)
    return data

# sales by store item dayofweek
def sales_by_store_item_dayofweek(df, end, aggregates='mean', value='sales'):
    
    print('Adding sales by store item dayofweek')
    data = calc_stats(df,end, window=7, aggregates=aggregates,
                      groupby = ['var2','dayofweek'], value=value)
    print('window 7 added')
    
    for window in  [14,28,28*2,28*3,28*6,28*12]:
        agg = calc_stats(df,end, window=window, aggregates=aggregates,
                         groupby=['var2','dayofweek'], value=value )
        data = pd.merge(data,agg)
        print('window %d added'% window)
    return data

# sales_by_store_item_day
def sales_by_store_item_day(df, end, aggregates='mean', value='sales'):
    
    print('Adding sales by store item day')
    data = calc_stats(df,end, window=365, aggregates=aggregates,
                      groupby = ['var2','day'], value=value)
    print('window 365 added')
    
    return data

# Sales by item
def sales_by_item(df, end, aggregates='mean', value='sales'):
    
    print('Adding sales by item ')
    data = calc_stats(df,end, window=7, aggregates=aggregates,
                      groupby = ['var2'], value=value)
    print('window 7 added')
    
    for window in  [14,28,28*2]:
        agg = calc_stats(df,end, window=window, aggregates=aggregates,
                         groupby=['var2'], value=value )
        data = pd.merge(data,agg)
        print('window %d added'% window)
    return data

def calc_roll_stat(df,end,groupby=None,window=1,aggregate='mean'):
    # Rolling statistics method
    last_date = pd.to_datetime(end) - pd.Timedelta(days=1)
    first_date = pd.to_datetime(end) - pd.Timedelta(days=window)
    df1 = df[(df.date >= first_date) & (df.date <= last_date)]
    
    dfPivot = df1.set_index(['datetime']+groupby)['electricity_consumption'].unstack().unstack()
    dfPivot = dfPivot.rolling(window=window).mean().fillna(method='bfill')
    return dfPivot.stack().stack().rename(aggregate+str(window))

def calc_expand_stat(df,end,window=1,aggregate='mean'):
    # Expanding statistics method
    last_date = pd.to_datetime(end) - pd.Timedelta(days=1)
    first_date = pd.to_datetime(end) - pd.Timedelta(days=window)
    df1 = df[(df.date >= first_date) & (df.date <= last_date)]
    
    dfPivot = df1.set_index(['date','var2'])['electricity_consumption'].unstack().unstack()
    dfPivot = dfPivot.expanding(min_periods=window).mean().fillna(method='bfill')
    dfPivot = dfPivot.stack().stack().rename(aggregate+'_'+str(window)).reset_index()
    return dfPivot

def sales_by_store_item_expading(df,end,aggregate = 'mean', value = 'sales'):
    print('Adding consumption by expanding')
    data =calc_expand_stat(df,end,window=3, aggregate='mean')
    return data

def create_data1(sales,test,date):
    
    # Date input
    for i in range(2):
        end = pd.to_datetime(date) - pd.Timedelta(days=7*i+1)
        print(end)
    
        # Rolling feature
        #for aggregates in ['mean','min','max','sum','std']:
        for aggregates in ['mean','sum']:

            # store/item
            print('-'*20+'Aggregate by '+aggregates+'-'*20)
            data = sales_by_store_item(sales,end, aggregates=aggregates,value='electricity_consumption')
            sales = pd.merge(sales,data,on=['var2'],how='left')
            test = pd.merge(test,data,on=['var2'], how='left')

            # store/item/dayofweek
            df = sales_by_store_item_dayofweek(sales,end, aggregates=aggregates,value='electricity_consumption')
            #data = pd.merge(data,df,)
            sales = pd.merge(sales,df,on=['var2','dayofweek'],how='left')
            test = pd.merge(test,df,on=['var2','dayofweek'], how='left')

            # store/item/day
            df = sales_by_store_item_day(sales,end, aggregates=aggregates,value='electricity_consumption')
            #data = pd.merge(data,df)
            sales = pd.merge(sales,df,on=['var2','day'],how='left')
            test = pd.merge(test,df,on=['var2','day'], how='left')

            # sales/item
            df = sales_by_item(sales,end, aggregates=aggregates, value='electricity_consumption')
            data = pd.merge(data,df)
            #data = pd.merge(sales,data)
            sales = pd.merge(sales,df, on=['var2'],how='left')
            test = pd.merge(test,df, on=['var2'], how='left')

    return sales,test

tes_start = '2013-07-24'

train.columns

# Rolling aggregation or lag feature for diffirend window size
train1,test1 = create_data1(train,test,tes_start)

train1['id'] = np.nan
train1['is_train'] = True
test1['is_train'] = False
test1['electricity_consumption'] = np.nan
# concat train,test
train_test = pd.concat([train1,test1],axis=0)

#Log transform
train_test['electricity_consumption_log'] = np.log(train_test['electricity_consumption']+1)
gc.collect()
train_test.shape

def one_hot_encoding(df,columns):
    print('Original shape',df.shape)
    df = pd.get_dummies(df,drop_first=True,columns=columns)
    print('After OHE', df.shape)
    return df

gc.collect()
train_test = one_hot_encoding(train_test,columns=['month','dayofweek'])

train_test.head()

col_drop = ['id','is_train','electricity_consumption','electricity_consumption_log','datetime']
X = train_test[train_test['is_train'] == True].drop(col_drop, axis=1)
y = train_test[train_test['is_train'] == True]['electricity_consumption_log']
test_new = train_test[train_test['is_train'] == False].drop(col_drop +['date'],axis=1)

# Time series based split
#Time series start time: "2013-01-01 00:00:00" and end time: "2017-12-31 00:00:00"
#Time series start time: "2018-01-01 00:00:00" and end time: "2018-03-31 00:00:00"
tra_start, tra_end = '2013-07-01','2016-07-01'
val_start, val_end = '2016-07-02','2017-06-23'
tes_start = '2013-07-24'
X_train = X[X.date.isin(pd.date_range(tra_start,tra_end))].drop(['date'],axis=1)
X_valid = X[X.date.isin(pd.date_range(val_start, val_end))].drop(['date'],axis=1)
y_train = y[X.date.isin(pd.date_range(tra_start,tra_end))]
y_valid = y[X.date.isin(pd.date_range(val_start, val_end))]
gc.collect()
X.shape,test_new.shape

def smape(y_true,y_pred):
    
    n = len(y_pred)
    masked_arr = ~((y_pred==0)&(y_true==0))
    y_pred, y_true = y_pred[masked_arr], y_true[masked_arr]
    nom = np.abs(y_true - y_pred)
    denom = np.abs(y_true) + np.abs(y_pred)
    smape = 200/n * np.sum(nom/denom)
    return smape
def lgb_smape(pred,train_data):
    ''' 
    Custom evaluvation function
    '''
    label = train_data.get_label()
    smape_val = smape(np.expm1(pred), np.expm1(label))
    return 'SMAPE',smape_val, False

def lgb_model(X_train, X_valid, y_valid, y_test,test_new):
    lgb_param = {}
    lgb_param['boosting_type'] ='gbdt'
    lgb_param['max_depth'] = 9
    lgb_param['num_leaves'] = 2**7
    lgb_param['learning_rate'] = 0.05
    #lgb_param['n_estimators'] = 3000
    lgb_param['feature_fraction'] = 0.9
    lgb_param['bagging_fraction'] = 0.9
    lgb_param['lambda_l1'] = 0.06
    lgb_param['lambda_l2'] =  0.1
    lgb_param['random_state'] = seed
    lgb_param['n_jobs'] = 4
    lgb_param['silent'] = -1
    lgb_param['verbose'] = -1
    lgb_param['metric'] = 'mae'
    
    model = lgb.LGBMRegressor(**lgb_param)
    lgb_train = lgb.Dataset(X_train,y_train)
    lgb_valid = lgb.Dataset(X_valid,y_valid)
    valid_set = [lgb_train,lgb_valid]
    model = lgb.train(params=lgb_param,train_set=lgb_train,valid_sets=valid_set,num_boost_round= 1000,
                      feval=lgb_smape,early_stopping_rounds=50,)
    print('-'*10,'*'*20,'-'*10)
    #model.fit(X_train,y_train, eval_set= [(X_train,y_train),(X_valid,y_valid)],
    #          eval_metric ='rmse',early_stopping_rounds=20,verbose=100)
    
    y_pred = model.predict(X_valid)
    print('Root mean_squared_error','-'*20 ,np.sqrt(mean_squared_error(y_valid, y_pred)))
    y_pred_new = model.predict(test_new)
    return y_pred_new, model

# Model training
y_pred_new, model = lgb_model(X_train, X_valid, y_valid, y_valid,test_new)

lgb.plot_importance(model,max_num_features=20);

sns.distplot(y_pred_new)

y_pred_new1 = np.exp(y_pred_new)-1
y_pred_new2=np.round(y_pred_new1,0)
y_pred_new2

sample['electricity_consumption']=y_pred_new2
sample.to_csv("submit3.csv",index=False)
files.download("submit3.csv")