#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import os


# In[2]:


import pymysql
import pymysql.cursors


# In[30]:


import datetime as dt
from datetime import datetime


# In[4]:


user = input("Username: ")
passwd = input("Password: ")


# In[5]:


# Open database connection
db = pymysql.connect(host="devpartners.haupcar.com",
                     user=user,
                     passwd=passwd,
                     db="haupcar",
                     charset='utf8')


# In[6]:


# prepare a cursor object using cursor() method
cursor = db.cursor()


# In[7]:


#Query service+MA days
query2 = '''SELECT v.groupid, v.vehiclecode, l.logtime, 
        l.vehicleid, l.vehiclestatus, l.stationid, l.stationcode 
        
        
        FROM vehicle_station_log as l
        LEFT JOIN vehicle as v
        ON l.vehicleid = v.vehicleid
        WHERE (l.logtime >= '2020-07-01') AND (l.logtime <= '2020-09-30' )
        ORDER BY v.groupid, l.logtime
        '''


# In[8]:


#getting user data from the table
cursor.execute(query2)


# In[9]:


#fetching all data from the cursor object
query2_result = cursor.fetchall()


# In[10]:


#get header
field_names = [i[0] for i in cursor.description]
totalday_df = pd.DataFrame(query2_result,columns =field_names)


# In[11]:


# disconnect from server
db.close()


# In[12]:


totalday_df2=totalday_df[totalday_df['vehiclecode'].isnull()==False]


# In[13]:


totalday_df2.sort_values(by=['vehicleid','logtime'], inplace=True, ascending=True)


# In[14]:


totalday_df2['duration']=''


# In[16]:


n=1


# In[17]:


for i in range(len(totalday_df2)):
    
    vehstatus1 = totalday_df2.iloc[i-n, 4]
    vehstatus2 = totalday_df2.iloc[i, 4]
    v1 = totalday_df2.iloc[i-1, 3]
    v2 = totalday_df2.iloc[i, 3]
    
    if (vehstatus1=='MA') & (vehstatus2=='MA') & (v1==v2):
        n=n+1
        totalday_df2.iloc[i, 7]=n
    elif (vehstatus2=='MA') & (v1!=v2):
        totalday_df2.iloc[i, 7]=1
        n=1
    elif (vehstatus1!='MA') & (vehstatus2=='MA') & (v1==v2):
        totalday_df2.iloc[i, 7]=1
        n=1
    else:
        n=1
        totalday_df2.iloc[i, 7]=0


# In[21]:


last_df = totalday_df2.sort_values(by=['vehicleid','logtime']).drop_duplicates(['vehicleid'], keep='last')


# In[23]:


lastMA_df = last_df[last_df['vehiclestatus']=='MA']


# In[26]:


lastMA_df['logtime'] = lastMA_df['logtime'].dt.strftime('%Y-%m-%d')


# In[33]:


lastMAnow_df = lastMA_df[lastMA_df['logtime']==datetime.today().strftime('%Y-%m-%d')]


# In[35]:


#export excel
writer = pd.ExcelWriter('MA_check.xlsx', engine='xlsxwriter')


# In[38]:


lastMAnow_df.to_excel(writer, sheet_name='todayMA', index = False)
lastMA_df.to_excel(writer, sheet_name='allMA', index = False)
totalday_df2.to_excel(writer, sheet_name='total', index = False)


# In[39]:


writer.save()


# In[ ]:




