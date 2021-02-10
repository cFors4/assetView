import time
from datetime import date
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from secrets import *

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from currency_converter import CurrencyConverter
c = CurrencyConverter()

import PyPDF2 

def load_driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--allow-running-insecure-content")

    driver = webdriver.Chrome(options = chrome_options)

    return driver

def login212(driver, url, username, password):
    driver.get(url)
    time.sleep(5)
    login_field = driver.find_element_by_xpath("//*[@id='username-real']")
    password_field = driver.find_element_by_xpath("//*[@id='pass-real']")
    try:
        login_button = driver.find_element_by_xpath("/html/body/div[1]/section[2]/div/div/div/form/input[8]") #input value changed from 6 to 8
    except:
        login_button = driver.find_element_by_xpath("/html/body/div[1]/section[2]/div/div/div/form/input[6]")

    login_field.clear()
    password_field.clear()
    
    login_field.send_keys(username)
    time.sleep(2)
    password_field.send_keys(password)
    time.sleep(3)
    login_button.click()

def getdata212(driver):

    total = driver.find_element_by_xpath("//*[@id='app']/div[1]/div[2]/div[2]/div[1]/div/div[1]/div/div[1]/div[1]/div[1]/div/div/label/label[2]")
    total = int(total.text.replace(',',''))
    profit = driver.find_element_by_xpath("//*[@id='app']/div[1]/div[2]/div[2]/div[1]/div/div[1]/div/div[1]/div[2]/div[2]/div[2]")
    profit = profit.text

    profitData = profit.split()

    netProfit = profitData[0][2:len(profitData[0])-3].replace(',','')
    pecentageProfit = profitData[1][1:len(profitData[1])-1].replace('%','')

    cash = driver.find_element_by_xpath("//*[@id='app']/div[1]/div[1]/div/div[2]/div[1]/div/span[2]")
    cash = cash.text
    cash = int(cash[1:len(cash)-3].replace(',',''))-int(total)
    
    return total,int(netProfit),float(pecentageProfit),cash
            
def getdataPro(driver,url,urlPro9):
    driver.get(url)
    time.sleep(5)                              
    fetch_field = driver.find_element_by_xpath('//*[@id="t-formula-bar-input"]/div').text
    BTC = float(fetch_field)
    bitcoin_api_url = 'https://www.google.com/search?q=bitcoin+price&oq=bitocin+pri&aqs=chrome.1.69i57j0i10i131i433i457j0i10i131i433l6.4397j1j4&sourceid=chrome&ie=UTF-8'
    driver.get(bitcoin_api_url)
    time.sleep(5)  
    BTC_field = driver.find_element_by_xpath('//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').text
    BTC_price = float(BTC_field.replace(',',''))
    urlcash = urlPro9
    driver.get(urlcash)
    time.sleep(5)                              
    cash_field = driver.find_element_by_xpath('//*[@id="t-formula-bar-input"]/div').text
    cash = float(cash_field)

    # avgPrice = 7700
    # costBasis = avgPrice*BTC
    # sold out initial investment so cost basis is now current contributions since 19/01/2021
    costBasis = 0 + 0 + 0
    gain = (BTC_price*BTC)-costBasis

    return BTC_price*BTC,gain,cash

def getdataToro(driver,url,password):
    print("Etoro protfolio")
    driver.get(url)
    time.sleep(5)
    username_field = driver.find_element_by_xpath('//*[@id="username"]')
    username_field.send_keys('connorsforsyth@gmail.com')
    password_field = driver.find_element_by_xpath('//*[@id="password"]')
    password_field.send_keys(password)
    sign_in = driver.find_element_by_xpath('/html/body/ui-layout/div/div/div[1]/login/login-sts/div/div/div/form/div/div[5]/button')
    sign_in.click()
    
def loginFI(driver, url, username, password):
    driver.get(url)
    time.sleep(7)
    login_field = driver.find_element_by_xpath('//*[@id="main"]/div/div/div/div/div/div[1]/div/div/input')
    continue_button = driver.find_element_by_xpath('//*[@id="main"]/div/div/div/div/div/div[2]/button') #input value changed from 6 to 8
    login_field.send_keys(username)
    time.sleep(2)
    continue_button.click()
    time.sleep(4)
    try:
        password_field = driver.find_element_by_xpath('//*[@id="main"]/div/div/div/div/div/div[2]/div/div/input')
    except:
        password_field = driver.find_element_by_xpath('//*[@id="password"]')
    try:
        continue_button2 = driver.find_element_by_xpath('//*[@id="main"]/div/div/div/div/div/div[4]/button')
    except:
        continue_button2 = driver.find_element_by_xpath('/html/body/main/section/div/div/div/form/div[2]/button')
    password_field.send_keys(password)
    time.sleep(2)
    continue_button2.click()
    time.sleep(5)
    blockFI = driver.find_element_by_xpath('//*[@id="main"]/div/div[2]/div/div/div[1]/div/div[2]/div[1]/div[1]/label[2]/label')
                                            
    blockFI = blockFI.text
    blockFI = blockFI.replace(',','')
    blockFI = float(blockFI.replace('$',''))
    

    costBasis = 990 + 300 + 0 #1.1 @ £900 + any additions to blockfi 
    poundBlockFI = c.convert(blockFI, 'USD', 'GBP')
    gain = poundBlockFI - costBasis
    netPercentage = gain/costBasis 

    return poundBlockFI,gain
    
def loginNation(driver, url, username, password):
    driver.get(url)
    time.sleep(7)
    close_button = driver.find_element_by_xpath('/html/body/div[4]/md-dialog/md-dialog-actions/button')
    switch_button = driver.find_element_by_xpath('/html/body/ui-view/div[2]/div[2]/div/div[2]/a')
    time.sleep(1)
    close_button.click()
    time.sleep(1)
    switch_button.click()
    login_field = driver.find_element_by_xpath('//*[@id="input_0"]')
    password_field = driver.find_element_by_xpath('//*[@id="input_1"]')
    time.sleep(2)
    continue_button = driver.find_element_by_xpath('/html/body/ui-view/div[2]/div[1]/div/form/div/div[1]/div[2]/button/span')
    login_field.send_keys(username)
    time.sleep(2)
    password_field.send_keys(password)
    time.sleep(3)
    continue_button.click()
    time.sleep(5)
    balance = driver.find_element_by_xpath('//*[@id="sideBar"]/div[1]/div[1]/div[1]')
    debt = balance.text
    refresh_button = driver.find_element_by_xpath('//*[@id="sideBar"]/div[2]/div/div[3]/div/div[2]/div[1]/div[2]/div/img')
    refresh_button.click()
    debt = debt.replace(',','')
    debt = float(debt.replace('£',''))

    return debt
    
def main():
    today = date.today()
    t = time.localtime()
    now = time.strftime("%H:%M:%S", t)
    url212 = "https://trading212.com/it/login"
    plt.close('all')
    urlGooglePro = urlPro
    urlFI = "https://app.blockfi.com/signin"
    urlNation = "https://my.moneydashboard.com/dashboard"
    
    password = password212
    passwordFI = password + '!'
    driver = load_driver()
    #Nationwide
    print("debt collection")
    liabilites = loginNation(driver, urlNation, username, password)
    print(liabilites)
    # liabilites = -1600

    #BLOCKFI
    print("block fi portfolio")
    totalFI,netProfitFI = loginFI(driver, urlFI, username, passwordFI)
    print(totalFI,netProfitFI)
    # totalFI     = 1000
    # netProfitFI = 10
    
    #TRADING212
    print("trading 212 protfolio")
    login212(driver, url212, username, password)
    time.sleep(20)
    total212,netProfit212,pecentageProfit212,cash212 = getdata212(driver)
    print(total212,netProfit212,cash212)
    # total212 = float(11110.60)
    # netProfit212 = float(2295.57)
    # totalwithcash = float(12226.56)
    # cash212 = float(totalwithcash - total212)

    #ETORO - protected
    # totalToro,netProfitToro,cashToro = getdataToro(driver,urlEtoro,password)
    print("Etoro protfolio")
    totalEtoro = 236
    netprofitEtoro = 82
    print(totalEtoro,netprofitEtoro)

    #BITCOIN - figure out way to automate cost basis
    print("coinbase pro protfolio")
    totalPro,netProfitPro,cashPro = getdataPro(driver,urlGooglePro,urlPro9)
    print(totalPro,netProfitPro,cashPro)
    # totalPro = 2530
    # netProfitPro = 2500
    # cashPro = 0

    driver.close()
    driver.quit()
    ##################
    #CALCULATIONS on data
    totalAssets = round(total212+totalPro+totalEtoro+totalFI,3)
    netProfit = round(netProfit212+netProfitPro+netprofitEtoro+netProfitFI,3)
    totalAssetsInvested = round(totalAssets-netProfit,3)
    percentageProfit = round(netProfit/totalAssetsInvested,5)
    netCash = round(cash212+cashPro,3)

    print("debt")
    totalLiabilites = 0 + liabilites
    print(totalLiabilites)
    # plt.style.use('dark_background')
    # plt.style.use('fivethirtyeight') 
    ##if percentage profit or profit negative - default to zero and subtract from total
    if (netProfit<0):
        print("uh oh stinky")
        totalLiabilites = totalLiabilites + netProfit
        netProfit = 0
        percentageProfit = 0

    #store and plot data
    # #################invested/profit/cash over time
    assets = [now,today,totalAssetsInvested,netProfit,netCash,0]
    df = pd.read_csv('assets.csv')
    df.loc[len(df)] = assets
    column = df["netProfit"]
    max_value = column.max()

    increase_month            = netProfit - df['netProfit'].iloc[-30]
    increase_month_percentage = (increase_month/df['netProfit'].iloc[-30])*100
    

    netCashMean = round(df["netCash"].mean(),3) #wave collapse function
    df['netCashMean'] = netCashMean
    increase_month_profit = round(increase_month,3)
    titleUp = 'Last Updated: '+str(now)+'\nTotal Invested into Assets: £'+str(totalAssetsInvested)+' Profit: £'+str(netProfit)+' Cash: £'+str(netCash) +'\n Mean cash: £'+str(netCashMean)+'\n Alltimehigh-Profit: £'+str(round(max_value,3)) +'\n  Profit increase last 30 days: £'+ str(increase_month_profit) +'\n Profit percentage increase last 30 days: % '+ str(round(increase_month_percentage,3))

        #manipulation 
    df.reset_index(inplace=True)
    df = df.sort_values('index').groupby('date').tail(1)
    df = df.drop(['index'], axis=1)
   
    df.to_csv('assets.csv',index = False)
    df.plot(figsize=(10,15))
    ax = df.plot.area(x = 'date',title=titleUp, rot=90, fontsize='10', grid=True,sharex=False,linewidth=0,colormap='gist_rainbow',stacked=False)
    ax.set_xlabel("Sum = Amount of days measured since 2019-02-21")
    ax.set_ylabel("SUM = total GBP assets = " +str(totalAssets))
    plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5), prop={'size': 15})

    ##############liabilities over time
    liabilities = [now,today,totalLiabilites,0]
    df2 = pd.read_csv('liabilities.csv')
    df2.loc[len(df2)] = liabilities
    liabilitiesMean = round(df2["totalLiabilites"].mean(),3) #wave collapse function
    df2['liabilitiesMean'] = liabilitiesMean
    titleDown = 'Liabilities: £'+str(totalLiabilites)+' liabilities Mean: £'+str(liabilitiesMean)

        #manipulation 
    df2.reset_index(inplace=True)
    df2 = df2.sort_values('index').groupby('date').tail(1)
    df2 = df2.drop(['index'], axis=1)
   
    df2.to_csv('liabilities.csv',index = False)
    df2.plot(figsize=(10,15))
    ax2 = df2.plot.area( x = 'date',title=titleDown, rot=90, fontsize='10' , grid=True,sharex=False,colormap='winter',stacked=False)
    ax2.set_xlabel("Sum = Amount of days measured since 2019-02-21")
    ax2.set_ylabel("SUM = total GBP liabilites +0%+")
    plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5), prop={'size': 15})
    
    ###############percentageProfit
    percentage = [now,today,percentageProfit,0]
    df3 = pd.read_csv('percentage.csv')
    if df3['date'].iloc[-1] == today:
        df3 = df3[:-1]
    df3.loc[len(df3)] = percentage
    column = df3["percentageProfit"]
    max_value = column.max()

    percentageProfit = percentageProfit*100
    profitChangeOnePoint          = round(percentageProfit - ((df3['percentageProfit'].iloc[-2])*100),3)
    profitChangeTwoPoints         = round(percentageProfit - ((df3['percentageProfit'].iloc[-4])*100),3)
    percentageProfitMean = round(df3["percentageProfit"].mean(),3) #wave collapse function
    df3['percentageProfitMean'] = percentageProfitMean
    titlePerc = 'Percentage Profit: %'+str(round(percentageProfit,3))+' percentageProfitMean: %'+ str(round(percentageProfitMean*100,3))+'\n Alltimehigh: %'+ str(round(max_value*100,3)) + '\n Percentage Profit change from last data point: %' +str(profitChangeOnePoint) + '\n Percentage Profit change from two data points: %' +str(profitChangeTwoPoints)

        #manipulation 
    df3.reset_index(inplace=True)
    df3 = df3.sort_values('index').groupby('date').tail(1)
    df3 = df3.drop(['index'], axis=1)
    
    df3.to_csv('percentage.csv',index = False)
    df3.plot(figsize=(10,15))
    ax3 = df3.plot.area(x = 'date',title=titlePerc, rot=90, fontsize='10', grid=True,sharex=False,linewidth=0, colormap='gist_rainbow',stacked=False)
    ax3.set_xlabel("Sum = Amount of days measured since 2019-02-21")
    ax3.set_ylabel("SUM = total percentage profit +NO LOSS+")
    plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5), prop={'size': 15})

    ##############volatility daily
    #from percentage profit
    df4 = df3[['time', 'date', 'percentageProfit']].copy()
    df4['volatility'] = -1* (df4['percentageProfit'] - df4['percentageProfit'].shift(-1))
    df4 = df4.drop(['percentageProfit'], axis=1)

    vol = profitChangeTwoPoints/100
    volatil = [now,today,vol]
    if df4['date'].iloc[-1] == today:
        df4 = df4[:-1]

    df4.loc[len(df4)] = volatil
    #calculate mean
    volatilityMean = round(df4["volatility"].mean(),3) #wave collapse function
    df4['volatilityMean'] = volatilityMean
    column = df4["volatility"]
    max_value_volatility = column.max()
    min_value_volatility = column.min()
    titleVol = 'Change of percentage profit mean: %' +str(round(volatilityMean*100,3)) + '\n Percentage profit change max: %' + str(round(max_value_volatility*100,3))+ '\nPercentage profit change min: %' + str(round(min_value_volatility*100,3))

        #mainpulation
    df4.reset_index(inplace=True)
    df4 = df4.sort_values('index').groupby('date').tail(1)
    df4 = df4.drop(['index'], axis=1)

    df4.to_csv('volatility.csv',index = False)
    df4.plot(figsize=(10,15))
    axVol = df4.plot(x = 'date',title=titleVol, rot=90, fontsize='10', grid=True,sharex=False,linewidth=2,stacked=False)
    axVol.set_xlabel("Sum = Amount of days measured since 2019-02-21")
    axVol.set_ylabel("Change of Percentage profit per day - Volatility")
    plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5), prop={'size': 15})

    ##############volatility monthly
    ##profit percentage in months format
    volMon = df3[['date','percentageProfit']].copy()
    volMon['date'] = pd.to_datetime(volMon['date'])
    volMon = volMon.groupby(pd.Grouper(key='date', freq='1M')).mean()
    volMon.index = volMon.index.strftime('%B, %Y')
    volMon = volMon.dropna()
    
    #profit percentage difference between months
    volMon['volatility'] = -1* (volMon['percentageProfit'] - volMon['percentageProfit'].shift(-1))
    changeSoFar = ((percentageProfit/100) - volMon['percentageProfit'].iloc[-2])
    volMon = volMon.replace(np.nan,changeSoFar)
    volMon = volMon.drop(['percentageProfit'], axis=1)
    column = volMon['volatility']
    max_value_volatility = column.max()
    min_value_volatility = column.min()
    #mean
    volatilityMean = round(volMon["volatility"].mean(),3) #wave collapse function
    volMon['volatilityMean'] = volatilityMean
    #graph
    volMon.reset_index(inplace=True)
    print(volMon)
    # volMon = volMon.drop(['index'], axis=1)

    titleVolMon = 'Change of percentage profit mean: %' +str(round(volatilityMean*100,3)) + '\n Percentage profit change max: %' + str(round(max_value_volatility*100,3))+ '\nPercentage profit change min: %' + str(round(min_value_volatility*100,3))
    volMon.plot(figsize=(10,15))
    axVolMon = volMon.plot(x = 'date',title=titleVolMon, rot=90, fontsize='10', grid=True,sharex=False,linewidth=2,stacked=False)
    axVolMon.set_xlabel("Sum = Amount of months measured since 2019-02-21")
    axVolMon.set_ylabel("Change of Percentage profit per Month - Volatility")
    plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5), prop={'size': 15})

    ##############bar percentage monthly
    percMon = df3[['date','percentageProfit']].copy()
    percMon['date'] = pd.to_datetime(percMon['date'])
    percMon = percMon.groupby(pd.Grouper(key='date', freq='1M')).mean()
    percMon.index = percMon.index.strftime('%B, %Y')
    percMon['percentageProfit'] = percMon['percentageProfit'].apply(lambda x: x*100)
    percMon = percMon.dropna()
    percMon.reset_index(inplace=True)
    #manipulation
    percMon.plot(figsize=(10,15))
    axPercMon = percMon.plot(kind = 'bar',x = 'date', rot=90, fontsize='10', grid=True,sharex=False,linewidth=0,stacked=False)
    axPercMon.set_xlabel("Sum = Amount of months measured since 2019-02-21")
    axPercMon.set_ylabel("Change of Percentage profit per Month")
    plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5), prop={'size': 15})

    for p in axPercMon.patches:
        width, height = p.get_width(), p.get_height()
        x, y = p.get_xy() 
        axPercMon.text(x+width/2, 
                y+height/2, 
                '{:.0f}%'.format(height), 
                horizontalalignment='center', 
                verticalalignment='center')

    ##############stacked bar chart monthly averages
    stacked = df[['date','totalAssetsInvested', 'netProfit', 'netCash']].copy()
    stacked = stacked.join(df2["totalLiabilites"])
    stacked['date'] = pd.to_datetime(stacked['date'])
    stacked = stacked.groupby(pd.Grouper(key='date', freq='1M')).mean()
    stacked.index = stacked.index.strftime('%B, %Y')
    stacked = stacked.dropna()

    liabilitesSafeLimit = -3000
    cashNeeded = round((totalAssetsInvested/2)-(totalLiabilites-liabilitesSafeLimit)-netCash,3)
    titleStacked = 'diversification = less volatility which != less risk \n Buying power needed for crash(-50%):  '+str(totalAssetsInvested*0.5) +'\nCASH TO GET AND SIT: '+str(cashNeeded)
    ax4 = stacked.plot(kind = 'bar',title=titleStacked, stacked=True, rot=90, fontsize='10', grid=True,sharex=False,linewidth=0)
    ax4.set_xlabel("Sum = Amount of months measured since 2019-02-21")
    ax4.set_ylabel("SUM = Monthly average NET")
    plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5), prop={'size': 15})
    
    for p in ax4.patches:
        width, height = p.get_width(), p.get_height()
        x, y = p.get_xy() 
        ax4.text(x+width/2, 
                y+height/2, 
                '{:.0f}'.format(height), 
                horizontalalignment='center', 
                verticalalignment='center')

    ################### NET GRAPH
    netCurrent = round((totalAssetsInvested +netProfit + netCash) +totalLiabilites,3)
    Net = (df["totalAssetsInvested"]+df["netCash"]+df["netProfit"]) + df2["totalLiabilites"]
    dateInsert = df["date"]
    dateInsert = dateInsert.iloc[:-1]
    dfNet = pd.DataFrame(index=dateInsert)
    dfNet.reset_index(inplace=True)
    dfNet.insert(loc=1, column='Net', value=Net)
    dfNet.drop(dfNet.tail(1).index,inplace=True)
    dfNet.loc[len(dfNet)] = [today,netCurrent]

    dfNet.to_csv('net.csv',index = False)
    #add annotation to all time high - todo
        ##projections
    p = totalAssetsInvested
    pmt = netCashMean #calculate contributions per month (not right)
    r = percentageProfitMean #calculate return % per year YoY (not right)
    n = 12 #amount of months per year
    t = 10 #amount of years
    column = dfNet["Net"]
    max_value = column.max()
    
    projection = round(((p*(1+(r/n))) + (pmt*(((1+(r/n))**(n*t)-1)/(r/n))))-liabilitiesMean,3)
    
    goalEarningperMonth = 1500
    nestEgg = (goalEarningperMonth*12)*25
    increase_month            = netCurrent - dfNet['Net'].iloc[-30]
    increase_month_percentage = (increase_month/dfNet['Net'].iloc[-30])*100
    increase_month_net = round(increase_month,3)
    increase_month_contribution = increase_month_net - increase_month_profit
    hourly_salary = round(netProfit/2080,3) #make over a year 
    titleNet = 'NET worth: £'+str(netCurrent)+'\n Projection at current rate (10 years): £'+str(projection)+'\n 4% rule to earn £'+str(goalEarningperMonth)+' a month: £'+str(nestEgg) +'\n Currently could make a month @6%: £'+ str(round((netCurrent*0.06)/12,3))+'\n Alltimehigh: £'+ str(round(max_value,3)) +'\n Alltimehigh difference: £'+ str(round(-1*(max_value-netCurrent),3)) +'\n  Increase this last 30 days: £'+ str(increase_month_net) +'\n percentage increase last 30 days: % '+ str(round(increase_month_percentage,3)) + '\nContributions last 30 days: £' + str(round(increase_month_contribution,3)) + '\nHourly salary over a year(make a year): £' + str(hourly_salary)
    
    dfNet.plot(figsize=(10,15))
    axNet = dfNet.plot(x = 'date',title=titleNet, rot=90, fontsize='10', grid=True,sharex=False,linewidth=5, color = 'lightgreen')
    axNet.set_xlabel("Sum = Amount of days measured since 2019-02-21")
    axNet.set_ylabel("Net £")
    plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5), prop={'size': 15})

    ################# Pie chart
    titlePie = 'GOAL AMOUNTS \nStocks:Crypto 77:22 (3.5): '+str(round((total212 + totalEtoro)/(totalPro + totalFI),3)) + '\nAmount in Main:' + str(total212*0.77) + '\nAmount in ARK:' + str(total212*0.15) + '\nAmount in ARKG:' + str(total212*0.075) + '\nAmount in ARK(rest):' + str(total212*0.0188) + '\nAmount in experiments:' + str(round(total212*0.03,3))
    labels = ['StocksInvested (70%)', 'StocksProfit' ,'CryptoInvested (20)%','CryptoProfit', 'Debt (0%)','Cash (10%)']
    sizes = [((total212 + totalEtoro)-(netProfit212 + netprofitEtoro)), (netProfit212+netprofitEtoro), ((totalPro + totalFI) - (netProfitPro + netProfitFI)), (netProfitPro + netProfitFI), (-1* totalLiabilites), netCash]
    dfPie = pd.DataFrame({'Assets/liabilites':sizes},index = labels)
    
    axPie = dfPie.plot.pie(y='Assets/liabilites', title = titlePie,figsize=(10,15), autopct = "%.2f%%", colors = ['royalblue', 'dodgerblue','gold','goldenrod','red','yellowgreen'])

    #save graphs#
    fig = ax.get_figure()
    fig.savefig('assets.pdf', bbox_inches = "tight")
    fig2 = ax2.get_figure()
    fig2.savefig('liabilities.pdf', bbox_inches = "tight")
    fig3 = ax3.get_figure()
    fig3.savefig('percentage.pdf', bbox_inches = "tight")
    fig4 = axNet.get_figure()
    fig4.savefig('net.pdf', bbox_inches = "tight")
    fig5 = axPie.get_figure()
    fig5.savefig('pie.pdf', bbox_inches = "tight")
    fig6 = ax4.get_figure()
    fig6.savefig('monthly.pdf', bbox_inches = "tight")
    fig7 = axVol.get_figure()
    fig7.savefig('volatility.pdf', bbox_inches = "tight")
    fig8 = axVolMon.get_figure()
    fig8.savefig('volatilityMonth.pdf', bbox_inches = "tight")
    fig9 = axPercMon.get_figure()
    fig9.savefig('percentageMonth.pdf', bbox_inches = "tight")

    ##MERGE PDF'S INTO ONE MAIN.PDF 
 
    # Open the files that have to be merged one by one
    pdf1File = open('assets.pdf', 'rb')
    pdf2File = open('liabilities.pdf', 'rb')
    pdf3File = open('percentage.pdf', 'rb')
    pdf4File = open('net.pdf', 'rb')
    pdf5File = open('pie.pdf', 'rb')
    pdf6File = open('monthly.pdf', 'rb')
    pdf7File = open('volatility.pdf', 'rb')
    pdf8File = open('volatilityMonth.pdf', 'rb')
    pdf9File = open('percentageMonth.pdf', 'rb')

    
    # Read the files that you have opened
    pdf1Reader = PyPDF2.PdfFileReader(pdf1File)
    pdf2Reader = PyPDF2.PdfFileReader(pdf2File)
    pdf3Reader = PyPDF2.PdfFileReader(pdf3File)
    pdf4Reader = PyPDF2.PdfFileReader(pdf4File)
    pdf5Reader = PyPDF2.PdfFileReader(pdf5File)
    pdf6Reader = PyPDF2.PdfFileReader(pdf6File)
    pdf7Reader = PyPDF2.PdfFileReader(pdf7File)
    pdf8Reader = PyPDF2.PdfFileReader(pdf8File)
    pdf9Reader = PyPDF2.PdfFileReader(pdf9File)
    
    ############ ORDER PDFS
    # Create a new PdfFileWriter object which represents a blank PDF document
    pdfWriter = PyPDF2.PdfFileWriter()
    
    # Loop through all the pagenumbers for the first document
    for pageNum in range(pdf1Reader.numPages):
        pageObj = pdf1Reader.getPage(pageNum)
        pdfWriter.addPage(pageObj)
    
    # Loop through all the pagenumbers for the second document
    for pageNum in range(pdf2Reader.numPages):
        pageObj = pdf2Reader.getPage(pageNum)
        pdfWriter.addPage(pageObj)

    # Loop through all the pagenumbers for the first document
    for pageNum in range(pdf3Reader.numPages):
        pageObj = pdf3Reader.getPage(pageNum)
        pdfWriter.addPage(pageObj)

    # Loop through all the pagenumbers for the first document- daily volatility
    for pageNum in range(pdf7Reader.numPages):
        pageObj = pdf7Reader.getPage(pageNum)
        pdfWriter.addPage(pageObj)
    
    # Loop through all the pagenumbers for the first document - monthly volatility
    for pageNum in range(pdf8Reader.numPages):
        pageObj = pdf8Reader.getPage(pageNum)
        pdfWriter.addPage(pageObj)
    
    # Loop through all the pagenumbers for the first document - monthly percentage
    for pageNum in range(pdf9Reader.numPages):
        pageObj = pdf9Reader.getPage(pageNum)
        pdfWriter.addPage(pageObj)
        
    # Loop through all the pagenumbers for the first document
    for pageNum in range(pdf6Reader.numPages):
        pageObj = pdf6Reader.getPage(pageNum)
        pdfWriter.addPage(pageObj)

    # Loop through all the pagenumbers for the first document
    for pageNum in range(pdf4Reader.numPages):
        pageObj = pdf4Reader.getPage(pageNum)
        pdfWriter.addPage(pageObj)

    # Loop through all the pagenumbers for the first document
    for pageNum in range(pdf5Reader.numPages):
        pageObj = pdf5Reader.getPage(pageNum)
        pdfWriter.addPage(pageObj)
        
    
    # Now that you have copied all the pages in both the documents, write them into the a new document
    pdfOutputFile = open('main.pdf', 'wb')
    pdfWriter.write(pdfOutputFile)
    
    # Close all the files - Created as well as opened
    pdfOutputFile.close()
    pdf1File.close()
    pdf2File.close()
    pdf3File.close()
    pdf4File.close()
    pdf5File.close()
    pdf6File.close()
    pdf7File.close()
    pdf8File.close()
    pdf9File.close()
    #data analysis - collect more data - find out best and worst move probabilistically - research
    #have annotations on pie chart based on data analysis
    #data science - what stack leads to most increase correlation gradient to ratio to find optimal ratio for increase (affected by adding cash and how frequencly you but once adding cash)

if __name__ == "__main__":
    main()
