###########################
# TrendPlotting.py        #
#                         #
# Pietro Giampa, Jan 2022 #
###########################

## Libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import ticker, cm
from matplotlib.dates import DateFormatter
import matplotlib.dates as mpdates
import os, glob
import img2pdf
from PIL import Image
import GetCurrency as gc
import Variables as currency
import Simulations as mc
import Analysis as analysis
from datetime import datetime
from datetime import timedelta
from mplfinance.original_flavor import candlestick_ohlc

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
def GetOverview(select_crypto, today, tag, status):
    crypto = currency.GetCurrencyTag(select_crypto)

    ## Pull Data From Last Week and Last Year
    if tag=='Year':
        DF = gc.GetCurrencyOneYear(crypto)
    elif tag=='Week':
        DF = gc.GetCurrencyPreviousWeek(crypto, today.year, today.month, today.day)

    ## Plot Style
    plt.style.use('dark_background')
    ax1 = plt.subplot2grid((2, 2), (0, 0), colspan=1)
    ax1.plot(DF.index, DF['Adj Close'], 'red')
    ax1.fill_between(DF.index, DF['Low'], DF['High'], color='orange', alpha=0.5)
    ax1.set_ylabel('Adj Close')
    ax1.set_xlabel('Date')
    ax1.grid(True)
    ax1.xaxis.set_major_formatter(DateFormatter("%m-%d"))
    ax2 = plt.subplot2grid((2, 2), (1, 0), colspan=1, sharex=ax1)
    ax2.plot(DF.index, DF['Volume'], 'green')
    ax2.set_ylabel('Volume')
    ax2.set_xlabel('Date')
    ax2.grid(True)
    ax2.xaxis.set_major_formatter(DateFormatter("%m-%d"))
    ax3 = plt.subplot2grid((2, 2), (0, 1), rowspan=2)
    earnings = mc.SimPastYear(10000.0, 0.95, select_crypto)
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
    title_str = 'Crypto: '+select_crypto+' - '+status
    plt.suptitle(title_str)
    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())    
    figure = plt.gcf() # get current figure
    figure.set_size_inches(12, 7)    
    fig_name = 'Reports/'+select_crypto+'_'+str(today.day)+'_'+str(today.month)+'_'+str(today.year)+'.png'
    plt.savefig(fig_name, dpi=100)

# Plot for Daily MACD
# Need to specify crypto
# -----
# crypto - DataFrame
# crypto_macd - DataFrame
# tag - String
# slow - Integer
# fast - Integer
# sgl - Integer
# today - datetime
def GetMACDplot(crypto, tag, slow, fast, sgl, today, status):

    crypto_tag = currency.GetCurrencyTag(crypto)
    ## Pull Data From Last Week and Last Year
    if tag=='Year':
        DF = gc.GetCurrencyOneYear(crypto_tag)
    
    ## Pull Data From Last Week and Last Year
    if tag=='Week':
        return 0

    crypto_macd = analysis.GetMACDDF(DF, slow, fast, sgl)
    
    ax1 = plt.subplot2grid((2, 2), (0, 0), colspan=1)    
    ax1.plot(DF.index, DF['Adj Close'], 'red')
    ax1.fill_between(DF.index, DF['Low'], DF['High'], color='orange', alpha=0.5)
    ax1.plot(DF['Close'])
    ax1.set_ylabel('Close')
    ax1.grid(True)
    ax2 = plt.subplot2grid((2, 2), (1, 0), colspan=1, sharex=ax1)
    ax2.plot(crypto_macd['macd'], color = 'violet', linewidth = 1.5, label = 'MACD')
    ax2.plot(crypto_macd['signal'], color = 'royalblue', linewidth = 1.5, label = 'SIGNAL')
    ax2.set_ylabel('MACD')
    ax2.set_xlabel('Date')
    ax2.grid(True)
    ax2.xaxis.set_major_formatter(DateFormatter("%m-%d"))
    for i in range(len(DF['Close'])):
        if str(crypto_macd['hist'][i])[0] == '-':
            ax2.bar(DF['Close'].index[i], crypto_macd['hist'][i], color = '#ef5350')
        else:
            ax2.bar(DF['Close'].index[i], crypto_macd['hist'][i], color = '#26a69a')

    ax3 = plt.subplot2grid((2, 2), (0, 1), rowspan=2)
    earnings = mc.MACDSimPastYear(10000.0, 0.95, crypto)
    cs = ax3.contourf([1,2,3,4], [1,2,3,4], earnings, locator = ticker.LinearLocator(), cmap ="Greens")
    line_colors = ['black' for l in cs.levels]
    cp = ax3.contour([1,2,3,4], [1,2,3,4], earnings, colors=line_colors)
    ax3.clabel(cp, fontsize=10, colors=line_colors)
    ax3.grid(True)
    ax3.set_xlabel('')
    ax3.set_ylabel('Fast Component')
    ax3.set_title('Slow Component')
    title_str = 'MACD Crypto: '+crypto+' - '+status
    plt.suptitle(title_str)

    plt.style.use('dark_background')
    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())
    figure = plt.gcf() 
    figure.set_size_inches(12, 7)
    fig_name = 'Reports/macd_'+crypto+'_'+str(today.day)+'_'+str(today.month)+'_'+str(today.year)+'.png'
    plt.savefig(fig_name, dpi=100)

# Plot for Daily report for investments
# Need to specify crypto
# -----
# select_crypto - String 
def GetCurrencyStatus():
    names = currency.names
    status = []
    namex = []
    today = datetime.today()
    tag='Year'
    img_list = []
    slow = 26
    fast = 12
    sgl = 9
    for n in range(len(names)):
        namex.append(n)
        print('Processing ... ', names[n])
        crypto = currency.tags[n]
        DF1 = gc.GetCurrencyOneYear(crypto)
        stat, stat_id = analysis.GetStatusMACD(DF1)
        status.append(stat_id)
        if stat=='Invest' or stat=='Hold':
            GetOverview(names[n], today, tag, stat)
            img_list.append('Reports/'+names[n]+'_'+str(today.day)+'_'+str(today.month)+'_'+str(today.year)+'.png')
            GetMACDplot(names[n], tag, slow, fast, sgl, today, stat)
            img_list.append('Reports/macd_'+names[n]+'_'+str(today.day)+'_'+str(today.month)+'_'+str(today.year)+'.png')

    plt.style.use('dark_background')
    fig, ax = plt.subplots()
    ax.stem(namex, status, markerfmt='ro')
    ax.set_xticks(namex)
    ax.set_yticks([1,2,3])
    ax.set_yticklabels(['Sell','Hold','Invest'])
    ax.set_xticklabels(names, rotation=90)
    ax.grid(True, axis='y')
    ax.set_ylim(0.2,3.2)
    ax.set_title('Crypto Trading Status')
    figure = plt.gcf()
    figure.set_size_inches(14, 8)
    fig_name = 'Reports/CryptoStatus_'+str(today.day)+'_'+str(today.month)+'_'+str(today.year)+'.png'
    plt.savefig(fig_name, dpi=100)
    img_list.insert(0,fig_name)
    ofile_name = 'Reports/DailyReport_'+str(today.day)+'_'+str(today.month)+'_'+str(today.year)+'.pdf'
    im_list = []
    for ii in range(len(img_list)):
        rgba = Image.open(img_list[ii])
        rgb = Image.new('RGB', rgba.size, (255, 255, 255))
        rgb.paste(rgba, mask=rgba.split()[3])
        im_list.append(rgb)
    im_list[0].save(ofile_name, "PDF" ,resolution=100.0, save_all=True, append_images=im_list[1:])
    return ofile_name

def GetDailyReports():
    names = currency.names
    status = []
    namex = []
    today = datetime.today()
    tag = 'Year'
    img_list = []
    slow = 26
    fast = 12
    sgl = 9
    #len(names)
    #for n in range(len(names)):
    namex.append(23)
    print('Processing ... ', names[23])
    crypto = names[23]
    crypto_tag = currency.GetCurrencyTag(crypto)
    DF = gc.GetCurrencyOneYear(crypto_tag)
    stat, stat_id = analysis.GetStatusMACD(DF)

    crypto_macd = analysis.GetMACDDF(DF, slow, fast, sgl)
    crypto_ha = analysis.GetHeikinAshiCandles(DF)
    crypto_rsi = DF['Close']
    rsi = analysis.GetRSI(crypto_rsi)
    
    crypto_ha['Date'] = pd.to_datetime(crypto_ha['Date'])
    crypto_ha['Date'] = crypto_ha['Date'].map(mpdates.date2num)

    ax1 = plt.subplot2grid((2, 2), (0, 0), colspan=1)
    ax1.plot(rsi.index, rsi, 'red')
    ax1.set_ylabel('Volume Indicator')
    ax1.grid(True)
    ax2 = plt.subplot2grid((2, 2), (1, 0), colspan=1, sharex=ax1)
    ax2.plot(crypto_macd['macd'], color = 'darkorange', linewidth = 1.5, label = 'MACD')
    ax2.plot(crypto_macd['signal'], color = 'royalblue', linewidth = 1.5, label = 'SIGNAL')
    ax2.set_ylabel('Momentum Indicator')
    ax2.set_xlabel('Date')
    ax2.grid(True)
    ax2.xaxis.set_major_formatter(DateFormatter("%m-%d"))
    for i in range(len(DF['Close'])):
        if str(crypto_macd['hist'][i])[0] == '-':
            ax2.bar(DF['Close'].index[i], crypto_macd['hist'][i], color = '#ef5350')
        else:
            ax2.bar(DF['Close'].index[i], crypto_macd['hist'][i], color = '#26a69a')

    ax3 = plt.subplot2grid((2, 2), (0, 1), rowspan=2)
    candlestick_ohlc(ax3, crypto_ha.values, width = 0.6,colorup = 'green', colordown = 'red',alpha = 0.8)
    ax3.grid(True)
    date_format = mpdates.DateFormatter('%d/%m')
    ax3.xaxis.set_major_formatter(date_format)
    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())
    figure = plt.gcf()
    plt.show()
