from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

import pandas as pd

import time
import datetime

import smtplib
from email.mime.multipart import MIMEMultipart

url = 'https://www.flylevel.com/'

classEnabled = "datepicker-day-button day range-start selected"
classDisabled = "datepicker-day-button day disabled"

browser = webdriver.Chrome(executable_path='/home/miameme/Downloads/chromedriver')
browser.get(url)


def triggersTheMenu():
    browser.find_element_by_xpath("//app-flight-input[@class='searcher-input destination separator']").click()

def arrival_country_chooser(arrival_country):
    fly_to = browser.find_element_by_xpath("//input[@id='inputDestination']").clear()
    time.sleep(0.5)
    fly_to.send_keys(arrival_country)
    time.sleep(0.5)
    browser.find_element_by_xpath("//app-station-item[@class='item list-station']").click() #Choosing the first item

#def choosingDate() :
    

triggersTheMenu()
arrival_country_chooser("Paris")