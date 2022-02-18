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

# Adding High-Low mediam
# Need crypto DataFrame
# -----
# crypto - Pandas DataFrame
def AddHighLowMedian(crypto):
    crypto['Mid'] = (crypto['High']-crypto['Low'])/2.
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
    mean, variance = GetBasicStats(crypto, 2)
    if crypto[category][-1]>crypto[category][-2] and crypto[category][-2]>crypto[category][-3]:
        if crypto[category][-1] > (mean[category]+variance[category]):
            status = 'Invest - Invest'
            status_id = 3
        else:
            status = 'Invest'
            status_id = 3
    if crypto[category][-1]<crypto[category][-2] and crypto[category][-2]<crypto[category][-3]:
        status = 'Sell'
        status_id = 1
    return status, status_id

# GetStatus, for selected category
# Returns the investmet status
# -----
# crypto - Series with tagged entries from DataFrame
def GetStatusMACD(crypto):
    status = 'Hold'
    status_id = 2
    slow = 26
    fast = 12
    sgl = 9
    crypto_macd = GetMACDDF(crypto, slow, fast, sgl)
    for i in range(0, crypto['Close'].size):
        if crypto_macd['macd'][i] < crypto_macd['signal'][i]:
            if status != 'Invest':
                status = 'Invest'
                status_id = 3
            else:
                status = 'Hold'
                status_id = 2
        elif crypto_macd['macd'][i] > crypto_macd['signal'][i]:
            if status == 'Invest':
                signal = 'Sell'
                status_id = 1
            else:
                signal = 'Hold'
                status_id = 2
    return status, status_id
                    
# GetStats, for given category
# Returns baseline, variance
# -----
# crypto - Series with tagged entries from DataFrame
# invest - Integer
def GetBasicStats(crypto,invest):
    crypto_select = crypto.tail(7)
    dropout = [crypto_select]
    crypto_select.drop(crypto_select.index[[-1,-2]])
    mean = crypto_select.mean()
    variance = crypto_select.var()
    return mean, variance

# GetAwesomeOscillator, for a given category
# Returns Awesome Oscillator
# -----
# crypto - DataFrame
# category - String
def GetAwesomeOscillator(crypto):
    crypto_long = crypto.tail(34)
    crypto_short = crypto.tail(5)
    AweOsc = crypto_short.mean() - crypto_long.mean()
    return AweOsc

# GetMACDDF, for a given crypto DataFrame
# Returns a DataFrame for MACD
# -----
# crypto - DataFrame
# slow - Integer
# fast - Integer
# sgl - Integer
def GetMACDDF(crypto, slow, fast, sgl):
    ewm_fast = crypto['Close'].ewm(span = fast, adjust = False).mean()
    ewm_slow = crypto['Close'].ewm(span = slow, adjust = False).mean()
    macd = pd.DataFrame(ewm_fast - ewm_slow).rename(columns = {'Close':'macd'})
    signal = pd.DataFrame(macd.ewm(span = sgl, adjust = False).mean()).rename(columns = {'macd':'signal'})
    hist = pd.DataFrame(macd['macd'] - signal['signal']).rename(columns = {0:'hist'})
    frames =  [macd, signal, hist]
    df = pd.concat(frames, join = 'inner', axis = 1)
    return df

def GetHeikinAshiCandles(crypto):
    crypto['HA_Close'] = (crypto['Open'] + crypto['High'] + crypto['Low'] + crypto['Close']) / 4
    crypto['HA_Open'] = (crypto['Open'].shift(1) + crypto['Open'].shift(1)) / 2
    crypto.iloc[0, crypto.columns.get_loc("HA_Open")] = (crypto.iloc[0]['Open'] + crypto.iloc[0]['Close'])/2
    crypto['HA_High'] = crypto[['High', 'Low', 'HA_Open', 'HA_Close']].max(axis=1)
    crypto['HA_Low'] = crypto[['High', 'Low', 'HA_Open', 'HA_Close']].min(axis=1)
    crypto['Date'] = crypto.index
    df = crypto.drop(['Open', 'High', 'Low', 'Close', 'Volume'], axis=1)  # remove old columns
    df = df.rename(columns={"Date":"Date", "HA_Open": "Open", "HA_High": "High", "HA_Low": "Low", "HA_Close": "Close"})
    df = df[['Date','Open', 'High', 'Low', 'Close']]  # reorder columns
    return df

def GetRSI(crypto):
    period = 14
    delta = crypto.diff().dropna()
    u = delta * 0
    d = u.copy()
    u[delta > 0] = delta[delta > 0]
    d[delta < 0] = -delta[delta < 0]
    u[u.index[period-1]] = np.mean( u[:period] ) #first value is sum of avg gains
    u = u.drop(u.index[:(period-1)])
    d[d.index[period-1]] = np.mean( d[:period] ) #first value is sum of avg losses
    d = d.drop(d.index[:(period-1)])
    rs = pd.DataFrame.ewm(u, com=period-1, adjust=False).mean() / \
         pd.DataFrame.ewm(d, com=period-1, adjust=False).mean()
    return 100 - 100 / (1 + rs)

# GetBollingerBands, for a given crypto DataFrame
# Returns a DataFrame for BollingerBands
# -----
# crypto - DataFrame
# span - Integer
def GetBollingerBands(crypto, span):
    mean = crypto['Close'].ewm(span = span, adjust = False).mean()
    std = crypto['Close'].ewm(span = span, adjust = False).std()
    twostd = std*2.0
    highband = pd.DataFrame(mean + twostd).rename(columns = {'Close':'high_band'})
    lowband = pd.DataFrame(mean - twostd).rename(columns = {'Close':'low_band'})
    frames = [mean, highband, lowband]
    df = pd.concat(frames, join = 'inner', axis = 1)
    return df


