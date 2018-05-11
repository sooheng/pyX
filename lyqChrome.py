# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 14:14:53 2018

@author: user
"""

from selenium import webdriver
import os
from time import time, localtime
import pickle
import re

with open('./lyqZh.pkl', 'rb') as fp:
        zhangHao, mima  = pickle.load(fp)

def changePhoneNum(phoneNum, password= '123456'):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    abspath = os.path.abspath(r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')  
    try:
        dr = webdriver.Chrome(abspath, chrome_options=chrome_options)
        dr.get("http://192.168.1.1")  
    
        lgpwd = dr.find_element_by_xpath("//input[@id='lgPwd']")
        lgpwd.send_keys(mima)
        ensure = dr.find_elements_by_css_selector('.btnR')[0]
        ensure.click()
        dr.implicitly_wait(5)#页面跳转时间
        
        wlan = dr.find_element_by_xpath("//h2[text()='上网设置']")
        wlan.click()
        name = dr.find_element_by_xpath("//input[@id='name']")
        name.clear()
        name.send_keys(phoneNum + '@cmcc')
        psw = dr.find_element_by_xpath("//input[@id='psw']")
        psw.clear()
        psw.send_keys(password)
        save = dr.find_element_by_xpath("//input[@id='saveImg']")
        save.click()
    finally:
        dr.quit()
    
def main():    
    phoneNums = []
    for i in zhangHao:
        ph = re.search('\d{11}', i)
        phoneNums.append(ph.group(0))
    today = localtime(time())[2]
    whoPhone = (today-1) // 10
    if whoPhone < len(phoneNums):     
        changePhoneNum(phoneNums[whoPhone])
    return

if __name__ == '__main__':
    main()