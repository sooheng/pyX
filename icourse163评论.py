# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 14:14:53 2018

@author: user
"""

from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException, ElementNotVisibleException
import os
from time import time, localtime, sleep
import json
from random import randint
#%%
chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument(r"user-data-dir=C:\Users\user\AppData\Local\Google\Chrome\User Data")
#chrome_options.add_argument('--headless')
abspath = os.path.abspath(r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
dr = webdriver.Chrome(abspath, chrome_options=chrome_options)
dr.implicitly_wait(10)
#%%
url = "http://www.icourse163.org/learn/UJS-1002011030?tid=1002784011"
dr.get(url)
dr.delete_all_cookies()# 删除第一次建立连接时的cookie
with open('./cookies163.json', 'r') as fp:# 读取登录时存储到本地的cookie
    cookies = json.load(fp)
for cok in cookies:
    dr.add_cookie(cok)
dr.get(url)# 再次访问页面，便可实现免登陆访问
dr.get(url+ '#/learn/content?type=detail&id=1003843713&cid=1004685430')
#%% 9-2

class EmptylistException(Exception):
    def __init__(self,err='找不到元素,列表是空的'):
        Exception.__init__(self,err)
     
class xplist(list):
    '''
    生成WebElement标签元素的列表,列表附带有标签的上级标签cont,查找使用的xpath,
    注意对xplist排序，切片后，由于是调用list的方法，所以会返回list类型。
    '''
    def __init__(self, cont, xpath):
        '''上级标签cont,查找使用的xpath'''
        self.cont = cont
        self.xpath = xpath
        __list = self.cont.find_elements_by_xpath(self.xpath)
        super(xplist,self).__init__(__list)
    
    def upEles(self):
        '''重新生成WebElement标签元素的列表'''
        print('更新eles')
        __xplist = xplist(self.cont, self.xpath)
        return __xplist      
    
    def findEles(self,contclk):
        try:        
            eles = xplist(self.cont, self.xpath)
            if bool(eles):
                raise EmptylistException()
        except EmptylistException:
            contclk.click()
            eles = xplist(self.cont, self.xpath)
            if bool(eles):
                print(contclk,'点开还是找不到！')
            else:
                print('点开cont找到元素')
        return eles

    
#%%
def clk(ele, contclk=None):
    '''不可见的元素,点击后使它可见'''
    try:
        ele.click()
    except ElementNotVisibleException:
        contclk.click()
        ele.click()
        print('点开cont点开元素')



def ping():
    dr.find_element_by_xpath(".//span[@class='f-icon u-icon-discuss2']").click()
    dr.find_element_by_xpath("//a[text()='发表回复']").click() #先点回复，渲染iframe
    sleep(randint(0,5))
    dr.find_element_by_xpath(".//span[@class='f-icon u-icon-discuss2']").click()
    cmt16 = dr.find_elements_by_xpath('//div[@style="z-index: 0;"]')
    sleep(randint(0,5))
    pinglun = cmt16[randint(0,10)].find_elements_by_xpath('./div/div')[1].text
    sleep(randint(0,5))
    print(pinglun)
    dr.find_element_by_xpath('//iframe').send_keys(pinglun)
    sleep(randint(0,5))
    dr.find_element_by_xpath("//a[text()='发表回复']").click()
    print('发表')
    sleep(randint(0,5))

#%%

cont2 = xplist(dr, "//div[@class='up j-up f-thide']")
chap12 = xplist(dr, "//div[@class='up j-up f-thide']/..//div[@class='f-thide list']")
chap12.findEles(cont2[0])

for j in range(12):
    try:
        clk(chap12[j], cont2[0])
    except StaleElementReferenceException:
        cont2 = cont2.upEles()
        chap12 = chap12.upEles()
        print('更新章节')
        clk(chap12[j], cont2[0])
#%%
    lesson = findEles(cont2[1], dr, "//div[@class='up j-up f-thide']/..//div[@class='f-thide list']")
    for i in range(len(lesson)):
        try:
            clk(lesson[i], cont2[1])
        except StaleElementReferenceException:
            cont2 = cont2.upEles()
            lesson = lesson.upEles()
            print('更新课程')
            clk(lesson[i], cont2[1])
        print('进入页面')
            
        
#%%  
cont2 = dr.find_elements_by_xpath("//div[@class='up j-up f-thide']")
cont2[0].click()
chap12 = cont2[0].find_elements_by_xpath("/.//div[@class='f-thide list']")
for j in range(8,12):
    try:    
        clk(chap12[j], cont2[0])
    except:
        cont2 = dr.find_elements_by_xpath("//div[@class='up j-up f-thide']")
        cont2[0].click()
        chap12 = cont2[0].find_elements_by_xpath("/.//div[@class='f-thide list']")
        clk(chap12[j], cont2[0])  
    try:
        lesson = cont2[1].find_elements_by_xpath("./../div/div")
    except:
        cont2 = dr.find_elements_by_xpath("//div[@class='up j-up f-thide']")
        cont2[1].click()
        lesson = cont2[1].find_elements_by_xpath("./../div/div")   
    for i in range(len(lesson)):
        try:
            clk(lesson[i], cont2[1])
        except:
            cont2 = dr.find_elements_by_xpath("//div[@class='up j-up f-thide']")
            cont2[1].click()
            lesson = cont2[1].find_elements_by_xpath("./../div/div")
            clk(lesson[i], cont2[1])
        print(lesson[i].text)
#        ping()