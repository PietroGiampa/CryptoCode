###########################
# TrendPlotting.py        #
#                         #
# Pietro Giampa, Jan 2022 #
###########################

## Libraries
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import GetCurrency as gc
import Variables as currency
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

## Select Crypto Currency
select_crypto = input('Select Crypto Currency: ')
crypto = currency.GetCurrencyTag(select_crypto)

## Pull Data From Last Week and Last Year
DF_Year = gc.GetCurrencyOneYear(crypto)
today = datetime.today()
DF_Week = gc.GetCurrencyPreviousWeek(crypto, today.year, today.month, today.day)

## Plot Style
plt.style.use('dark_background')

## Plotting 1D Trends
fig, ax = plt.subplots(nrows=4, ncols=1, sharex=True)
ax[0].plot(DF_Year.index, DF_Year['Adj Close'], 'red')
ax[0].fill_between(DF_Year.index, DF_Year['Low'], DF_Year['High'], color='green', alpha=0.5)
ax[0].set_ylabel('Adj Close')
ax[0].grid(True)
ax[1].plot(DF_Year.index, DF_Year['Close']-DF_Year['Open'], 'blue')
ax[1].set_ylabel('Close-Open')
ax[1].grid(True)
ax[2].plot(DF_Year.index, DF_Year['High']-DF_Year['Low'], 'orange')
ax[2].set_ylabel('High-Low')
ax[2].grid(True)
ax[3].plot(DF_Year.index, DF_Year['Volume'], 'pink')
ax[3].set_ylabel('Volume')
ax[3].set_xlabel('Date')
ax[3].grid(True)
plt.show()
