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


# In[5]:


user = input("Username: ")
passwd = input("Password: ")


# In[6]:


# Open database connection
db = pymysql.connect(host="devpartners.haupcar.com",
                     user=user,
                     passwd=passwd,
                     db="haupcar",
                     charset='utf8')


# In[7]:


# prepare a cursor object using cursor() method
cursor = db.cursor()


# In[8]:


q1 = '''SELECT r.reservationno, r.logtime, r.vehicleid ,r.receiptno, r.chargetotal, r.userid,
        r.reservehours, r.startkm, r.stopkm, r.groupid, r.actualhours, r.stationid, r.hourrate
        
        FROM reservation as r
        WHERE (r.logtime >= '2019-03-01') AND (r.logtime <= '2019-9-30' )
            AND r.receiptno != ''
        ORDER BY r.reservationno
        '''


# In[9]:


cursor.execute(q1)


# In[10]:


q1_result = cursor.fetchall()


# In[11]:


q1_field_names = [i[0] for i in cursor.description]
resv = pd.DataFrame(q1_result,columns =q1_field_names)


# In[13]:


resv['distance']=resv['stopkm']-resv['startkm']


# In[16]:


resv.to_csv('a.csv')


# In[ ]:




