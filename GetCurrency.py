###########################
# GetCurrency.py Code     #
#                         #
# Pietro Giampa, Jan 2022 #
###########################

## Libraries
import numpy as np
import pandas_datareader as pdr
from datetime import datetime
from datetime import timedelta

# Get Currency Data for a Single Day
# Need to specify origin DataFrame, year, month and day
# -----
# currency - Pandas DataFrame
# year - Integer
# month - Integer
# day - Integer 
def GetCurrencySingleDay(currency, year, month, day):
    start = datetime(year,month,day)
    end = datetime(year,month,day)
    CC = pdr.DataReader(currency,'yahoo',start,end)
    return CC

# Get Currency Data for Previous Week
# Need to specify origin DataFrame, year, month and day
# -----
# currency - Pandas DataFrame
# year - Integer
# month - Integer
# day - Integer 
def GetCurrencyPreviousWeek(currency, year, month, day):
    end = datetime(year, month, day)
    start = end - timedelta(days=14)
    CC = pdr.DataReader(currency,'yahoo',start,end)
    return CC

# Get Currency Data for the N Days
# Need to specify origin Currency, Delay
# -----
# currency - Float
# delay = int
def GetCurrencyPreviusNDays(currency, delay):
    end = datetime.today()
    start = end - timedelta(days=delay)
    CC = pdr.DataReader(currency,'yahoo',start,end)
    return CC

# Get Currency Data for the Past Year
# Need to specify origin DataFrame, year, month and day
# -----
# currency - Pandas DataFrame
def GetCurrencyOneYear(currency):
    end = datetime.today()
    start = datetime(end.year-1, end.month, end.day)
    CC = pdr.DataReader(currency,'yahoo',start,end)
    return CC

# Get Currency Data for the Past 5 Years
# Need to specify origin DataFrame, year, month and day
# -----
# currency - Pandas DataFrame
def GetCurrencyHistory(currency):
    end = datetime.today()
    start = datetime(end.year-5, end.month, end.day)
    CC = pdr.DataReader(currency,'yahoo',start,end)
    return CC
