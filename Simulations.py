###########################
# Simulations.py          #
#                         #
# Pietro Giampa, Jan 2022 #
###########################

## Libraries
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker, cm
import pandas as pd
import GetCurrency as gc
from datetime import datetime
import Variables as currency
import Analysis as analysis

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

# Run Volume Model over the past year
# Need to specify original investment and fraction of support and crypto
# -----
# money_start - Float
# invst_frac - Float
# select_crypto = String
def SimPastYear(money_start, invst_frac, select_crypto):

    ## Set Start Date Last Year
    today = datetime.today()
    start_date = datetime(today.year-1, today.month, today.day)
    
    ## Set the cryptocurrency for simulations
    #select_crypto = input('Select Crypto Currency: ')
    coin = currency.GetCurrencyTag(select_crypto)
    
    ## Get Crypto Data
    crypto = gc.GetCurrencyOneYear(coin)
    crypto = analysis.AddUPDOWN(crypto,'Volume')
    
    ## Variables
    earnings = [[0 for i in range(3)] for j in range(3)]
    earnings_X = []
    earnings_Y = []

    ## Loop Through Data
    for invst_th in range(1,4):
        for wdraw_th in range(1,4):
            current_money=money_start
            upcount=0
            downcount=0
            gain=0.
            invst_in=0.
            invst_out=0.
            status='HOLD'
            for nevent in range(0, crypto['Close'].size):        
                if crypto['UPDOWN'][nevent]=='UP':
                    upcount = upcount + 1
                    downcount = 0        
                if crypto['UPDOWN'][nevent]=='DOWN':
                    upcount = 0
                    downcount = downcount + 1
                if status=='HOLD' and upcount==invst_th and crypto['Close'][nevent]>0.:
                    status='INVEST'
                    invst_in=crypto['Close'][nevent]
                if status=='INVEST' and downcount==wdraw_th:        
                    invst_out=crypto['Close'][nevent]
                    gain = current_money*invst_frac*((invst_out-invst_in)/abs(invst_in))
                    current_money = current_money + gain
                    status='SELL'
                    status='HOLD'
            earnings[invst_th-1][wdraw_th-1]=current_money
            earnings_Y.append(wdraw_th)
            earnings_X.append(invst_th)
        
    #Returns earnings
    return earnings


# Run Volume Model over the past year
# Need to specify original investment and fraction of support and crypto
# -----
# money_start - Float
# invst_frac - Float
# select_crypto = String
def MACDSimPastYear(money_start, invst_frac, select_crypto):
    ## Set the cryptocurrency for simulations
    #select_crypto = input('Select Crypto Currency:                                                        
    coin = currency.GetCurrencyTag(select_crypto)
    ## Get Crypto Data
    crypto = gc.GetCurrencyOneYear(coin)
    ## Variables
    earnings = [[0 for i in range(4)] for j in range(4)]
    earnings_X = []
    earnings_Y = []

    ## Loop Through Data
    for invst_th in range(0,4):
        for wdraw_th in range(0,4):
            slow = 26-2+invst_th
            fast = 12-2+wdraw_th
            sgl = 9
            crypto_macd = analysis.GetMACDDF(crypto, slow, fast, sgl)    
            current_money=money_start
            upcount=0
            downcount=0
            gain=0.
            invst_in=0.
            invst_out=0.
            signal='HOLD'
            for i in range(0, crypto['Close'].size):
                if crypto_macd['macd'][i] < crypto_macd['signal'][i]:
                    if signal != 'INVEST':
                        signal = 'INVEST'
                        invst_in = crypto['Close'][i]
                    else:
                        signal = 'HOLD'
                elif crypto_macd['macd'][i] > crypto_macd['signal'][i]:
                    if signal == 'INVEST':
                        signal = 'SELL'
                        invst_out = crypto['Close'][i]
                    else:
                        signal = 'HOLD'
                if signal == 'SELL':
                    gain = current_money*invst_frac*((invst_out-invst_in)/invst_in)
                    current_money = current_money + gain

            earnings[invst_th-1][wdraw_th-1]=current_money
            earnings_Y.append(wdraw_th)
            earnings_X.append(invst_th)

    #Returns earnings
    return earnings
