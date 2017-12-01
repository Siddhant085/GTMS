
path_to_driver = "./chromedriver"


import os
import time
import codecs
import re
import datetime
from selenium import webdriver

url = 'localhost:5000/'
driver = webdriver.Chrome(path_to_driver)
driver.get(url)

#Login 
uid = driver.find_element_by_id('u_id')
pwd = driver.find_element_by_id('password_u')
button = driver.find_element_by_id('loginBtn')
uid.send_keys("constructor")
pwd.send_keys("constructor")
time.sleep(0.2)
button.click()

time.sleep(1)
#Go to panel
driver.find_element_by_id('goto').click()

time.sleep(1)
driver.find_element_by_css_selector('#proj_bid > tbody > tr').click()
time.sleep(1)

#Open a project
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
driver.find_element_by_id('wd').send_keys('24')
driver.find_element_by_id('desc').send_keys('No delays! still working!')
time.sleep(0.5)

driver.find_element_by_id('updbut').click()
