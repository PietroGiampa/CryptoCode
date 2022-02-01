###########################
# Analysis.py Code        #
#                         #
# Pietro Giampa, Jan 2022 #
###########################

## Libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.signal import find_peaks
from GetCurrency import GetCurrencySingleDay
from GetCurrency import GetCurrencyPreviousWeek
from GetCurrency import GetCurrencyOneYear

# Adding Averages to the DataFrame
# Need to specify origin DataFrame, original category, and # of days
# -----
# crypto - Pandas DataFrame
# category - String
# days - Integer
def AddAverage(crypto, category, days):
    # Can only do averages if the data in the DataFrame is bigger than the requested averages
    if crypto.size/crypto.columns.size < days:
        return 'can not compute average'
    #Create name for the new DataFrame column to be added
    new_column_name = category+'_avg_%s'%str(days)
    #Loop over entries and calc average
    crypto[new_column_name] = crypto[category].rolling(window=days, center=False).mean()
    #return updated DataFrame
    return crypto

# Adding an UP, DOWN and EQUAL flag
# Need to specify origin DataFrame
# -----
# crypto - Pandas DataFrame
# category - String 
def AddUPDOWN(crypto, category):
    # Initialize Flag
    status=[]
    # Loop through DataFrame
    for k in range(int(crypto.size/crypto.columns.size)-1):
        if k==0:
            status.append('EQUAL')
        if crypto[category][k] < crypto[category][k-1]:
            status.append('DOWN')
        if crypto[category][k] > crypto[category][k-1]:
            status.append('UP')
        if crypto[category][k] == crypto[category][k-1]:
            status.append('EQUAL')
    crypto['UPDOWN'] = pd.Series(status, index=crypto.index)
    return crypto

# Peak Finder, based on SciPy library
# Used to identify peaks for history analysis and model building
# Need to specify original DataFrame, category, height and distance input
# -----
# crypto - Pandas DataFrame
# category - String
# height - Integer/Float
# distance - Integer/Float 
def FindPeaksSciPy(crypto, category, height, distance):
    #Find peaks with SciPy
    peaks, notes = find_peaks(crypto[category], height=height, distance=distance)
    #return arrays with peaks
    return peaks


# GetBaseline, for selected category
# Returns the average for a fix number of days
# -----
# crypto - Series with tagged entries from DataFrame
# categry - Float
# days - Int
def GetBaseline(crypto, category, days):
    #Initiate baseline
    baseline = 0.
    #Loop backwards in time
    for k in range(days):
        baseline = baseline + crypto[category][k]
    #normalize by number of days selected
    baseline = baseline/float(days)
    #return baseline float
    return baseline

# GetStatus, for selected category
# Returns the investmet status
# -----
# crypto - Series with tagged entries from DataFrame
def GetStatus(crypto, category):
    status = 'Hold'
    status_id = 2
    if crypto[category][-1]>crypto[category][-2] and crypto[category][-2]>crypto[category][-3]:
        status = 'Invest'
        status_id = 3
    if crypto[category][-1]<crypto[category][-2] and crypto[category][-2]<crypto[category][-3]:
        status = 'Sell'
        status_id = 1
    return status, status_id
