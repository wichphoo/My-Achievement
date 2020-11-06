#!/usr/bin/env python
# coding: utf-8

# In[9]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os 


# In[10]:


import pymysql
import pymysql.cursors


# In[11]:


user = input("Username: ")
passwd = input("Password: ")


# In[12]:


# Open database connection
db = pymysql.connect(host="devpartners.haupcar.com",
                     user=user,
                     passwd=passwd,
                     db="haupcar",
                     charset='utf8')


# In[13]:


# prepare a cursor object using cursor() method
cursor = db.cursor()


# In[14]:


#Query service-days
q1 = '''SELECT v.vehicleid, v.reservationno, v.logtime, v.latitude, v.longitude, v.enginestate, v.speed
              
        FROM vehicle_interval_log as v
        WHERE (v.logtime >= '2020-08-24') AND (v.logtime <= '2020-09-30')
        AND (v.vehicleid=623 OR v.vehicleid=612 OR v.vehicleid=628 OR v.vehicleid=642 
            OR v.vehicleid=648 OR v.vehicleid=649)
        ORDER BY v.logtime
        '''


# In[15]:


cursor.execute(q1)


# In[16]:


q1_result = cursor.fetchall()


# In[17]:


q1_field_names = [i[0] for i in cursor.description]
vehlog_df = pd.DataFrame(q1_result,columns =q1_field_names)


# In[18]:


db.close()


# In[19]:


vehlog_df['logtime'] = pd.to_datetime(vehlog_df['logtime'], errors='coerce')


# In[20]:


stop_df=vehlog_df[vehlog_df['speed']==0]


# In[21]:


def haversine_distance(lat1, lon1, lat2, lon2):
   r = 6371
   phi1 = np.radians(lat1)
   phi2 = np.radians(lat2)
   delta_phi = np.radians(lat2 - lat1)
   delta_lambda = np.radians(lon2 - lon1)
   a = np.sin(delta_phi / 2)**2 + np.cos(phi1) * np.cos(phi2) *   np.sin(delta_lambda / 2)**2
   res = r * (2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a)))
   return np.round(res*1000, 2)


# In[22]:


stop_df['distance_m'] = haversine_distance(
    stop_df['latitude'], stop_df['longitude'], stop_df['latitude'].shift(1), stop_df['longitude'].shift(1))


# In[23]:


l1=[stop_df.iloc[x,5] in stop_df.iloc[x-1:x,5].tolist() for x in np.arange(1,len(stop_df))]+['']


# In[24]:


stop_df['track_state']=l1


# In[25]:


l2=[stop_df.iloc[x,1] in stop_df.iloc[x-1:x,1].tolist() for x in np.arange(1,len(stop_df))]+['']


# In[26]:


stop_df['track_resv']=l2


# In[27]:


stop_df['stop_duration']=''


# In[28]:


n=0


# In[29]:


for i in range(len(stop_df)):
    engine_state = stop_df.iloc[i, 5]
    t1 = stop_df.iloc[i-n, 2]
    t2 = stop_df.iloc[i, 2]
    resv1 = stop_df.iloc[i-1, 1]
    resv2 = stop_df.iloc[i, 1]
    t=t2-t1
    
    if (engine_state=='STOP') & (resv1==resv2):
        n=n+1
        stop_df.iloc[i, 10]=t
    else:
        n=0
        stop_df.iloc[i, 10]=pd.Timedelta('1000 days')


# In[30]:


stop_df['stop_duration']=pd.to_timedelta(stop_df['stop_duration'])


# In[31]:


stop_df['stop_duration']=stop_df['stop_duration']/np.timedelta64(1, 'm')


# In[32]:


stop_df2=stop_df[(((stop_df['stop_duration']>15)&(stop_df['stop_duration']<1440000))&(stop_df['track_state']==False))&(stop_df['distance_m']<100)|
                 (((stop_df['stop_duration']>15)&(stop_df['stop_duration']<1440000))&(stop_df['track_resv']==False))&(stop_df['distance_m']<100)]


# In[61]:


stop_df2.to_csv('stopveh.csv', index=False)


# In[1]:


#outside KU


# In[43]:


from shapely.geometry import Point, Polygon
import geopandas as gpd
import shapely


# In[3]:


KU=[(100.561851,13.847501),(100.571389,13.842036),(100.572698,13.844370),(100.572582,13.856489),(100.566134,13.855541)]


# In[41]:


poly=Polygon(KU)


# In[34]:


geometry=stop_df2.apply(lambda row: shapely.geometry.Point((row['longitude'], row['latitude'])), axis=1)


# In[36]:


stop_df2 = gpd.GeoDataFrame(stop_df2, geometry=geometry)


# In[60]:


stop_df2


# In[38]:


stop_df2['KU']=''


# In[59]:


for i in range(len(stop_df2)):
    point = stop_df2.iloc[i, 11]
    
    if (point.within(poly)):
        stop_df2.iloc[i, 12]='Inside'
    else:
        stop_df2.iloc[i, 12]='Outside' 


# In[ ]:




