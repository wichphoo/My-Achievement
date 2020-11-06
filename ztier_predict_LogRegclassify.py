# -*- coding: utf-8 -*-
"""Ztier_predict_LRclassify.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/12IPIA3jaxkkdJv3UkMReTfnpjaY35oRl
"""

import numpy as np
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import RobustScaler
from sklearn.datasets import make_classification
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import SGDClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import cross_val_score

"""Import"""

from google.colab import files
uploaded = files.upload()

import io
df = pd.read_csv(io.BytesIO(uploaded['Ztier_total.csv']))

"""Prep Data"""

del df['MerchantID']
#convert object to float64
df['Average - Short-Term Debt/Equity'] = pd.to_numeric(df['Average - Short-Term Debt/Equity'], errors='coerce')
df['Average - Cash/Net Sales'] = pd.to_numeric(df['Average - Cash/Net Sales'], errors='coerce')
df['Average - Ebit/Sales'] = pd.to_numeric(df['Average - Ebit/Sales'], errors='coerce')
df['Average - Net Income/Sales'] = pd.to_numeric(df['Average - Net Income/Sales'], errors='coerce')
df['Average - Ebitda/Interest Expense'] = pd.to_numeric(df['Average - Ebitda/Interest Expense'], errors='coerce')
df['Average - Ebit/Interest Expenses'] = pd.to_numeric(df['Average - Ebit/Interest Expenses'], errors='coerce')
df['Average - Account Payable/Sales'] = pd.to_numeric(df['Average - Account Payable/Sales'], errors='coerce')
df = df.fillna(0)

df['Z-score Tier'].replace({-1:0}, inplace=True)

df2=df

cols_to_normalize=df2.columns[0:29]

col_values=df2[cols_to_normalize].values

#col_scaled=MinMaxScaler().fit_transform(col_values)
col_scaled=RobustScaler().fit_transform(col_values)

df2[cols_to_normalize]=pd.DataFrame(col_scaled,columns=cols_to_normalize)

#check normalize
newdf = df2.agg(['min', 'max','mean'])
newdf

X=df2[df2.columns[0:29]]

y=df2[df2.columns[-1:]]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=5)

"""SGD Model (try)"""

#SGD log
SGD = SGDClassifier(loss='log', random_state=5, alpha=0.0001, max_iter=1000, l1_ratio=.15)

#CV accuracy
SGDCV = cross_val_score(SGD, X_train, y_train, cv=10)

SGDCV

np.mean(SGDCV)

#Test accuracy
SGD.fit(X_train, y_train)

print("test accuracy: %0.5f" % SGD.score(X_test, y_test))

"""Model Logreg"""

#log req
logreg = LogisticRegression(random_state=5)

#CV accuracy
logreqCV = cross_val_score(logreg, X_train, y_train, cv=10)

logreqCV

np.mean(logreqCV)

logreg.fit(X_train, y_train)

print("test accuracy: %0.5f" % logreg.score(X_test, y_test))

from sklearn.externals import joblib

joblib_file = "LR_model.pkl"  
joblib.dump(logreg, joblib_file)

from google.colab import files
files.download('LR_model.pkl')

"""Confuse"""

y_pred=logreg.predict(X)

y_pred = y_pred.tolist()

conf=metrics.confusion_matrix(y, y_pred)

conf=pd.DataFrame(conf)
conf

print(metrics.classification_report(y, y_pred))

"""Export Pretable"""

pre_prob = logreg.predict_proba(X)

pre_prob = pd.DataFrame(pre_prob)

pre_prob1 = pre_prob[0].values.tolist()

#pre_prob = logreg.predict_proba(X) again
pre_prob2 = pre_prob[1].values.tolist()

#Create Prediction table

y_all = y['Z-score Tier'].values.tolist()

#Recall merchantID to make prediction table
import io
df = pd.read_csv(io.BytesIO(uploaded['Ztier_total.csv']))
dfwithID = df

ID = dfwithID['MerchantID'].tolist()

dataframe = pd.DataFrame([ID, y_all, y_pred, pre_prob1, pre_prob2], index =['MerchantID', 'y_actual', 'y_predict', 'Predict_Prob(0)', 'Predict_Prob(1)'])

dataframe = dataframe.T

dataframe.to_csv('Prediction LogReq.csv')

from google.colab import files
files.download('Prediction LogReq.csv')

"""ROC"""

#acc when pred with all data
print("Accuracy:",metrics.accuracy_score(y_all, y_pred))

from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve
from sklearn.metrics import plot_roc_curve
from matplotlib import pyplot
from matplotlib import pyplot as plt

plot_roc_curve(logreg, X, y)

