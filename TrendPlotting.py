###########################
# TrendPlotting.py        #
#                         #
# Pietro Giampa, Jan 2022 #
###########################

## Libraries
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from GetCurrency import GetCurrencySingleDay
from GetCurrency import GetCurrencyOneYear
from GetCurrency import GetCurrencyPreviousWeek
from Variables import Bitcoin, Dogecoin, Cosmos, Shiba
from datetime import datetime

###########################
# DataFrame               #
#                         #
# 1. Open                 #
# 2. High                 #
# 3. Low                  #
# 4. Close                #
# 5. Adj Close            #
# 6. Volume               #
###########################

## Bitcoin, Degecoin, Cosmos, Shiba
select_crypto = input('Select Crypto Currency: \n 1) Bitcoin \n 2) Dogecoin \n 3) Cosmos \n 4) Shiba \n -->')
if select_crypto=='Bitcoin':
    crypto = Bitcoin
if select_crypto=='Dogecoin':
    crypto = Dogecoin
if select_crypto=='Cosmos':
    crypto = Cosmos
if select_crypto=='Shiba':
    crypto = Shiba

## Pull Data From Last Week and Last Year
DF_Year = GetCurrencyOneYear(crypto)
today = datetime.today()
DF_Week = GetCurrencyPreviousWeek(crypto, today.year, today.month, today.day)

## Plot Style
plt.style.use('dark_background')

## Plotting 1D Trends
fig, ax = plt.subplots(nrows=4, ncols=1, sharex=True)
ax[0].plot(DF_Year.index, DF_Year['Adj Close'], 'red')
ax[0].fill_between(DF_Year.index, DF_Year['Low'], DF_Year['High'], color='green', alpha=0.5)
ax[1].plot(DF_Year.index, DF_Year['Close']-DF_Year['Open'], 'blue')
ax[2].plot(DF_Year.index, DF_Year['High']-DF_Year['Low'], 'orange')
ax[3].plot(DF_Year.index, DF_Year['Volume'], 'pink')
plt.show()

## Plotting 2D Trends
fig1, ax1 = plt.subplots(nrows=1, ncols=3)
ax1[0].hexbin(DF_Year['Adj Close'], DF_Year['Volume'], bins='log', cmap='Oranges')
ax1[1].hexbin(DF_Year['Adj Close'], DF_Year['High']-DF_Year['Low'], bins='log', cmap='Oranges')
ax1[2].hexbin(DF_Year['Adj Close'], DF_Year['Close']-DF_Year['Open'], bins='log', cmap='Oranges')
plt.show()
