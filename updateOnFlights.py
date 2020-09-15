from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup # BeautifulSoup is in bs4 package 
import requests

import pandas as pd

import time
import datetime

import smtplib
from email.mime.multipart import MIMEMultipart
from email.message import EmailMessage

url = 'https://www.flylevel.com/'

classEnabled = "datepicker-day-button day range-start selected"
classDisabled = "datepicker-day-button day disabled"

#browser = webdriver.Chrome(executable_path='/usr/bin/chromedriver')
browser = webdriver.Chrome(executable_path='/home/miameme/Downloads/chromedriver')
browser.get(url)

content = requests.get(url)
soup = BeautifulSoup(content.text, 'html.parser')

def triggerMenuDestination():
    browser.find_element_by_xpath("//app-flight-input[@class='searcher-input destination separator']").click()

def arrival_country_chooser(arrival_country):
    fly_to = browser.find_element_by_xpath("//input[@id='inputDestination']")
    fly_to.clear()
    time.sleep(0.5)
    fly_to.send_keys(arrival_country)
    time.sleep(0.5)
    browser.find_element_by_xpath("//app-station-item[@class='item list-station']").click() #Choosing the first item
    time.sleep(0.5)

def triggerMenuDate():
    browser.find_element_by_xpath("//app-flight-date-input[@class='searcher-input']").click()
    time.sleep(0.5)

def triggerNextMonths():
    browser.find_element_by_xpath("//span[@class='icon-chevron-right arrowforward']").click()
    time.sleep(0.5)
    browser.find_element_by_xpath("//span[@class='icon-chevron-right arrowforward']").click()
    time.sleep(0.5)

def isAvailable():
    available = browser.find_elements_by_xpath("//span[@class='datepicker-day-button day disabled']")
    if len(available) < 62 :
        sendEmail("ALERTE ROUGE, ALERTE ROUGE, ceci n'est pas un exercice.")
    else :
        sendEmail("ALERTE... GREEN LOL")

def connectMail():
    global server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login("aghines.gasselin@gmail.com", "dx&334@3##ojQ!")

def sendEmail(etatVol) :
    global message
    message = EmailMessage()
    message.set_content(etatVol)
    message['Subject'] = 'Update availability of level\'s flights'
    message['From'] = 'aghines.gasselin@gmail.com'
    message['to'] = 'twoswaglol.law@gmail.com'

    server.send_message(message)

triggerMenuDestination()           #OK
arrival_country_chooser("Paris")   #OK
triggerMenuDate()                  #OK
triggerNextMonths()                #OK en full screen...
connectMail()                      #OK
isAvailable()                      #OK mais bon pas tres clean on va pas se le cacher
browser.quit()