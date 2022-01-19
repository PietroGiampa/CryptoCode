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

## Get Currency Data for a Single Day
def GetCurrencySingleDay(currency, year, month, day):
    start = datetime(year,month,day)
    end = datetime(year,month,day)
    CC = pdr.DataReader(currency,'yahoo',start,end)
    return CC

## Get Currency Data for Previous Week
def GetCurrencyPreviousWeek(currency, year, month, day):
    end = datetime(year, month, day)
    start = end - timedelta(days=7)
    CC = pdr.DataReader(currency,'yahoo',start,end)
    return CC

## Get Currency Data for the Past Year
def GetCurrencyOneYear(currency):
    end = datetime.today()
    start = datetime(end.year-1, end.month, end.day)
    CC = pdr.DataReader(currency,'yahoo',start,end)
    return CC

## Get Currency Data for the Past 5 Years
def GetCurrencyHistory(currency):
    end = datetime.today()
    start = datetime(end.year-5, end.month, end.day)
    CC = pdr.DataReader(currency,'yahoo',start,end)
    return CC
