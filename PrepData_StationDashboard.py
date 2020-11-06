#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import os


# In[2]:


import pymysql
import pymysql.cursors


# In[3]:


import datetime as dt
import math


# # Get Data

# In[4]:


user = input("Username: ")
passwd = input("Password: ")


# In[8]:


# Open database connection
db = pymysql.connect(host="devpartners.haupcar.com",
                     user=user,
                     passwd=passwd,
                     db="haupcar",
                     charset='utf8')


# In[9]:


# prepare a cursor object using cursor() method
cursor = db.cursor()


# Get station table

# In[10]:


#get station table
q1 = '''SELECT s.stationid, s.stationcode
    FROM `station` as s
    '''


# In[11]:


cursor.execute(q1)


# In[12]:


q1_result = cursor.fetchall()


# In[13]:


q1_field_names = [i[0] for i in cursor.description]
station_df = pd.DataFrame(q1_result, columns =q1_field_names)


# Get service day

# In[14]:


#Query service-days
q2 = '''SELECT l.logtime, l.vehiclestatus, l.stationid, l.stationcode 
        
        
        FROM vehicle_station_log as l
        WHERE (l.logtime >= '2019-06-01') AND (l.logtime <= '2019-12-31')
            AND l.vehiclestatus = 'SERVICE'
        ORDER BY l.logtime
        '''


# In[15]:


cursor.execute(q2)


# In[16]:


q2_result = cursor.fetchall()


# In[17]:


q2_field_names = [i[0] for i in cursor.description]
service_df = pd.DataFrame(q2_result,columns =q2_field_names)


# In[18]:


#service_df['logtime'] = service_df['logtime'].dt.strftime('%Y-%m-%d')
service_df['logtime'] = service_df['logtime'].dt.strftime('%Y-%m')


# In[19]:


service_df1 = service_df.pivot_table(index=['stationid', 'stationcode', 'logtime'],  
                           aggfunc='count')


# In[20]:


service_df1=service_df1.reset_index(level=['stationid','stationcode', 'logtime'])


# In[21]:


service_df1.rename(columns={'vehiclestatus':'service_days'},inplace=True)


# Get service+ma days

# In[22]:


q4 = '''SELECT l.logtime, l.vehiclestatus, l.stationid, l.stationcode 
        
        
        FROM vehicle_station_log as l
        WHERE (l.logtime >= '2019-06-01') AND (l.logtime <= '2019-12-31' )
            AND (l.vehiclestatus = 'SERVICE' OR l.vehiclestatus = 'MA')
        ORDER BY l.logtime
        '''


# In[23]:


cursor.execute(q4)


# In[24]:


q4_result = cursor.fetchall()


# In[25]:


q4_field_names = [i[0] for i in cursor.description]
service_ma_df = pd.DataFrame(q4_result,columns =q4_field_names)


# In[26]:


service_ma_df['logtime'] = service_ma_df['logtime'].dt.strftime('%Y-%m')


# In[27]:


service_ma_df1 = service_ma_df.pivot_table(index=['stationid', 'stationcode', 'logtime'],  
                           aggfunc='count')


# In[28]:


service_ma_df1=service_ma_df1.reset_index(level=['stationid','stationcode', 'logtime'])


# In[29]:


service_ma_df1.rename(columns={'vehiclestatus':'total_days'},inplace=True)


# Merge service & service+MA

# In[30]:


day_df = service_ma_df1.merge(service_df1, on = ['stationid','stationcode','logtime'], how = 'left')


# In[31]:


day_df['service_days'] = np.where(day_df['service_days'].isnull(),
                                0, day_df['service_days'])


# Get resv table

# In[32]:


#Query revenue from resv
q3 = '''SELECT r.reservationno, r.logtime, r.vehicleid ,r.receiptno, r.chargetotal, r.userid,
        r.reservehours, r.startkm, r.stopkm, r.groupid, r.actualhours, r.stationid, r.hourrate
        
        FROM reservation as r
        WHERE (r.logtime >= '2019-06-01') AND (r.logtime <= '2019-12-31' )
            AND r.receiptno != ''
        ORDER BY r.reservationno
        '''


# In[33]:


cursor.execute(q3)


# In[34]:


q3_result = cursor.fetchall()


# In[35]:


q3_field_names = [i[0] for i in cursor.description]
resv_df = pd.DataFrame(q3_result,columns =q3_field_names)


# Get usertype

# In[36]:


q4 = '''SELECT g.groupid, g.selectable_usertype
    FROM `group` as g
    '''


# In[37]:


cursor.execute(q4)


# In[38]:


q4_result = cursor.fetchall()


# In[39]:


q4_field_names = [i[0] for i in cursor.description]
group_df = pd.DataFrame(q4_result, columns =q4_field_names)


# In[40]:


group_df.rename(columns={'selectable_usertype':'usertype'},inplace=True)


# In[41]:


group_df['stutype'] = np.where((group_df['usertype']=='STUDENT') | (group_df['usertype']=='STUDENT_PIN'),
                                1,
                                group_df['usertype'])


# In[42]:


group_df['stutype'] = np.where((group_df['stutype']!=1),
                                0,
                                group_df['stutype'])


# Merge resv table with usertype

# In[43]:


resv_df1 = resv_df.merge(group_df, on = 'groupid', how = 'left')


# In[44]:


del resv_df1['receiptno']


# In[45]:


resv_df1['logtime'] = resv_df1['logtime'].dt.strftime('%Y-%m')


# In[46]:


resv_df1['drivingdistance']=resv_df1['stopkm']-resv_df1['startkm']


# In[47]:


index_km_error = resv_df1[resv_df1['drivingdistance']<0].index


# In[48]:


resv_df1.drop(index_km_error, inplace=True)


# In[49]:


del resv_df1['startkm']
del resv_df1['stopkm']
del resv_df1['usertype']


# In[50]:


del resv_df1['chargetotal']


# Get charge information with resv

# In[51]:


q5 = '''SELECT c.reservationno, c.chargetotal
    FROM `charge` as c
    
    WHERE (c.chargetime >= '2019-06-01') AND (c.chargetime <= '2019-12-31' )
    AND c.reservationno != ''
    AND c.chargemethod = 'OMISE'
    AND c.chargestate = 'CHARGED'
    ORDER BY c.reservationno
    '''


# In[52]:


cursor.execute(q5)


# In[53]:


q5_result = cursor.fetchall()


# In[54]:


q5_field_names = [i[0] for i in cursor.description]
charge_df = pd.DataFrame(q5_result, columns =q5_field_names)


# In[55]:


charge_df = charge_df.pivot_table(index=['reservationno'], 
                           aggfunc='sum')


# In[56]:


charge_df = charge_df.reset_index(level=['reservationno'])


# In[57]:


resv_df1 = resv_df1.merge(charge_df, on = ['reservationno'], how = 'left')


# In[58]:


index_nocharge = resv_df1[resv_df1['chargetotal'].isnull()].index


# In[59]:


resv_df1.drop(index_nocharge, inplace=True)


# In[60]:


# disconnect from server
db.close()


# # Creat Factors

# In[61]:


resv_df1['daily']=''


# In[62]:


resv_df1['daily'] = np.where(resv_df1['reservehours']>=8,
                                1, resv_df1['daily'])


# In[63]:


resv_df1['daily'] = np.where(resv_df1['daily']!=1,
                                0, resv_df1['daily'])


# In[64]:


resv_df1['stutype']=pd.to_numeric(resv_df1['stutype'], errors='coerce')
resv_df1['daily']=pd.to_numeric(resv_df1['daily'], errors='coerce')


# In[65]:


countuser1=resv_df1.pivot_table(index=['stationid','userid', 'logtime'], 
                           aggfunc='sum')


# In[66]:


countuser1=countuser1.reset_index(level=['stationid','userid','logtime'])


# In[67]:


countuser1['stutype'] = np.where(countuser1['stutype']>1, 1, countuser1['stutype'])


# In[68]:


countuser2=countuser1.pivot_table(index=['stationid', 'logtime'], 
                           aggfunc='sum')


# In[69]:


countuser2=countuser2.reset_index(level=['stationid','logtime'])


# In[70]:


countuser3=countuser2[['stationid','logtime','stutype']]


# In[71]:


countusertotal1=resv_df1.pivot_table(index=['stationid', 'logtime'], 
                           aggfunc='count')


# In[72]:


countusertotal1=countusertotal1.reset_index(level=['stationid','logtime'])


# In[73]:


countuser4=countuser3.merge(countusertotal1, on = ['stationid','logtime'], how = 'left')


# In[74]:


countuser4['%student_user']=countuser4['stutype_x']/countuser4['stutype_y']


# In[75]:


countuser5=countuser4[['stationid','logtime','%student_user']]


# In[76]:


sumresv_df = resv_df1.pivot_table(index=['stationid', 'logtime'], 
                           aggfunc='sum')


# In[77]:


sumresv_df = sumresv_df.reset_index(level=['stationid','logtime'])


# In[78]:


sumresv_df = sumresv_df[['stationid', 'logtime','reservehours', 'chargetotal', 'drivingdistance', 'stutype', 'daily','hourrate']]


# In[79]:


df2 = day_df.merge(sumresv_df, on = ['stationid', 'logtime'], how = 'left')


# In[80]:


df2['%UT'] = df2['reservehours']/(df2['service_days']*24)


# In[81]:


df2['%UT'] = np.where(df2['%UT']>1, 1, df2['%UT'])


# In[82]:


df2['%AV'] = df2['service_days']/df2['total_days']


# In[83]:


df2.rename(columns={'stutype':'countstu'},inplace=True)
df2.rename(columns={'daily':'countdaily'},inplace=True)


# In[84]:


countresv_df = resv_df1.pivot_table(index=['stationid', 'logtime'], 
                           aggfunc='count')


# In[85]:


countresv_df = countresv_df.reset_index(level=['stationid','logtime'])


# In[86]:


countresv_df = countresv_df[['stationid', 'logtime', 'stutype', 'daily', 'reservationno']]


# In[87]:


df3 = df2.merge(countresv_df, on = ['stationid', 'logtime'], how = 'left')


# In[88]:


df3.rename(columns={'reservationno':'countresv'},inplace=True)


# In[89]:


df3['%student_trip']=df3['countstu']/df3['stutype']
df3['%daily']=df3['countdaily']/df3['daily']


# In[90]:


del df3['countstu']
del df3['stutype']
del df3['countdaily']
del df3['daily']


# In[91]:


unique_df = resv_df1.pivot_table(index=['stationid', 'logtime'], 
                           aggfunc=lambda resv_df1: len(resv_df1.unique()))


# In[92]:


unique_df = unique_df.reset_index(level=['stationid','logtime'])


# In[93]:


unique_df = unique_df[['stationid', 'logtime', 'userid']]


# In[94]:


df4 = df3.merge(unique_df, on = ['stationid', 'logtime'], how = 'left')


# In[95]:


df4['totalveh']=df4['total_days']/30
df4['serviceveh']=df4['service_days']/30


# In[96]:


for i in range(len(df4)):
    df4.loc[i, 'totalveh']=math.ceil(df4.loc[i, 'totalveh'])
    df4.loc[i, 'serviceveh']=math.ceil(df4.loc[i, 'serviceveh'])


# In[97]:


df4.rename(columns={'userid':'uniqueuser'},inplace=True)


# In[98]:


df4['revenue/serviceveh']=df4['chargetotal']/df4['serviceveh']
df4['countresv/veh']=df4['countresv']/df4['totalveh']
df4['drivingdistance/veh']=df4['drivingdistance']/df4['totalveh']
df4['reservehours/veh']=df4['reservehours']/df4['totalveh']
df4['spending/uniqueuser']=df4['chargetotal']/df4['uniqueuser']
df4['modelrate/resv']=df4['hourrate']/df4['countresv']


# In[99]:


index_nodata = df4[df4['reservehours'].isnull()].index


# In[100]:


df4.drop(index_nodata, inplace=True)


# In[101]:


result_df = df4[['stationid','stationcode','logtime','%UT','%AV','%student_trip','%daily','revenue/serviceveh',
          'drivingdistance/veh','reservehours/veh','countresv/veh','uniqueuser','modelrate/resv','spending/uniqueuser']]


# In[102]:


resv_df1['countresv']=1


# In[103]:


reuser_df = resv_df1.pivot_table(index=['stationid', 'logtime','userid'], 
                           aggfunc='sum')


# In[104]:


reuser_df = reuser_df.reset_index(level=['stationid','logtime','userid'])


# In[105]:


reuser_df = reuser_df[['stationid','userid','logtime','countresv']]


# In[106]:


reuser_df = reuser_df.sort_values(by=['stationid', 'userid'])


# In[107]:


reuser_df=reuser_df.reset_index(drop=True)


# In[108]:


reuser_df1 = reuser_df.pivot_table(index=['stationid', 'userid'], 
                           aggfunc='sum')


# In[109]:


reuser_df1 = reuser_df1.reset_index(level=['stationid','userid'])


# In[110]:


index_repeat = reuser_df1[reuser_df1['countresv']<=3].index


# In[111]:


reuser_df1.drop(index_repeat, inplace=True)


# In[112]:


countreuser_df = reuser_df1.pivot_table(index=['stationid'], 
                           aggfunc='count')


# In[113]:


countreuser_df = countreuser_df.reset_index(level=['stationid'])


# In[114]:


countreuser_df['repeatuser']=countreuser_df['userid']


# In[115]:


del countreuser_df['countresv']
del countreuser_df['userid']


# In[116]:


result_df = result_df.merge(countreuser_df, on = ['stationid'], how = 'left')


# In[117]:


result_df['repeatuser'] = np.where(result_df['repeatuser'].isnull(),
                                0, result_df['repeatuser'])


# In[118]:


result_df1 = result_df.merge(countuser5, on = ['stationid','logtime'], how = 'left')


# In[119]:


result_df2 = result_df1.pivot_table(index=['stationid','stationcode'], 
                           aggfunc='mean')


# In[ ]:





# In[120]:


result_df2.to_csv('oldhealtcheckdata_20200917.csv', index=True)


# In[ ]:





# In[ ]:




