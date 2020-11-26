import time
from datetime import date

import pandas as pd
from IPython.core.display import HTML

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from secrets import *
import json


#Loads the driver
def load_driver():
    chrome_options = Options()

    #chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options = chrome_options)

    return driver

#Login page
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

    print(total)
    profitData = profit.split()

    netProfit = profitData[0][2:len(profitData[0])-3].replace(',','')
    print(netProfit)
    pecentageProfit = profitData[1][1:len(profitData[1])-1].replace('%','')
    print(pecentageProfit)

    cash = driver.find_element_by_xpath("//*[@id='app']/div[1]/div[1]/div/div[2]/div[1]/div/span[2]")
    cash = cash.text
    cash = int(cash[1:len(cash)-3].replace(',',''))-int(total)
    print(cash)
    
    return total
        
def plot():
    pass
    
def main():
    today = date.today()
    url = "https://live.trading212.com/beta"

    username = "connorsforsyth@gmail.com"
    password = password212

    driver = load_driver()

    # while True: keep updating
    login212(driver, url, username, password)
    time.sleep(20)
    data212 = getdata212(driver)
    # loginPro
    # time.sleep(20)
    # dataPro = getdataPro()
    driver.get_screenshot_as_file("screenshot.png")
    # plot data
    
    
    

    # driver.close()
    driver.quit()

if __name__ == "__main__":
    main()