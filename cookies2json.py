# -*- coding: utf-8 -*-
"""
Created on Sat May 12 17:14:06 2018

@author: user
"""

from selenium import webdriver
import os
from time import time, localtime, sleep
import json

chrome_options = webdriver.ChromeOptions()
abspath = os.path.abspath(r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
dr = webdriver.Chrome(abspath, chrome_options=chrome_options)
url = "http://www.icourse163.org/learn/UJS-1002011030?tid=1002784011"
dr.get(url)
dr.implicitly_wait(5)
#%%

#%%
cookies = dr.get_cookies()
with open('./cookies163.json', 'w') as fp:
    json.dump(cookies, fp)