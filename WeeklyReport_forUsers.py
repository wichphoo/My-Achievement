#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import filedialog
from tkinter import *


# In[2]:


#Import Complete All Resv
root= tk.Tk()
canvas1 = tk.Canvas(root, width = 300, height = 160, bg = 'lightsteelblue2', relief = 'raised')
canvas1.pack()
def getCSV ():
    global df   
    import_file_path = filedialog.askopenfilename()
    df = pd.read_csv (import_file_path)
    print ('import complete_resv successfull')  
browseButton_CSV = tk.Button(text="Import Complete All Resv\n(.csv)", command=getCSV, bg='white', fg='black', font=('helvetica', 15, 'bold'))
canvas1.create_window(150, 80, window=browseButton_CSV)
quitbutton = tk.Button(text = "Next", command = root.destroy)
quitbutton.pack()
root.title('Weekly_V1')
root.mainloop()


# In[3]:


del df['email']


# In[4]:


index1 = df[ df['Promo'] == 'HFCOVID'].index
index2 = df[ df['Promo'] == 'hfcovid'].index


# In[5]:


df.drop(index1, inplace=True)


# In[6]:


df.drop(index2, inplace=True)


# In[7]:


df.loc[((df.Others<1) & (df.Others>-1)), 'Others'] = 0


# In[8]:


df.rename(columns={'Discount (THB)':'Discount'},inplace=True)
df.rename(columns={'Revenues (THB)':'Revenues'},inplace=True)
df.rename(columns={'Distance Price 1':'DistancePrice1'},inplace=True)
df.rename(columns={'Distance Price 2':'DistancePrice2'},inplace=True)


# In[9]:


df=df[['Fleet Owner','Rsv. State','Rsv. No','userid','Vehicle Code','License Number','Station Code','Log Time','Reserve Start TIme','Reserve Stop Time','Receipt Date','User Type','Receipt No','Hour Rate','Day Rate','Total Usage (hr)','Hour Price','DistancePrice1','DistancePrice2','Promo','Discount','Others','Revenues','remark']]


# In[10]:


df['remark']=df['remark'].fillna('')


# In[11]:


searchfor = ['Free','free','ฟรี','PHTRforMED']


# In[12]:


#index3=df[(df['remark'].str.contains('|'.join(searchfor))) & (df.Revenues==0)].index
index3=df[(df['remark'].str.contains('|'.join(searchfor)))].index


# In[13]:


df.drop(index3, inplace=True)


# In[14]:


index4=df[(df.Promo.notna()) & (df.Discount==0)].index


# In[15]:


df.drop(index4, inplace=True)


# In[16]:


index5=df[(df.Discount!=0) & (df.Promo.isnull())].index


# In[17]:


df.drop(index5, inplace=True)


# In[18]:


index6=df[df.Revenues==0].index


# In[19]:


df.drop(index6, inplace=True)


# In[20]:


index7=df[df.DistancePrice1==0].index


# In[21]:


df.drop(index7, inplace=True)


# In[22]:


index8=df[(df.Others>1000) | (df.Others<-1000)].index


# In[23]:


df.drop(index8, inplace=True)


# In[24]:


#dfx1=df[(df.Promo.notna()) & (df.Discount==0)]


# In[25]:


#dfx2=df[(df.Discount!=0) & (df.Promo.isnull())]


# In[26]:


#dfx3=df[df.Revenues==0]


# In[27]:


#dfx4=df[df.DistancePrice1==0]


# In[28]:


#dfx5=df[(df.Others>1000) | (df.Others<-1000)]


# In[29]:


#df2 = pd.concat([dfx1,dfx2,dfx3,dfx4,dfx5], axis=0).drop_duplicates()


# In[30]:


#df2.sort_values(by=['Rsv. No'], inplace=True)


# In[31]:


#export new file for manual check
#root= tk.Tk()
#canvas1 = tk.Canvas(root, width = 300, height = 160, bg = 'lightsteelblue2', relief = 'raised')
#canvas1.pack()
#def exportCSV ():
#    global df2
#    export_file_path2 = filedialog.asksaveasfilename(defaultextension='.csv')
#    df2.to_csv (export_file_path2, index = False, header=True)
#saveAsButton_CSV = tk.Button(text='Export a new file\nfor Manualcheck', command=exportCSV, bg='white', fg='black', font=('helvetica', 15, 'bold'))
#canvas1.create_window(150, 80, window=saveAsButton_CSV)
#quitbutton = tk.Button(text = "Next", command = root.destroy)
#quitbutton.pack()
#root.title('Weekly_V1')
#root.mainloop()


# In[32]:


#import manual check done
#root= tk.Tk()
#canvas1 = tk.Canvas(root, width = 300, height = 160, bg = 'lightsteelblue2', relief = 'raised')
#canvas1.pack()
#def getCSV ():
#    global newdf2   
#    import_file_path2 = filedialog.askopenfilename()
#    newdf2 = pd.read_csv (import_file_path2)
#    print ('import manualcheck file successfull') 
#browseButton_CSV = tk.Button(text="Import Checked\nfile (.csv)", command=getCSV, bg='white', fg='black', font=('helvetica', 15, 'bold'))
#canvas1.create_window(150, 80, window=browseButton_CSV)
#quitbutton = tk.Button(text = "Next", command = root.destroy)
#quitbutton.pack()
#root.title('Weekly_V1')
#root.mainloop()


# In[33]:


#df1=pd.concat([df, df2, df2]).drop_duplicates(keep=False)


# In[34]:


#newdf = pd.concat([df1,newdf2], axis=0).drop_duplicates()


# In[35]:


newdf = df


# In[36]:


del newdf['remark']


# In[37]:


df_comp=newdf[['Fleet Owner','Rsv. State','Rsv. No','userid','Vehicle Code','License Number','Station Code','Log Time','Reserve Start TIme','Reserve Stop Time','Receipt Date','User Type','Receipt No','Hour Rate','Day Rate','Total Usage (hr)','Hour Price','DistancePrice1','DistancePrice2','Promo','Discount','Others','Revenues']]


# In[38]:


#del newdf['Fleet Owner']
del newdf['Rsv. State']
del newdf['Rsv. No']
del newdf['userid']
del newdf['License Number']
del newdf['Station Code']
del newdf['Log Time']
del newdf['Reserve Start TIme']
del newdf['Reserve Stop Time']
del newdf['Receipt Date']
del newdf['User Type']
del newdf['Receipt No']
del newdf['Hour Rate']
del newdf['Day Rate']
del newdf['Promo']


# In[39]:


newdf['Hour Price']=pd.to_numeric(newdf['Hour Price'], errors='coerce')
newdf['Total Usage (hr)']=pd.to_numeric(newdf['Total Usage (hr)'], errors='coerce')
newdf['DistancePrice1']=pd.to_numeric(newdf['DistancePrice1'], errors='coerce')
newdf['DistancePrice2']=pd.to_numeric(newdf['DistancePrice2'], errors='coerce')
newdf['Discount']=pd.to_numeric(newdf['Discount'], errors='coerce')
newdf['Others']=pd.to_numeric(newdf['Others'], errors='coerce')
newdf['Revenues']=pd.to_numeric(newdf['Revenues'], errors='coerce')


# In[40]:


#Import All State
root= tk.Tk()
canvas1 = tk.Canvas(root, width = 300, height = 160, bg = 'lightsteelblue2', relief = 'raised')
canvas1.pack()
def getCSV ():
    global df_all   
    import_file_path = filedialog.askopenfilename()
    df_all = pd.read_csv (import_file_path)
    print ('import all state successfull')  
browseButton_CSV = tk.Button(text="Import All State Resv\n(.csv)", command=getCSV, bg='white', fg='black', font=('helvetica', 15, 'bold'))
canvas1.create_window(150, 80, window=browseButton_CSV)
quitbutton = tk.Button(text = "Next", command = root.destroy)
quitbutton.pack()
root.title('Weekly_V1')
root.mainloop()


# In[41]:


df_all=df_all[['Fleet Owner','Rsv. State','Rsv. No','userid','Vehicle Code',
               'License Number','Station Code','Log Time','Reserve Start Time',
               'Reserve Stop Time','User Type','Hour Rate',
               'Day Rate','Total Usage (hr)','Hour Price','Distance Price 1','Distance Price 2','Promo',
               'Discount (THB)','Others','Revenues (THB)']]


# In[42]:


df_all.loc[((df_all.Others<1) & (df_all.Others>-1)), 'Others'] = 0


# In[43]:


newdf=newdf.groupby(['Vehicle Code']).sum().reset_index()


# In[44]:


#import vehicle_summary
root= tk.Tk()
canvas1 = tk.Canvas(root, width = 300, height = 160, bg = 'lightsteelblue2', relief = 'raised')
canvas1.pack()
def getCSV ():
    global veh_sum   
    import_file_path3 = filedialog.askopenfilename()
    veh_sum = pd.read_csv (import_file_path3)
    print ('import vehicle_summary successfull')  
browseButton_CSV = tk.Button(text="Import vehicle_summary file\n(.csv)", command=getCSV, bg='white', fg='black', font=('helvetica', 15, 'bold'))
canvas1.create_window(150, 80, window=browseButton_CSV)
quitbutton = tk.Button(text = "Next", command = root.destroy)
quitbutton.pack()
root.title('Weekly_V1')
root.mainloop()


# In[45]:


#sumcost=newdf.merge(veh_sum, on='Vehicle Code', how='outer')
sumcost=veh_sum.merge(newdf, on='Vehicle Code', how='outer')


# In[46]:


del sumcost['Total Usage (hr)_x']
del sumcost['Hour Price (THB)']
del sumcost['Distance Price 1 (THB)']
del sumcost['Discount Price 2 (THB)']
del sumcost['Discount (THB)']
del sumcost['Others (THB)']
del sumcost['Revenues']
del sumcost['Revenue (THB)']


# In[47]:


sumcost.rename(columns={'Total Usage (hr)_y':'Total Usage (hr)'},inplace=True)
sumcost.rename(columns={'Hour Price':'Hour Price (THB)'},inplace=True)
sumcost.rename(columns={'DistancePrice1':'Distance Price 1 (THB)'},inplace=True)
sumcost.rename(columns={'DistancePrice2':'Discount Price 2 (THB)'},inplace=True)
sumcost.rename(columns={'Discount':'Discount (THB)'},inplace=True)
sumcost.rename(columns={'Others':'Others (THB)'},inplace=True)
#sumcost.rename(columns={'Revenues':'Revenue (THB)'},inplace=True)


# In[48]:


sumcost['Revenue (THB)'] = (sumcost['Hour Price (THB)']+sumcost['Distance Price 1 (THB)']
                            +sumcost['Discount Price 2 (THB)']-sumcost['Discount (THB)']
                            +sumcost['Others (THB)'])


# In[49]:


sumcost = sumcost.fillna(0)


# In[50]:


sumcost['Total Usage (hr)'] = np.where(sumcost['Total Distance (km)'] == 0, 0, sumcost['Total Usage (hr)'])
sumcost['Hour Price (THB)'] = np.where(sumcost['Total Distance (km)'] == 0, 0, sumcost['Hour Price (THB)'])
sumcost['Distance Price 1 (THB)'] = np.where(sumcost['Total Distance (km)'] == 0, 0, sumcost['Distance Price 1 (THB)'])
sumcost['Discount Price 2 (THB)'] = np.where(sumcost['Total Distance (km)'] == 0, 0, sumcost['Discount Price 2 (THB)'])
sumcost['Discount (THB)'] = np.where(sumcost['Total Distance (km)'] == 0, 0, sumcost['Discount (THB)'])
sumcost['Others (THB)'] = np.where(sumcost['Total Distance (km)'] == 0, 0, sumcost['Others (THB)'])
sumcost['Revenue (THB)'] = np.where(sumcost['Total Distance (km)'] == 0, 0, sumcost['Revenue (THB)'])


# In[51]:


sumcost=sumcost[['fleetowner','Vehicle Code','License Number','Service Days','MA Days','Total Usage (hr)','Total Distance (km)','Hour Price (THB)','Distance Price 1 (THB)','Discount Price 2 (THB)','Discount (THB)','Others (THB)','Revenue (THB)']]


# In[52]:


sumcost.sort_values(by=['fleetowner','Vehicle Code'], inplace=True)


# In[53]:


#export excel
writer = pd.ExcelWriter('weekly_20201004.xlsx', engine='xlsxwriter')


# In[54]:


sumcost.to_excel(writer, sheet_name='VehSum', index = False)


# In[55]:


df_comp.to_excel(writer, sheet_name='Complete', index = False)


# In[56]:


df_all.to_excel(writer, sheet_name='AllState', index = False)


# In[57]:


writer.save()


# In[ ]:




