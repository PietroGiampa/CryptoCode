###########################
# Analysis.py Code        #
#                         #
# Pietro Giampa, Jan 2022 #
###########################

## Libraries
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from GetCurrency import GetCurrencySingleDay
from GetCurrency import GetCurrencyOneYear
from Variables import Bitcoin, Dogecoin, Shiba

# Adding Averages to the DataFrame
# Need to specify origin DataFrame, original category, and # of days
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

# Peak Finder, based on SciPy library
# Used to identify peaks for history analysis and model building
# Need to specify original DataFrame, category, height and distance input
def FindPeaksSciPy(crypto, category, height, distance):
    peaks, notes = find_peaks(crypto[category], height=height, distance=distance)
    return peaks