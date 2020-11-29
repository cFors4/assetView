import time
from datetime import date
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from secrets import *

import csv
import pandas as pd
import matplotlib.pyplot as plt

import PyPDF2 


def load_driver():
    chrome_options = Options()

    #chrome_options.add_argument("--headless")
    #chrome_options.add_argument("--disable-extensions")
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
    print("trading 212 protfolio")

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
    print("coinbase pro protfolio")

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

    avgPrice = 7700
    costBasis = avgPrice*BTC
    gain = (BTC_price*BTC)-costBasis
    netPercentage = gain/costBasis

    return BTC_price*BTC,gain,netPercentage,cash

    
def main():
    today = date.today()
    t = time.localtime()
    now = time.strftime("%H:%M:%S", t)
    url212 = "https://live.trading212.com/beta"
    plt.close('all')
    urlGooglePro = urlPro
    
    username = "connorsforsyth@gmail.com"
    password = password212
    driver = load_driver()
    
    #Collection of data
    #TRADING212
    login212(driver, url212, username, password)
    time.sleep(20)
    total212,netProfit212,pecentageProfit212,cash212 = getdata212(driver)
    #BITCOIN
    totalPro,netProfitPro,pecentageProfitPro,cashPro = getdataPro(driver,urlGooglePro,urlPro9)
    #ETORO??
    #nationwide?? debt

    #CALCULATIONS on data
    print(total212,totalPro)
    totalAssets = round(total212+totalPro,2)
    netProfit = round(netProfit212+netProfitPro,2)
    totalAssetsInvested = round(totalAssets-netProfit,2)
    percentageProfit = round(netProfit/totalAssets,5)
    netCash = round(cash212+cashPro,2)
    totalLiabilites = -2400
    driver.close()
    driver.quit()


    #store and plot data
    # invested/profit/cash over time
    titleUp = 'Total Invested into Assets: '+str(totalAssetsInvested)+' Profit: '+str(netProfit)+' Cash: '+str(netCash)
    assets = [now,today,totalAssetsInvested,netProfit,netCash]
    df = pd.read_csv('assets.csv')
    df.loc[len(df)] = assets
    # df.to_csv('assets.csv',index = False)

        #manipulation 
    df.reset_index(inplace=True)
    df = df.sort_values('index').groupby('date').tail(1)
    df = df.drop(['index'], axis=1)
    print(df)
    df.to_csv('assets.csv',index = False)
    df.plot(figsize=(10,15))
    ax = df.plot.area(x = 'date',title=titleUp, rot=90, fontsize='10', grid=True,sharex=False,linewidth=0,colormap='gist_rainbow') #.tight_layout()
    ax.set_xlabel("Sum = Amount of days since 2020-11-27")
    ax.set_ylabel("SUM = total GBP assets")

   
    #liabilities over time
    titleDown = 'Liabilities: '+str(totalLiabilites)+''
    liabilities = [now,today,totalLiabilites]
    df2 = pd.read_csv('liabilities.csv')
    df2.loc[len(df2)] = liabilities
    # df2.to_csv('liabilities.csv',index = False)

        #manipulation 
    df2.reset_index(inplace=True)
    df2 = df2.sort_values('index').groupby('date').tail(1)
    df2 = df2.drop(['index'], axis=1)
    print(df2)
    df2.to_csv('liabilities.csv',index = False)
    df2.plot(figsize=(10,15))
    #ax = ax
    ax2 = df2.plot.area( x = 'date',title=titleDown, rot=90, fontsize='10' , grid=True,sharex=False,colormap='winter') #.tight_layout()
    ax2.set_xlabel("Sum = Amount of days since 2020-11-27")
    ax2.set_ylabel("SUM = total GBP liabilites +0%+")

    #percentageProfit
    titlePerc = 'Percentage Profit: '+str(percentageProfit)+''
    percentage = [now,today,percentageProfit]
    df3 = pd.read_csv('percentage.csv')
    df3.loc[len(df3)] = percentage
    # df3.to_csv('percentage.csv',index = False)

        #manipulation 
    df3.reset_index(inplace=True)
    df3 = df3.sort_values('index').groupby('date').tail(1)
    df3 = df3.drop(['index'], axis=1)
    print(df3)
    df3.to_csv('percentage.csv',index = False)
    df3.plot(figsize=(10,15))
    ax3 = df3.plot.area(x = 'date',title=titlePerc, rot=90, fontsize='10', grid=True,sharex=False,linewidth=0, colormap='gist_rainbow') #.tight_layout()
    ax3.set_xlabel("Sum = Amount of days since 2020-11-27")
    ax3.set_ylabel("SUM = total percentage profit +NO LOSS+")

    #save graphs
    fig = ax.get_figure()
    fig.savefig('assets.pdf', bbox_inches = "tight")
    fig2 = ax2.get_figure()
    fig2.savefig('liabilities.pdf', bbox_inches = "tight")
    fig3 = ax3.get_figure()
    fig3.savefig('percentage.pdf', bbox_inches = "tight")

    ##MERGE PDF'S INTO ONE MAIN.PDF 
 
    # Open the files that have to be merged one by one
    pdf1File = open('assets.pdf', 'rb')
    pdf2File = open('liabilities.pdf', 'rb')
    pdf3File = open('percentage.pdf', 'rb')
    
    # Read the files that you have opened
    pdf1Reader = PyPDF2.PdfFileReader(pdf1File)
    pdf2Reader = PyPDF2.PdfFileReader(pdf2File)
    pdf3Reader = PyPDF2.PdfFileReader(pdf3File)
    
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
    
    # Now that you have copied all the pages in both the documents, write them into the a new document
    pdfOutputFile = open('main.pdf', 'wb')
    pdfWriter.write(pdfOutputFile)
    
    # Close all the files - Created as well as opened
    pdfOutputFile.close()
    pdf1File.close()
    pdf2File.close()
    pdf3File.close()

    #current pie chart of assets+sub(profit)/liabilities+sub(availableliabilites)/cash

    #plt.show()

    #data science - what stack leads to most increase correlation gradient to ratio to find optimal ratio for increase (affected by adding cash and how frequencly you but once adding cash)
if __name__ == "__main__":
    main()