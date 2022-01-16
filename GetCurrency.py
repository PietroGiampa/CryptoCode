## Libraries
import numpy as np
import pandas_datareader as pdr
from datetime import datetime

def GetCurrencySingleDay(currency, year, month, day):
    start = datetime(year,month,day)
    end = datetime(year,month,day)
    CC = pdr.DataReader(currency,'yahoo',start,end)
    return CC

def GetCurrencyOneYear(currency):
    end = datetime.today()
    start = datetime(end.year-1, end.month, end.day)
    CC = pdr.DataReader(currency,'yahoo',start,end)
    return CC

def GetCurrencyHistory(currency):
    end = datetime.today()
    start = datetime(end.year-5, end.month, end.day)
    CC = pdr.DataReader(currency,'yahoo',start,end)
    return CC
