from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

import pickle
import pprint
import time


uName = "twoswaglol.law@gmail.com"
pwd = "YmuKXOIPnhAfit8y"

url = 'https://freebitco.in'


#browser = webdriver.Chrome(executable_path='/usr/bin/chromedriver')
browser = webdriver.Chrome(executable_path='/home/miameme/Downloads/chromedriver')
# browser.get(url)

def clickOnRoll():
    browser.find_element_by_xpath("//input[@class='free_play_element new_button_style profile_page_button_style']").click()

def save_cookies(driver, location):
    pickle.dump(driver.get_cookies(), open(location, "wb"))


def load_cookies(driver, location, url=None):

    cookies = pickle.load(open(location, "rb"))
    driver.delete_all_cookies()
    # have to be on a page before you can add any cookies, any page - does not matter which
    driver.get("https://google.com" if url is None else url)
    for cookie in cookies:
        if isinstance(cookie.get('expiry'), float):#Checks if the instance expiry a float 
            cookie['expiry'] = int(cookie['expiry'])# it converts expiry cookie to a int 
        driver.add_cookie(cookie)

def connection():
    uNameForm = browser.find_element_by_xpath("//input[@id='login_form_btc_address']")
    #pwdForm = browser.find_element_by_xpath("//input[@id='login_form_password']")

    uNameForm.click()
    time.sleep(0.5)
    uNameForm.clear()
    time.sleep(0.5)
    uNameForm.send_keys(uName)
    time.sleep(0.5)

    # pwdForm.click()
    # time.sleep(0.5)
    # pwdForm.clear()
    # time.sleep(0.5)
    # pwdForm.send_keys(pwd)
    # time.sleep(0.5)



#connection()
#save_cookies(browser, "/home/miameme/Cookies/cookies.txt")
load_cookies(browser, "/home/miameme/Cookies/cookies.txt", None)
browser.get(url)
clickOnRoll()
time.sleep(5)
browser.quit()