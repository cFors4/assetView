import time
from datetime import date
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
from IPython.core.display import HTML

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup
from lxml import html
from lxml import etree

from secrets import *


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

        
#Buy button
def buy():
    pass

#Sell button
def sell():
    pass
    
def main():
    today = date.today()
    url = "https://live.trading212.com/beta"

    username = "connorsforsyth@gmail.com"
    password = password212

    driver = load_driver()

    login212(driver, url, username, password)
    time.sleep(20)
    # data212 = getdata212()
    # loginPro
    # time.sleep(20)
    # dataPro = getdataPro()
    driver.get_screenshot_as_file("screenshot.png")
    # plot data
    
    # while True:
    #     time.sleep(1)
    #     print(get_ticker(driver), get_bid(driver), end = "\r", flush = True)

    driver.close()
    driver.quit()

if __name__ == "__main__":
    main()