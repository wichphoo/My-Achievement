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


# In[4]:


from math import ceil
import calendar


# In[32]:


user = input("Username: ")
passwd = input("Password: ")


# In[33]:


# Open database connection
db = pymysql.connect(host="devpartners.haupcar.com",
                     user=user,
                     passwd=passwd,
                     db="haupcar",
                     charset='utf8')


# In[34]:


# prepare a cursor object using cursor() method
cursor = db.cursor()


# Get Service day & total day

# In[8]:


#Query service-days
q2 = '''SELECT l.logtime, l.vehiclestatus, l.stationid, l.stationcode, l.vehicleid, l.vehiclelcode
        
        
        FROM vehicle_station_log as l
        WHERE (l.logtime >= '2020-08-21') AND (l.logtime <= '2020-09-30')
        AND l.vehiclestatus = 'SERVICE'
        AND ((l.stationid = 501) OR (l.stationid = 503) OR (l.stationid = 505))
        ORDER BY l.logtime
        '''


# In[9]:


cursor.execute(q2)


# In[10]:


q2_result = cursor.fetchall()


# In[11]:


q2_field_names = [i[0] for i in cursor.description]
service_df = pd.DataFrame(q2_result,columns =q2_field_names)


# In[12]:


#Query service+MA days
q1 = '''SELECT l.logtime, l.vehiclestatus, l.stationid, l.stationcode, l.vehicleid, l.vehiclelcode
        
        
        FROM vehicle_station_log as l
        WHERE (l.logtime >= '2020-08-21') AND (l.logtime <= '2020-09-30')
        AND (l.vehiclestatus = 'SERVICE' OR l.vehiclestatus = 'MA')
        AND ((l.stationid = 501) OR (l.stationid = 503) OR (l.stationid = 505))
        ORDER BY l.logtime
        '''


# In[13]:


cursor.execute(q1)


# In[14]:


q1_result = cursor.fetchall()


# In[15]:


q1_field_names = [i[0] for i in cursor.description]
totalday_df = pd.DataFrame(q1_result,columns =q1_field_names)


# In[ ]:


#match station fail
#cause can't use groupid as key


# In[ ]:


#Query veh
#q3 = '''SELECT v.vehicleid, v.groupid,
#        s.groupid, s.stationid, s.stationcode 
        
        
#        FROM vehicle as v
#        LEFT JOIN station as s
#        ON v.groupid = s.groupid

#        WHERE s.stationid = '501' OR s.stationid = '503' OR s.stationid = '505'
#        ORDER BY s.stationid, v.vehicleid
#        '''


# In[ ]:


#cursor.execute(q3)


# In[ ]:


#q3_result = cursor.fetchall()


# In[ ]:


#q3_field_names = [i[0] for i in cursor.description]
#station_df = pd.DataFrame(q3_result,columns =q3_field_names)


# In[ ]:





# In[16]:


service_df['logtime'] = service_df['logtime'].dt.strftime('%Y-%m-%d')
totalday_df['logtime'] = totalday_df['logtime'].dt.strftime('%Y-%m-%d')


# In[17]:


service_df['logtime']=pd.to_datetime(service_df['logtime'])
totalday_df['logtime']=pd.to_datetime(totalday_df['logtime'])


# In[ ]:


#def week_of_month(tgtdate):

#    days_this_month = calendar.mdays[tgtdate.month]
#    for i in range(1, days_this_month):
#        d = dt.datetime(tgtdate.year, tgtdate.month, i)
#        if d.day - d.weekday() > 0:
#            startdate = d
#            break
    # now we canuse the modulo 7 appraoch
#    return (tgtdate - startdate).days //7 + 1


# In[ ]:


#service_df['weekofmonth'] = service_df['logtime'].apply(week_of_month)
#totalday_df['weekofmonth'] = totalday_df['logtime'].apply(week_of_month)


# In[ ]:


#service_df['weeknumber']=''
#totalday_df['weeknumber']=''


# In[ ]:


#for i in range(len(service_df)):
#    if service_df.loc[i, 'weekofmonth']==5:
#        service_df.loc[i, 'weekofmonth']=0
#    else:
#        pass


# In[ ]:


#for i in range(len(totalday_df)):
#    if totalday_df.loc[i, 'weekofmonth']==5:
#        totalday_df.loc[i, 'weekofmonth']=0
#    else:
#        pass


# In[ ]:


#weeknumber
#service_df['weeknumber'].loc[0]=0

#for i in range(len(service_df)):
#    w1=service_df.loc[i+1, 'weekofmonth']
#    w2=service_df.loc[i, 'weekofmonth']
#
#    if w1 == w2:
#        service_df.loc[i+1, 'weeknumber']=service_df.loc[i, 'weeknumber']
#        
#    else:
#        service_df.loc[i+1, 'weeknumber']=service_df.loc[i, 'weeknumber']+1


# In[ ]:


#weeknumber
#3totalday_df['weeknumber'].loc[0]=0

#for i in range(len(totalday_df)):

#    if totalday_df.loc[i+1, 'weekofmonth']==totalday_df.loc[i, 'weekofmonth']:
#        totalday_df.loc[i+1, 'weeknumber']=totalday_df.loc[i, 'weeknumber']
        
#    else:
#        totalday_df.loc[i+1, 'weeknumber']=totalday_df.loc[i, 'weeknumber']+1


# In[19]:


#service_df1 = service_df.pivot_table(index=['weeknumber','vehicleid','vehiclelcode'],  
#                           aggfunc='count')
#totalday_df1 = totalday_df.pivot_table(index=['weeknumber','vehicleid','vehiclelcode'],  
#                           aggfunc='count')
service_df1 = service_df.pivot_table(index=['vehicleid','vehiclelcode'],  
                           aggfunc='count')
totalday_df1 = totalday_df.pivot_table(index=['vehicleid','vehiclelcode'],  
                           aggfunc='count')


# In[20]:


#service_df1=service_df1.reset_index(level=['weeknumber','vehicleid','vehiclelcode'])
#totalday_df1=totalday_df1.reset_index(level=['weeknumber','vehicleid','vehiclelcode'])
service_df1=service_df1.reset_index(level=['vehicleid','vehiclelcode'])
totalday_df1=totalday_df1.reset_index(level=['vehicleid','vehiclelcode'])


# In[21]:


service_df1.rename(columns={'vehiclestatus':'service_days'},inplace=True)
totalday_df1.rename(columns={'vehiclestatus':'total_days'},inplace=True)


# In[22]:


#day_df = totalday_df1.merge(service_df1, on = ['weeknumber','vehicleid','vehiclelcode'], how = 'left')
day_df = totalday_df1.merge(service_df1, on = ['vehicleid','vehiclelcode'], how = 'left')


# In[23]:


del day_df['stationcode_x']
del day_df['stationid_x']
del day_df['stationcode_y']
del day_df['stationid_y']
del day_df['logtime_y']
del day_df['logtime_x']
#del day_df['weekofmonth_x']
#del day_df['weekofmonth_y']


# In[24]:


day_df


# In[41]:


#Query resv
q4 = '''SELECT r.reservationno, r.logtime, r.vehicleid ,r.receiptno, r.userid, r.groupid,
        r.reservehours, r.startkm, r.stopkm, r.stationid, r.totalprice, r.reservationstate
        
        FROM reservation as r
        WHERE (r.logtime >= '2020-08-24') AND (r.logtime <= '2020-09-30' )
            AND (r.groupid=8 OR r.groupid=213)
            AND (r.vehicleid=623 OR r.vehicleid=612 OR r.vehicleid=628 OR r.vehicleid=642 
            OR r.vehicleid=648 OR r.vehicleid=649)
        ORDER BY r.reservationno
        '''


# In[42]:


cursor.execute(q4)


# In[43]:


q4_result = cursor.fetchall()


# In[44]:


q4_field_names = [i[0] for i in cursor.description]
resv_df = pd.DataFrame(q4_result,columns =q4_field_names)


# In[53]:


db.close()


# In[48]:


resv_df


# In[49]:


#remove admin
resv_df1 = resv_df[(resv_df['userid']!=3888)&(resv_df['userid']!=164173)&(resv_df['userid']!=199001)]


# In[51]:


resv_df1.to_csv('pcx_resv.csv')


# In[ ]:


countresv=len(resv_df)


# In[ ]:


resv_df['usertype']=''


# In[ ]:


resv_df['usertype'] = np.where(resv_df['groupid']==8, 'Student', resv_df['usertype'])
resv_df['usertype'] = np.where(resv_df['groupid']==213, 'Staff', resv_df['usertype'])


# In[ ]:


resv_df['drivingdistance']=resv_df['stopkm']-resv_df['startkm']


# In[ ]:


#resv_df['logtime'] = resv_df['logtime'].dt.strftime('%Y-%m-%d')


# In[ ]:


del resv_df['startkm']
del resv_df['stopkm']
del resv_df['reservationno']
del resv_df['receiptno']


# In[ ]:


resv_df1 = resv_df.pivot_table(index=['userid'],  
                           aggfunc='count')


# In[ ]:


repeatuser=resv_df1[resv_df1['logtime']>3]


# In[ ]:


firsttimeuser=resv_df1[resv_df1['logtime']==1]


# In[ ]:


countfisttimeuser=len(firsttimeuser)


# In[ ]:


countrepeatuser=len(repeatuser)


# In[ ]:


countuser=resv_df['userid'].nunique()


# In[ ]:


#resv_df['logtime']=pd.to_datetime(resv_df['logtime'])


# In[ ]:


#resv_df['weekofmonth'] = resv_df['logtime'].apply(week_of_month)


# In[ ]:


#resv_df['weeknumber']=''


# In[ ]:


#for i in range(len(resv_df)):
#    if resv_df.loc[i, 'weekofmonth']==5:
#        resv_df.loc[i, 'weekofmonth']=0
#    else:
#        pass


# In[ ]:


#weeknumber
#resv_df['weeknumber'].loc[0]=1

#for i in range(len(resv_df)):
#    w1=resv_df.loc[i+1, 'weekofmonth']
#    w2=resv_df.loc[i, 'weekofmonth']

#    if w1 == w2:
#        resv_df.loc[i+1, 'weeknumber']=resv_df.loc[i, 'weeknumber']
        
#    else:
#        resv_df.loc[i+1, 'weeknumber']=resv_df.loc[i, 'weeknumber']+1


# In[ ]:


resv_df2=resv_df[resv_df['drivingdistance']>0]


# In[ ]:


allresvhour = resv_df['reservehours'].mean()


# In[ ]:


alldistance = resv_df2['drivingdistance'].mean()


# In[ ]:


#perweek1 = resv_df.pivot_table(index=['weeknumber'],aggfunc='mean')


# In[ ]:


#perweek2 = resv_df2.pivot_table(index=['weeknumber'],aggfunc='mean')


# In[ ]:


#perweek1 = perweek1.reset_index(level=['weeknumber'])
#perweek2 = perweek2.reset_index(level=['weeknumber'])


# In[ ]:


#perweek1 = perweek1[['weeknumber','reservehours']]
#perweek2 = perweek2[['weeknumber','drivingdistance']]


# In[ ]:


#perweek=perweek1.merge(perweek2, on='weeknumber', how='outer')


# In[ ]:


#perweek


# In[ ]:


print("number of reservations = {}\nnumber of registered users = {}\nnumber of first time users = {}\nnumber of repeated users = {}\naverage reserved hours (hr) = {:.2f}\naverage driving distance (km) = {:.2f}".format(countresv,countuser,countfisttimeuser,countrepeatuser,allresvhour,alldistance))


# In[ ]:


resv_df.to_csv('resv_20200924.csv')


# In[ ]:




