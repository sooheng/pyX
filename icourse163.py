# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 14:14:53 2018

@author: user
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, ElementNotVisibleException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
import json
from random import randint
from modul_icourse163 import Xplist as xplist
#%%   
def openurl(url):
    dr.get(url)
    dr.delete_all_cookies()
    with open('./cookies163.json', 'r')as fp:
        cookies = json.load(fp)
    for cok in cookies:
        dr.add_cookie(cok)
    dr.get(url)# 再次访问页面，便可实现免登陆访问
    dr.get(url+ '#/learn/content?type=detail&id=1003843713&cid=1004685430')
   
def upCookies():
    cookies = dr.get_cookies()
    with open('./cookies163.json', 'w') as fp:
        json.dump(cookies, fp)
    
def startup():
            
    chrome_options = webdriver.ChromeOptions()   
    abspath = 'C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe'
    dr = webdriver.Chrome(abspath, chrome_options=chrome_options)
    dr.implicitly_wait(10)
    wait = WebDriverWait(dr, 10) #等待的最大时间10    
    return dr, wait

#%%
def clk(ele, contclk=None):
        '''不可见的元素,点击后使它可见'''
        if not ele.is_displayed():
            contclk.click() 
        try:
            ele.click()
        except ElementNotVisibleException:
            contclk.click()
            wait.until(lambda ele:ele.is_displayed())
            ele.click()
            print('元素还是不可见')

def ping():
    dr.find_element_by_xpath("//ul[@class='j-unitslist unitslist f-cb']/li[2]").click()
    sleep(randint(0,5))
    cmt16 = dr.find_elements_by_xpath('//div[@style="z-index: 0;"]')
    pinglun = cmt16[randint(0,10)].find_elements_by_xpath('./div/div')[1].text
    print('pinglun')    
    dr.find_element_by_xpath('//iframe').click()
#    dr.switch_to.frame(dr.find_element_by_xpath('//iframe'))
    sleep(randint(0,5))
    dr.find_element_by_xpath('//iframe').send_keys(pinglun)
    sleep(randint(0,5))
    dr.find_element_by_xpath("//a[text()='发表回复']").click()
    print('发表')

def do_something():
    wait.until(EC.presence_of_element_located((By.XPATH, "//ul[@class='j-unitslist unitslist f-cb']/li[3]")))
    try:
        dr.find_element_by_xpath("//ul[@class='j-unitslist unitslist f-cb']/li[3]").click()
    except:
        print('doc')
        sleep(1)
        dr.find_element_by_xpath("//ul[@class='j-unitslist unitslist f-cb']/li[3]").click()
#        ping(True)
#        ping(True)
#%%
dr, wait = startup()
url = "http://www.icourse163.org/learn/UJS-1002011030?tid=1002784011"
openurl(url)
cur_url = []

cont2 = xplist(dr, "//div[@class='up j-up f-thide']") # 0是章， 1是节
chap12 = xplist(dr, "//div[@class='f-fl j-chapter']//div[@class='f-thide list']")
lesson = xplist(dr, "//div[@class='f-fl j-lesson']//div[@class='f-thide list']")
#%%
for j in range(12):
    try:
        cont2.upEles()
        chap12.clk2upEles(cont2.alist[0])
        xplist.clk(chap12.alist[j], cont2.alist[0])
    except:
        print('无法更新章节元素')
        raise
    cont2.upEles()
    lesson.clk2upEles(cont2.alist[1])
    for i in range(len(lesson.alist)):
        try:
            cont2.upEles()
            lesson.clk2upEles(cont2.alist[1])
            xplist.clk(lesson.alist[i], cont2.alist[1])
        except:         
            print('无法更新课程元素')
            raise
        print('进入页面', j+1, i+1)
        cur_url.append((j+1, i+1))
        cur_url.append(dr.current_url)
        do_something()
dr.close()
#%%  
#cont2 = dr.find_elements_by_xpath("//div[@class='up j-up f-thide']")
#cont2[0].click()
#chap12 = cont2[0].find_elements_by_xpath("/.//div[@class='f-thide list']")
#for j in range(8,12):
#    try:    
#        clk(chap12[j], cont2[0])
#    except:
#        cont2 = dr.find_elements_by_xpath("//div[@class='up j-up f-thide']")
#        cont2[0].click()
#        chap12 = cont2[0].find_elements_by_xpath("/.//div[@class='f-thide list']")
#        clk(chap12[j], cont2[0])  
#    try:
#        lesson = cont2[1].find_elements_by_xpath("./../div/div")
#    except:
#        cont2 = dr.find_elements_by_xpath("//div[@class='up j-up f-thide']")
#        cont2[1].click()
#        lesson = cont2[1].find_elements_by_xpath("./../div/div")   
#    for i in range(len(lesson)):
#        try:
#            clk(lesson[i], cont2[1])
#        except:
#            cont2 = dr.find_elements_by_xpath("//div[@class='up j-up f-thide']")
#            cont2[1].click()
#            lesson = cont2[1].find_elements_by_xpath("./../div/div")
#            clk(lesson[i], cont2[1])
#        print(lesson[i].text)
#        ping()