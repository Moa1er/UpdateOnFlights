from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

url = 'https://freebitco.in'


#browser = webdriver.Chrome(executable_path='/usr/bin/chromedriver')
browser = webdriver.Chrome(executable_path='/home/miameme/Downloads/chromedriver')
browser.get(url)

def clickOnRoll():
    browser.find_element_by_xpath("//input[@class='free_play_element new_button_style profile_page_button_style']").click()

clickOnRoll()
browser.quit()