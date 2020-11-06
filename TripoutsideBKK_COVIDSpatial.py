#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os 


# In[2]:


#Import
userhome = os.path.expanduser('~')
#veh_log = pd.read_csv(userhome + r'/Desktop/04 Covid19 spatial/Vehicle-log-2020-05-26.csv')
#veh_log = pd.read_csv(userhome + r'/Desktop/04 Covid19 spatial/Vehicle-log_May-June 2020.csv')
#resv = pd.read_csv(userhome + r'/Desktop/Resv-Report-2020-07-03.csv')
resv = pd.read_csv(userhome + r'/Desktop/04 Covid19 spatial/Reservation-2020-07-11.csv')


# In[3]:


userhome = os.path.expanduser('~')
#veh_log = pd.read_csv(userhome + r'/Desktop/04 Covid19 spatial/20200721/Vehicle-log2-2020-07-11.csv')
veh_log = pd.read_csv(userhome + r'/Desktop/04 Covid19 spatial/20200721/Vehicle-log-2020-07-11.csv')


# In[4]:


df=veh_log


# In[6]:


df.head()


# Prep Data

# In[7]:


del df['bat_id']
del df['bat_level']
del df['gpsenginelockstate']
del df['gpsdoorlockstate']


# In[8]:


df['logtime'] = pd.to_datetime(df['logtime'], errors='coerce')
df['station_dt'] = pd.to_datetime(df['station_dt'], errors='coerce')


# In[9]:


#sta0 = df[df['stationid'] == 0].index
#df.drop(sta0, inplace=True)


# Stop Veh

# In[10]:


stop_df=df[df['speed']==0]


# In[11]:


disveh=df[(df['charge']==0)|(df['fuel']==0)]


# In[12]:


df2=pd.concat([stop_df, disveh, disveh]).drop_duplicates(keep=False)


# In[13]:


#df2=df2[df2['hdop']>0]


# In[14]:


def haversine_distance(lat1, lon1, lat2, lon2):
   r = 6371
   phi1 = np.radians(lat1)
   phi2 = np.radians(lat2)
   delta_phi = np.radians(lat2 - lat1)
   delta_lambda = np.radians(lon2 - lon1)
   a = np.sin(delta_phi / 2)**2 + np.cos(phi1) * np.cos(phi2) *   np.sin(delta_lambda / 2)**2
   res = r * (2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a)))
   return np.round(res*1000, 2)


# In[15]:


df2['distance_m'] = haversine_distance(df2['latitude'], df2['longitude'], df2['latitude'].shift(1), df2['longitude'].shift(1))


# In[16]:


l=[df2.iloc[x,14] in df2.iloc[x-1:x,14].tolist() for x in np.arange(1,len(df2))]+['']


# In[17]:


df2['track_state']=l


# In[18]:


l2=[df2.iloc[x,1] in df2.iloc[x-1:x,1].tolist() for x in np.arange(1,len(df2))]+['']


# In[19]:


df2['track_resv']=l2


# In[20]:


df2['stop_duration']=''


# In[21]:


n=0


# In[24]:


sta0 = df2[df2['stationid'] == 0].index
df2.drop(sta0, inplace=True)


# In[27]:


df2.head(50)


# In[26]:


for i in range(len(df2)):
    engine_state1 = df2.iloc[i, 14]
    #n=0
    t1 = df2.iloc[i-n, 2]
    t2 = df2.iloc[i, 2]
    resv1 = df2.iloc[i-1, 1]
    resv2 = df2.iloc[i, 1]
    t=t2-t1
    
    if (engine_state1=='STOP') & (resv1==resv2):
        n=n+1
        df2.iloc[i, 20]=t
    else:
        n=0
        df2.iloc[i, 20]=pd.Timedelta('1000 days')


# In[28]:


df2['stop_duration']=pd.to_timedelta(df2['stop_duration'])


# In[29]:


df2['stop_duration']=df2['stop_duration']/np.timedelta64(1, 'm')


# In[31]:


df3=df2[(((df2['stop_duration']>15)&(df2['stop_duration']<1440000))&(df2['track_state']==False))&(df2['distance_m']<100)|
        (((df2['stop_duration']>15)&(df2['stop_duration']<1440000))&(df2['track_resv']==False))&(df2['distance_m']<100)]


# Merge Resv Data

# In[32]:


resv['resv_type']=''


# In[33]:


for i in range(len(resv)):
    
    if (resv.iloc[i, 6]>8):
        resv.iloc[i, 12]='daily'
    else:
        resv.iloc[i, 12]='hourly'


# In[34]:


merge_data=pd.merge(resv,df3,how='inner',left_on='reservationno',right_on='reservationno')


# In[35]:


#del merge_data['reservationstate']
#del merge_data['vehicleid_x']
#del merge_data['stationid_x']
#del merge_data['receiptno']
#merge_data.rename(columns={'vehicleid_y':'vehicleid'},inplace=True)
#merge_data.rename(columns={'stationid_y':'stationid'},inplace=True)


# In[36]:


df4=merge_data


# In[37]:


df4.info()


# Point in Polygon

# In[38]:


from shapely.geometry import Point, Polygon
import geopandas as gpd
import shapely


# In[40]:


#IKEA BangYai
IKBY=[(100.409692,13.880704),(100.412117,13.880870),(100.412288,13.879683),(100.414756,13.878516),(100.413791,13.874433),(100.410293,13.874329)]
#IKEA BangNa
IKBN=[(100.679781,13.641183),(100.682412,13.644951),(100.682966,13.648517),(100.680173,13.650356),(100.676204,13.647306),(100.676227,13.644839),(100.676550,13.643000),(100.679043,13.642058)]


# In[39]:


BKK=[(99.836901, 14.056007), (99.908640, 14.120530), (100.042775 , 14.155426), (100.136778, 14.146564), (100.212504, 14.179478)
, (100.283006, 14.169351), (100.280395, 14.127573), (100.309119, 14.137702), (100.345676, 14.114911), (100.511488, 14.128839)
, (100.549350, 14.114911), (100.511488, 14.128839), (100.887502, 14.273130), (100.894030, 14.249088), (100.948866, 14.269334)
, (100.943644, 14.233902), (100.914920, 14.222512), (100.909698, 13.841251), (100.937116, 13.814628), (100.858779, 13.700495)
, (100.948952, 13.666509), (100.961120, 13.643845), (100.912446, 13.592597), (100.912446, 13.572883), (100.904333, 13.554153)
, (100.890352, 13.561741), (100.871976, 13.492338), (100.849359, 13.479967), (100.625314, 13.522575), (100.077218, 13.429150)
, (100.029846, 13.514199), (100.031061, 13.749108), (99.970328, 13.721970), (99.938747, 13.750288), (99.966684, 13.808093)
, (99.958181, 13.835221), (99.901092, 13.843477), (99.899878, 13.904797), (99.926514, 13.922614), (99.919931, 13.942250)
, (99.890226, 13.943490), (99.858544, 13.964423), (99.847198, 13.996973), (99.833387, 14.000802)]


# In[41]:


poly1 = Polygon(IKBY)
poly2 = Polygon(IKBN)
poly3 = Polygon(BKK)


# In[42]:


#geometry=df4.apply(lambda row: shapely.geometry.Point((row['latitude'], row['longitude'])), axis=1)
geometry=df4.apply(lambda row: shapely.geometry.Point((row['longitude'], row['latitude'])), axis=1)


# In[45]:


df4


# In[44]:


df4 = gpd.GeoDataFrame(df4, geometry=geometry)


# In[ ]:


df4['IKEA']=''
df4['BKK']=''


# In[ ]:


for i in range(len(df4)):
    point = df4.loc[i, 'geometry']
    
    if (point.within(poly1)):
        df4.loc[i, 'IKEA']='BangYai'
    elif (point.within(poly2)):
        df4.loc[i, 'IKEA']='BangNa'
    else:
        df4.loc[i, 'IKEA']='None' 


# In[ ]:


for i in range(len(df4)):
    point = df4.loc[i, 'geometry']
    
    if (point.within(poly3)):
        df4.loc[i, 'BKK']='Inside'
    else:
        df4.loc[i, 'BKK']='Outside' 


# In[ ]:


df4.to_csv('spatial.csv')


# Map Plot

# In[ ]:


userhome = os.path.expanduser('~')
df4 = pd.read_csv(userhome + r'/Desktop/04 Covid19 spatial/20200721/spatial.csv')


# In[ ]:


df4=df4[['reservationno','reservestarttime','reservestoptime','reservehours','actualhours','resv_type','latitude',
        'longitude','IKEA','BKK','geometry','logtime_y']]


# In[ ]:


df4.info()


# In[ ]:


#geometry=df4.apply(lambda row: shapely.geometry.Point((row['latitude'], row['longitude'])), axis=1)
geometry=df4.apply(lambda row: shapely.geometry.Point((row['longitude'], row['latitude'])), axis=1)


# In[ ]:


crs={'init': 'epsg:4326'}


# In[ ]:


point = gpd.GeoDataFrame(df4, crs=crs, geometry=geometry)


# In[ ]:


userhome = os.path.expanduser('~')
shp = gpd.read_file(userhome + r'/Desktop/04 Covid19 spatial/Shape_File/Province/TH_Province.shp')


# In[ ]:


shp = shp.to_crs(epsg=4326)


# In[ ]:


df4['PROV']=''


# In[ ]:


#df4.loc[0,'geometry'].within(shp.loc[0,'geometry'])


# In[ ]:


for i in range(len(df4)):
    point = df4.loc[i, 'geometry']
    
    for j in range(len(shp)):
        poly = shp.loc[j, 'geometry']
        
        if (point.within(poly)):
            df4.loc[i, 'PROV'] = shp.loc[j, 'PROV_NAME'] 
            
        else :
            pass


# In[ ]:


df4.info()


# In[ ]:


df4.head()


# In[ ]:


for i in range(len(df4)):
    
    if (df4.loc[i, 'reservehours']>8):
        df4.loc[i, 'resv_type']='daily'
    else:
        df4.loc[i, 'resv_type']='hourly'


# In[ ]:


df4.to_csv('b.csv')


# concat

# In[ ]:


userhome = os.path.expanduser('~')
a = pd.read_csv(userhome + r'/Desktop/04 Covid19 spatial/20200722/a.csv')
b = pd.read_csv(userhome + r'/Desktop/04 Covid19 spatial/20200722/b.csv')


# In[ ]:


ab=pd.concat([a,b], axis=0)


# In[ ]:


ab.to_csv('ab.csv')


# In[ ]:




