#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
from sklearn.cluster import KMeans


# In[2]:


df=pd.read_csv('/Users/wichphoopoonnasee/Desktop/Parking Performance/cluster/healtcheckdata_20200911.csv')


# In[39]:


df_raw=pd.read_csv('/Users/wichphoopoonnasee/Desktop/Parking Performance/cluster/healtcheckdata_20200911.csv')


# In[9]:


df.info()


# In[5]:


del df['stationcode']
del df['stationid']


# In[6]:


def clean_dataset(df):
    assert isinstance(df, pd.DataFrame), "df needs to be a pd.DataFrame"
    df.dropna(inplace=True)
    indices_to_keep = ~df.isin([np.nan, np.inf, -np.inf]).any(1)
    return df[indices_to_keep].astype(np.float64)


# In[7]:


#df=df.set_index(['stationid','logtime'])


# In[8]:


df=clean_dataset(df)


# In[10]:


df.describe()


# In[11]:


# standardizing the data
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
data_scaled = scaler.fit_transform(df)


# In[12]:


#kmeans = KMeans(n_clusters=3, init='k-means++')


# In[13]:


SSE = []
for cluster in range(1,20):
    kmeans = KMeans(n_jobs = -1, n_clusters = cluster, init='k-means++')
    kmeans.fit(data_scaled)
    SSE.append(kmeans.inertia_)

# converting the results into a dataframe and plotting them
frame = pd.DataFrame({'Cluster':range(1,20), 'SSE':SSE})
plt.figure(figsize=(12,6))
plt.plot(frame['Cluster'], frame['SSE'], marker='o')
plt.xlabel('Number of clusters')
plt.ylabel('Inertia')


# In[14]:


kmeans.inertia_


# In[15]:


kmeans = KMeans(n_jobs = -1, n_clusters = 4, init='k-means++')
kmeans.fit(data_scaled)
pred = kmeans.predict(data_scaled)


# In[16]:


frame = pd.DataFrame(data_scaled)
frame['cluster'] = pred
frame['cluster'].value_counts()


# In[34]:


cluster_df=frame['cluster']


# In[38]:


#del df_raw['stationcode']


# In[40]:


df_raw=df_raw.set_index(['stationid','stationcode'])


# In[41]:


df_raw_clean=clean_dataset(df_raw)


# In[42]:


df_raw_clean=df_raw_clean.reset_index(level=['stationid','stationcode'])


# In[43]:


df1=pd.concat([df_raw_clean,cluster_df], axis=1)


# In[44]:


c0_df=df1[df1['cluster']==0]
c1_df=df1[df1['cluster']==1]
c2_df=df1[df1['cluster']==2]
c3_df=df1[df1['cluster']==3]


# In[45]:


c0_stat=c0_df.agg(['max', 'min','mean'])


# In[46]:


del c0_stat['stationid']
#del c0_stat['logtime']


# In[47]:


c1_stat=c1_df.agg(['max', 'min','mean'])


# In[48]:


del c1_stat['stationid']
#del c1_stat['logtime']


# In[49]:


c2_stat=c2_df.agg(['max', 'min','mean'])


# In[50]:


del c2_stat['stationid']
#del c2_stat['logtime']


# In[51]:


c3_stat=c3_df.agg(['max', 'min','mean'])


# In[52]:


del c3_stat['stationid']
#del c3_stat['logtime']


# In[53]:


df_name=df_raw1[['stationid','stationcode']]


# In[54]:


df_2 = df1.merge(df_name, on = ['stationid'], how = 'left')


# In[57]:


df_2


# In[58]:


df_2.drop_duplicates(['stationid'], inplace=True)


# In[59]:


c_all=pd.concat([c0_stat,c1_stat,c2_stat,c3_stat], axis=0)


# In[60]:


writer = pd.ExcelWriter('cluster_result.xlsx', engine='xlsxwriter')


# In[61]:


df_2.to_excel(writer, sheet_name='data', index = False)


# In[62]:


c0_stat.to_excel(writer, sheet_name='cluster0', index = True)


# In[63]:


c1_stat.to_excel(writer, sheet_name='cluster1', index = True)


# In[64]:


c2_stat.to_excel(writer, sheet_name='cluster2', index = True)


# In[65]:


c3_stat.to_excel(writer, sheet_name='cluster3', index = True)


# In[66]:


c_all.to_excel(writer, sheet_name='stat', index = True)


# In[67]:


writer.save()


# In[68]:


df_2['stationid'].nunique()


# In[ ]:




