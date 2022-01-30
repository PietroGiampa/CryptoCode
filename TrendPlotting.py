###########################
# TrendPlotting.py        #
#                         #
# Pietro Giampa, Jan 2022 #
###########################

## Libraries
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker, cm
from scipy.signal import find_peaks
import GetCurrency as gc
import Variables as currency
import Simulations as mc
import Analysis as analysis
from datetime import datetime
from datetime import timedelta

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

# Plot for Daily report for investments
# Need to specify crypto
# -----
# select_crypto - String
def GetOneYearOverview(select_crypto):
    crypto = currency.GetCurrencyTag(select_crypto)

    ## Pull Data From Last Week and Last Year
    DF_Year = gc.GetCurrencyOneYear(crypto)
    today = datetime.today()
    DF_Week = gc.GetCurrencyPreviousWeek(crypto, today.year, today.month, today.day)

    ## Plot Style
    plt.style.use('dark_background')
    ax1 = plt.subplot2grid((2, 2), (0, 0), colspan=1)
    ax1.plot(DF_Year.index, DF_Year['Adj Close'], 'red')
    ax1.fill_between(DF_Year.index, DF_Year['Low'], DF_Year['High'], color='orange', alpha=0.5)
    ax1.set_ylabel('Adj Close')
    ax1.set_xlabel('Date')
    ax1.grid(True)
    ax2 = plt.subplot2grid((2, 2), (1, 0), colspan=1, sharex=ax1)
    ax2.plot(DF_Year.index, DF_Year['Volume'], 'green')
    ax2.set_ylabel('Volume')
    ax2.set_xlabel('Date')
    ax2.grid(True)
    ax3 = plt.subplot2grid((2, 2), (0, 1), rowspan=2)
    earnings = mc.SimPastYear(50000.0, 0.85, select_crypto)
    cs = ax3.contourf([1,2,3], [1,2,3], earnings, locator = ticker.LinearLocator(), cmap ="Greens")
    line_colors = ['black' for l in cs.levels]
    cp = ax3.contour([1,2,3], [1,2,3], earnings, colors=line_colors)
    ax3.clabel(cp, fontsize=10, colors=line_colors)
    ax3.set_xticks([1,2,3])
    ax3.set_yticks([1,2,3])
    ax3.grid(True)
    ax3.set_xlabel('Up Days - Invest')
    ax3.set_ylabel('Down Days - Sell')
    ax3.set_title('One Year MC Model')
    title_str = 'Crypto: '+select_crypto
    plt.suptitle(title_str)
    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())    
    figure = plt.gcf() # get current figure
    figure.set_size_inches(12, 7)    
    fig_name = 'Reports/'+select_crypto+'_'+str(today.day)+'_'+str(today.month)+'_'+str(today.year)+'.png'
    plt.savefig(fig_name, dpi=100)


#Plot for Daily report for investments
# Need to specify crypto
# -----
# select_crypto - String 
def GetCurrencyStatus():
    names = currency.names
    status = []
    namex = []
    today = datetime.today()
    for n in range(len(names)):
        namex.append(n)
        print('Processing ... ', names[n])
        crypto = currency.GetCurrencyTag(names[n])
        DF1 = gc.GetCurrencyPreviousWeek(crypto, today.year, today.month, today.day)
        DF1 = analysis.AddUPDOWN(DF1,'Volume')
        setnum = int(DF1.size/DF1.columns.size)
        if DF1['UPDOWN'][setnum-1]=='UP' and DF1['UPDOWN'][setnum-2]=='UP':
            status.append(3)
            GetOneYearOverview(names[n])
        elif DF1['UPDOWN'][setnum-1]=='DOWN' and DF1['UPDOWN'][setnum-2]=='DOWN':
             status.append(1)
        else:
            status.append(2)

    fig, ax = plt.subplots()
    ax.stem(namex, status)
    ax.set_xticks(namex)
    ax.set_yticks([1,2,3])
    ax.set_yticklabels(['Sell','Hold','Invest'])
    ax.set_xticklabels(names, rotation=90)
    ax.grid(True)
    ax.set_ylim(0.2,3.2)
    figure = plt.gcf()
    figure.set_size_inches(14, 8)
    fig_name = 'Reports/CryptoStatus_'+str(today.day)+'_'+str(today.month)+'_'+str(today.year)+'.png'
    plt.savefig(fig_name, dpi=100)
    plt.show()
    
GetCurrencyStatus()
