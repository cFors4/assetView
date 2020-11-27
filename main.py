import time
from datetime import date
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from secrets import *

import csv
import pandas as pd

def load_driver():
    chrome_options = Options()

    #chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--disable-extensions")
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
    login_button = driver.find_element_by_xpath("/html/body/div[1]/section[2]/div/div/div/form/input[6]")

    login_field.clear()
    password_field.clear()
    
    login_field.send_keys(username)
    password_field.send_keys(password)
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
    #make secret
    bitcoin_api_url = 'https://www.google.com/search?q=bitcoin+price&oq=bitocin+pri&aqs=chrome.1.69i57j0i10i131i433i457j0i10i131i433l6.4397j1j4&sourceid=chrome&ie=UTF-8'
    driver.get(bitcoin_api_url)
    time.sleep(5)  
    BTC_field = driver.find_element_by_xpath('//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').text
    BTC_price = float(BTC_field.replace(',',''))
    #make secret
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
    # urlPro = "https://pro.coinbase.com/"
    #make secret
    urlGooglePro = urlPro
    
    username = "connorsforsyth@gmail.com"
    password = password212

    driver = load_driver()

    # while True: keep updating
    #TRADING212

    try:
        login212(driver, url212, username, password)
        time.sleep(20)
        total212,netProfit212,pecentageProfit212,cash212 = getdata212(driver)
    except:
        print("no internet")

    #BITCOIN
    totalPro,netProfitPro,pecentageProfitPro,cashPro = getdataPro(driver,urlGooglePro,urlPro9)

    #ETORO??
    #nationwide?? debt
    totalLiabilites = -3000

    print(total212,totalPro)
    totalAssets = total212+totalPro
    netProfit = netProfit212+netProfitPro
    pieSlice212 = total212/totalAssets
    pieSlicePro = totalPro/totalAssets
    percentageProfit = netProfit/totalAssets
    netCash = cash212+cashPro

    driver.close()
    driver.quit()

    # store data - ratios cash to assets to liabilites?
    store = [now,today,totalAssets,netProfit,percentageProfit,netCash,totalLiabilites]

    # with open('data.csv', mode='a',newline='') as data:
    #     writer = csv.writer(data)
    #     writer.writerow(store)

    df = pd.read_csv('data.csv')
    df.loc[len(df)] =store
    print(df)
    df.to_csv('data.csv',index = False)
    
    #PLOT
    #plot pie chart of assets+sub(profit)/liabilities+sub(availableliabilites)/cash
    #percentage profit over time
    #total over time


if __name__ == "__main__":
    main()