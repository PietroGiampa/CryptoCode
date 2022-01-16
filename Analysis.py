###########################
# Analysis.py Code        #
#                         #
# Pietro Giampa, Jan 2022 #
###########################

## Libraries
import numpy as np
import matplotlib.pyplot as plt
from GetCurrency import GetCurrencySingleDay
from GetCurrency import GetCurrencyOneYear
from Variables import Bitcoin, Dogecoin, Shiba


# Adding Averages to the DataFrame
# Need to specify original category and # of days
def AddAverage(crypto, category, days):
    # Can only do averages if the data in the DataFrame is bigger than the requested averages
    if BTC.size/BTC.columns.size < days:
        return 'can not compute average'
    #Create name for the new DataFrame column to be added
    new_column_name = category+'_avg_%s'%str(days)
    #Loop over entries and calc average
    crypto[new_column_name] = crypto[category].rolling(window=days, center=False).mean()
    #return updated DataFrame
    return crypto

## Pick Crypto & Add 3 Days Weighted Average
#BTC = GetCurrencyOneYear(Dogecoin)
#BTC = AddAverage(BTC, 'Close', 2)
#print(BTC.head())
#BTC['Close'].plot.area(stacked=False)
#BTC['Close_avg_2'].plot()
#BTC['AC7'].plot()
#BTC['AC4'].plot()
#plt.show()
