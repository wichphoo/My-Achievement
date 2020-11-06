#!/usr/bin/env python
# coding: utf-8

# In[1]:


from oauth2client.service_account import ServiceAccountCredentials
import gspread


# In[2]:


from Google import Create_Service


# In[3]:


import pandas as pd
import numpy as np
import os
import datetime as dt
import math


# In[4]:


import pymysql
import pymysql.cursors


# # Connect with PHP server

# In[14]:


user = input("Username: ")
passwd = input("Password: ")


# In[15]:


# Open database connection
db = pymysql.connect(host="devpartners.haupcar.com",
                     user=user,
                     passwd=passwd,
                     db="haupcar",
                     charset='utf8')


# In[16]:


cursor = db.cursor()


# # Query

# In[8]:


#Query service-days
query = '''SELECT v.groupid, v.vehiclecode, v.vehiclemodel, v.vehicletype,
        l.logtime, l.vehicleid, l.vehiclestatus, l.stationid, l.stationcode 
        
        
        FROM vehicle_station_log as l
        LEFT JOIN vehicle as v
        ON l.vehicleid = v.vehicleid
        WHERE (l.logtime >= '2020-01-01')
            AND l.vehiclestatus = 'SERVICE'
        ORDER BY v.groupid, l.logtime
        '''


# In[9]:


#getting user data from the table
cursor.execute(query)


# In[10]:


#fetching all data from the cursor object
query_result = cursor.fetchall()


# In[11]:


#get header
field_names = [i[0] for i in cursor.description]
service_df = pd.DataFrame(query_result,columns =field_names)


# In[17]:


#call groupid and groupcode from the group table mysql
query_group = '''SELECT g.groupid, g.groupcode, g.name
    FROM `group` as g
    '''


# In[18]:


cursor.execute(query_group)


# In[19]:


query_group_result = cursor.fetchall()


# In[20]:


group_field_names = [i[0] for i in cursor.description]
group_df = pd.DataFrame(query_group_result, columns =group_field_names)


# In[21]:


merged_df = service_df.merge(group_df, on = 'groupid', how = 'left')


# In[22]:


searchfor = ['TEST','BMW i3','Sample model','PCX','FOMM','Bike','EV','COMING SOON','IONIQ']


# In[23]:


index=merged_df[(merged_df['vehiclemodel'].str.contains('|'.join(searchfor)))].index


# In[24]:


merged_df.drop(index, inplace=True)


# In[25]:


merged_df['weeknumber'] = merged_df['logtime'].dt.strftime('%Y-W%W')


# In[26]:


merged_df.rename(columns={'vehiclestatus':'service_days'},inplace=True)


# In[27]:


merged_pivot = merged_df.pivot_table(index=['groupid', 'groupcode', 'vehiclecode','vehicleid','stationid',
                                      'stationcode','name','vehiclemodel','vehicletype', 'weeknumber'], 
                             aggfunc='count')


# In[28]:


merged_pivot=merged_pivot.reset_index()


# In[29]:


del merged_pivot['logtime']
#del merged_pivot['vehiclemodel']
#del merged_pivot['vehiclemodel']


# In[30]:


#Query revenue from resv complete
resv_query1 = '''SELECT r.logtime, r.vehicleid ,r.chargetotal
        
        FROM reservation as r
        WHERE (r.logtime >= '2020-01-01')
            AND r.reservationstate = 'COMPLETE'
            AND r.receiptno != ''
            AND r.reservehours < 168
        ORDER BY r.logtime
        '''


# In[31]:


cursor.execute(resv_query1)


# In[32]:


resv_query_result = cursor.fetchall()


# In[33]:


field_names = [i[0] for i in cursor.description]
resv_df = pd.DataFrame(resv_query_result,columns =field_names)


# In[34]:


resv_df['weeknumber'] = resv_df['logtime'].dt.strftime('%Y-W%W')


# In[35]:


resv_pivot=resv_df.groupby(['vehicleid','weeknumber']).sum().reset_index()


# In[36]:


resv_pivot.rename(columns={'chargetotal':'chargetotal_COMPLETE'},inplace=True)


# In[37]:


merged_df2=merged_pivot.merge(resv_pivot, on=['vehicleid','weeknumber'], how='left')


# In[38]:


#Query revenue from resv
resv_query2 = '''SELECT r.logtime, r.vehicleid ,r.chargetotal
        
        FROM reservation as r
        WHERE (r.logtime >= '2020-01-01')
            AND r.reservationstate = 'DRIVE'
            AND r.reservehours < 168
        ORDER BY r.logtime
        '''


# In[39]:


cursor.execute(resv_query2)


# In[40]:


resv_query_result = cursor.fetchall()


# In[41]:


field_names = [i[0] for i in cursor.description]
drive_df = pd.DataFrame(resv_query_result,columns =field_names)


# In[42]:


drive_df['weeknumber'] = drive_df['logtime'].dt.strftime('%Y-W%W')


# In[43]:


drive_pivot=drive_df.groupby(['vehicleid','weeknumber']).sum().reset_index()


# In[44]:


drive_pivot.rename(columns={'chargetotal':'chargetotal_DRIVE'},inplace=True)


# In[45]:


merged_df3=merged_df2.merge(drive_pivot, on=['vehicleid','weeknumber'], how='left')


# In[46]:


#Query revenue from resv
resv_query3 = '''SELECT r.logtime, r.vehicleid ,r.chargetotal
        
        FROM reservation as r
        WHERE (r.logtime >= '2020-01-01')
            AND r.reservationstate = 'RESERVE'
            AND r.reservehours < 168
        ORDER BY r.logtime
        '''


# In[47]:


cursor.execute(resv_query3)


# In[48]:


resv_query_result = cursor.fetchall()


# In[49]:


field_names = [i[0] for i in cursor.description]
reserve_df = pd.DataFrame(resv_query_result,columns =field_names)


# In[50]:


reserve_df['weeknumber'] = reserve_df['logtime'].dt.strftime('%Y-W%W')


# In[51]:


reserve_pivot=reserve_df.groupby(['vehicleid','weeknumber']).sum().reset_index()


# In[52]:


reserve_pivot.rename(columns={'chargetotal':'chargetotal_RESERVE'},inplace=True)


# In[53]:


merged_df4=merged_df3.merge(reserve_pivot, on=['vehicleid','weeknumber'], how='left')


# In[54]:


merged_df4.fillna(0, inplace=True)


# In[55]:


merged_df4['countvehicle']=merged_df4['service_days']/7


# In[56]:


merged_df4['countvehicle']=np.ceil(merged_df4['countvehicle'])


# In[57]:


sep = '-'


# In[58]:


for i in range(len(merged_df4)):
    
    merged_df4.loc[i, 'groupcode'] = merged_df4.loc[i, 'groupcode'].split(sep, 1)[0]


# In[59]:


#merged_df4['Revenue/Vehicle']=merged_df4['chargetotal_COMPLETE']/merged_df4['countvehicle']
#merged_df4['ONGOING']=merged_df4['chargetotal_DRIVE']
#merged_df4['BACKLOG']=merged_df4['chargetotal_RESERVE']


# In[60]:


sr_df1 = merged_df4.pivot_table(index=['stationid', 'stationcode','weeknumber'], 
                             aggfunc='sum')


# In[61]:


#del sr_df1['BACKLOG']
#del sr_df1['ONGOING']
#del sr_df1['Revenue/Vehicle']
del sr_df1['groupid']
del sr_df1['service_days']
del sr_df1['vehicleid']


# In[62]:


sr_df1=sr_df1.reset_index()


# In[63]:


#sr_df1['Revenue/Station']=sr_df1['chargetotal_COMPLETE']/sr_df1['countvehicle']
#sr_df1['ONGOING']=sr_df1['chargetotal_DRIVE']
#sr_df1['BACKLOG']=sr_df1['chargetotal_RESERVE']


# In[64]:


for i in range(len(merged_df4)):
    
    merged_df4.loc[i, 'weeknumber'] = dt.datetime.strptime(merged_df4.loc[i, 'weeknumber'] + '-0', "%Y-W%W-%w")


# In[65]:


merged_df4['weeknumber'] = merged_df4['weeknumber'].dt.strftime('%Y-%m-%d')


# In[66]:


for i in range(len(sr_df1)):
    
    sr_df1.loc[i, 'weeknumber'] = dt.datetime.strptime(sr_df1.loc[i, 'weeknumber'] + '-0', "%Y-W%W-%w")


# In[67]:


sr_df1['weeknumber'] = sr_df1['weeknumber'].dt.strftime('%Y-%m-%d')


# In[68]:


db.close()


# In[69]:


veh_revenue=merged_df4[['groupcode','vehiclecode','stationcode','vehiclemodel','vehicletype','weeknumber',
                        'chargetotal_COMPLETE','chargetotal_DRIVE','chargetotal_RESERVE','countvehicle']]


# In[70]:


veh_revenue.rename(columns={'groupcode':'name'},inplace=True)


# In[71]:


st_revenue=sr_df1[['stationcode','weeknumber',
                  'chargetotal_COMPLETE','chargetotal_DRIVE','chargetotal_RESERVE','countvehicle']]


# # Connect with google sheet

# In[73]:


scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]


# In[74]:


cerds = ServiceAccountCredentials.from_json_keyfile_name("cerds.json", scope)


# In[75]:


client = gspread.authorize(cerds)


# In[76]:


sheet = client.open('weeklydashboarddata_01')


# In[77]:


sheet_1 = sheet.get_worksheet(0)


# In[78]:


#data = sheet_1.get_all_records()


# In[79]:


sheet_1.clear()


# In[80]:


sheet_2 = sheet.get_worksheet(1)


# In[81]:


sheet_2.clear()


# In[82]:


sheet_1.insert_rows([veh_revenue.columns.values.tolist()] + veh_revenue.values.tolist())


# In[83]:


sheet_2.insert_rows([st_revenue.columns.values.tolist()] + st_revenue.values.tolist())


# In[ ]:




