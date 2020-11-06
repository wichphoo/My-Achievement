#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd 
import os


# In[2]:


from sklearn import metrics
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier


# In[3]:


from matplotlib import pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# In[88]:


userhome = os.path.expanduser('~')
df = pd.read_csv(userhome + r'/Desktop/Parking Performance/locationfactor/parkingdata_20200821.csv')


# In[ ]:


#userhome = os.path.expanduser('~')
#df = pd.read_csv(userhome + r'/Desktop/Parking Performance/cluster/20200911/locationfactor.csv')


# In[ ]:


#df.info()


# In[ ]:


#del df['stationid']
#del df['stationcode_x']
#del df['No. of parking']
#del df['No. of Service Vehicle days']
#del df['No. of Service Vehicle/days']
#del df['Cost/Parking']
#del df['Offline marketing']
#del df['Zone']
#df = pd.get_dummies(df)


# In[58]:


del df['TRUE']
del df['stationcode']
del df['No. of parking']
del df['No. of Service Vehicle days']
del df['No. of Service Vehicle/days']
del df['Cost/Parking']
del df['Offline marketing']
del df['Zone']
del df['hotel']
#del df['office']
#del df['shopping mall/convenient store_FALSE']
del df['gas station']
df = pd.get_dummies(df)


# In[59]:


df.rename(columns={'UT':'%UT'},inplace=True)


# In[60]:


df['UT']=''


# In[61]:


df['UT'] = np.where(df['%UT']>=14, 'VG', df['UT'])
df['UT'] = np.where((df['%UT']<14) & (df['%UT']>=9), 'G', df['UT'])
df['UT'] = np.where((df['%UT']<9) & (df['%UT']>=4), 'F', df['UT'])
df['UT'] = np.where(df['%UT']<4, 'P', df['UT'])


# In[62]:


df['UT'].unique()


# In[63]:


del df['%UT']


# In[39]:


#MAPE function
def mean_absolute_percentage_error(y_true, y_pred): 
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100


# In[72]:


ranks = {}


# In[73]:


def ranking(ranks, names, order=1):
    ranks = (order*np.array([ranks]).T).T[0]
    ranks = map(lambda x: round(x,2), ranks)
    return dict(zip(names, ranks))


# In[64]:


df_UT = df[df['UT'].isnull()==False]


# In[65]:


y1 = df_UT.UT.values
x1 = df_UT.drop(['UT'], axis = 1)
colnames = x1.columns


# In[66]:


rf1 = RandomForestClassifier(n_jobs=-1, n_estimators=1000, min_samples_leaf=1, verbose=1)
rf1.fit(x1,y1)


# In[67]:


y1_pred = rf1.predict(x1)


# In[71]:


print("Accuracy:",metrics.accuracy_score(y1, y1_pred))


# In[74]:


ranks["RF1"] = ranking(rf1.feature_importances_, colnames);


# In[75]:


feature_imp = pd.Series(rf1.feature_importances_,colnames).sort_values(ascending=False)
feature_imp


# In[76]:


# Create empty dictionary to store the mean value calculated from all the scores
r = {}
for name in colnames:
    r[name] = round(np.mean([ranks[method][name] 
                             for method in ranks.keys()]), 2)
 
methods = sorted(ranks.keys())
ranks["Mean"] = r
methods.append("Mean")
 
print("\t%s" % "\t".join(methods))
for name in colnames:
    print("%s\t%s" % (name, "\t".join(map(str, 
                         [ranks[method][name] for method in methods]))))


# In[77]:


# Put the mean scores into a Pandas dataframe
meanplot = pd.DataFrame(list(r.items()), columns= ['UT','Feature Importance'])

# Sort the dataframe
meanplot = meanplot.sort_values('Feature Importance', ascending=False)


# In[78]:


# Let's plot the ranking of the features
sns.factorplot(x="Feature Importance", y="UT", data = meanplot, kind="bar", 
               size=5, aspect=1.9, palette='coolwarm')


# In[79]:


userhome = os.path.expanduser('~')
df_all = pd.read_csv(userhome + r'/Desktop/Parking Performance/locationfactor/allscenario2.csv')


# In[80]:


yall_pred = rf1.predict(df_all)


# In[81]:


df1=pd.DataFrame(data=yall_pred)


# In[82]:


df2=pd.concat([df_all,df1], axis=1)


# In[ ]:


from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report


# In[ ]:


matrix = classification_report(y1,y1_pred,labels=['S','A','B','C'])


# In[ ]:


print('Classification report : \n',matrix)
