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
from Analysis import GetBaseline, AddUPDOWN, AddAverage

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

## Set Inital Pot of Money
money_start = 50000.00 #CAD

## Set Start Date Last Year
today = datetime.today()
start_date = datetime(today.year-1, today.month, today.day)

## Set the cryptocurrency for simulations
select_crypto = input('Select Crypto Currency: ')
coin = currency.GetCurrencyTag(select_crypto)

## Get Crypto Data
crypto = gc.GetCurrencyOneYear(coin)
crypto = AddUPDOWN(crypto,'Volume')

## Variables
earnings = [[0 for i in range(4)] for j in range(4)]
earnings_X = []
earnings_Y = []


## Loop Through Data
for invst_th in range(1,5):
    for wdraw_th in range(1,5):
        current_money=money_start
        upcount=0
        downcount=0
        gain=0.
        invst_frac=0.95
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
                gain = current_money*invst_frac*((invst_out-invst_in)/invst_in)
                current_money = current_money + gain
                status='SELL'
                status='HOLD'
        #print(invst_th, '\t', wdraw_th, '\t', current_money)
        earnings[invst_th-1][wdraw_th-1]=current_money
        earnings_X.append(wdraw_th)
        earnings_Y.append(invst_th)
        
#plt.style.use('_mpl-gallery-nogrid')
fig, ax = plt.subplots()
cs = ax.contourf([1,2,3,4], [1,2,3,4], earnings, cmap='RdBu_r', levels=500)
plt.show()
