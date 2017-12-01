
path_to_driver = "./chromedriver"
path_to_driver2 = "C:\\Program\ Files\ (x86)\\Mozilla\ Firefox\\firefox.exe"


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
uid.send_keys("admin")
pwd.send_keys("admin")
button.click()

time.sleep(1)
#Go to panel
driver.find_element_by_id('goto').click()

time.sleep(1)
driver.find_element_by_link_text('Waiting Projects').click()
time.sleep(1)
driver.find_element_by_link_text('Allocated Projects').click()
time.sleep(0.5)

#Open a project
driver.find_element_by_id('pr0').click()
