#!/usr/bin/env python
# coding: utf-8

# # Linear Regression Slope (LRS)

# https://library.tradingtechnologies.com/trade/chrt-ti-linear-regression-slope.html

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings("ignore")


import yfinance as yf
yf.pdr_override()


# In[2]:


# input
symbol1 = 'AAPL'
symbol2 = 'QQQ'
start = '2018-08-01'
end = '2019-01-01'

# Read data 
df1 = yf.download(symbol1,start,end)
df2 = yf.download(symbol2,start,end)


# In[3]:


# View Columns
df1.head()


# In[4]:


df2.head()


# In[5]:


avg1 = df1['Adj Close'].mean()
avg2 = df2['Adj Close'].mean()
df1['AVGS1_S1'] = avg1 - df1['Adj Close']
df1['AVGS2_S2'] = avg2 - df2['Adj Close']
df1['Average_SQ'] = df1['AVGS1_S1']**2
df1['AVG_AVG'] = df1['AVGS1_S1']*df1['AVGS2_S2']


# In[6]:


sum_sq = df1['Average_SQ'].sum()
sum_avg = df1['AVG_AVG'].sum()
slope = sum_avg/sum_sq
intercept = avg2-(slope*avg1)


# In[7]:


m = (df1['Adj Close']-df1['Adj Close'].mean())*(df2['Adj Close']-df2['Adj Close'].mean())/(df1['Adj Close']-df1['Adj Close'].mean())


# In[8]:


n = 20
df1['Slope'] = m.rolling(n).mean()


# In[9]:


fig = plt.figure(figsize=(14,7))
ax1 = plt.subplot(2, 1, 1)
ax1.plot(df1['Adj Close'])
ax1.set_title('Stock '+ symbol1 +' Closing Price')
ax1.set_ylabel('Price')
ax1.legend(loc='best')

ax2 = plt.subplot(2, 1, 2)
#df1['VolumePositive'] = df1['Open'] < df1['Adj Close']
#colors = df1.VolumePositive.map({True: 'g', False: 'r'})
#ax2.bar(df1.index, df1['Volume'], color=colors, alpha=0.4)
ax2.plot(df1['Slope'], label='Slope')
ax2.grid()
ax2.set_ylabel('Slope')
ax2.set_xlabel('Date')


# ## Candlestick with Linear Regression Slope

# In[10]:


from matplotlib import dates as mdates
import datetime as dt

dfc = df1.copy()
dfc['VolumePositive'] = dfc['Open'] < dfc['Adj Close']
#dfc = dfc.dropna()
dfc = dfc.reset_index()
dfc['Date'] = mdates.date2num(dfc['Date'].astype(dt.date))
dfc.head()


# In[11]:


from mplfinance.original_flavor import candlestick_ohlc

fig = plt.figure(figsize=(14,7))
ax1 = plt.subplot(2, 1, 1)
candlestick_ohlc(ax1,dfc.values, width=0.5, colorup='g', colordown='r', alpha=1.0)
ax1.xaxis_date()
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
ax1.grid(True, which='both')
ax1.minorticks_on()
ax1v = ax1.twinx()
colors = dfc.VolumePositive.map({True: 'g', False: 'r'})
ax1v.bar(dfc.Date, dfc['Volume'], color=colors, alpha=0.4)
ax1v.axes.yaxis.set_ticklabels([])
ax1v.set_ylim(0, 3*df1.Volume.max())
ax1.set_title('Stock '+ symbol1 +' Closing Price')
ax1.set_ylabel('Price')

ax2 = plt.subplot(2, 1, 2)
#df1['VolumePositive'] = df1['Open'] < df1['Adj Close']
#colors = df1.VolumePositive.map({True: 'g', False: 'r'})
#ax2.bar(df1.index, df1['Volume'], color=colors, alpha=0.4)
ax2.plot(df1['Slope'], label='Slope')
ax2.grid()
ax2.set_ylabel('Slope')
ax2.set_xlabel('Date')

