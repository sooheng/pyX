# -*- coding: utf-8 -*-
"""
Created on Mon May 14 17:36:16 2018

@author: user
"""
from selenium.common.exceptions import StaleElementReferenceException, ElementNotVisibleException
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
import json
#%%
#exmples:
#wait.until(EC.presence_of_element_located((By.XPATH, '/html')))
#wait.until(lambda ele:ele.is_displayed())
#chrome_options.add_argument(r"user-data-dir=C:\Users\user\AppData\Local\Google\Chrome\User Data")
#chrome_options.add_argument('--headless')
#%%
class Page(object):
    '''多个页面page共享一个浏览器dr'''
    dr = None
    wait = None
    
    def __init__(self):
        if not (self.dr and self.wait):
            self.startup()
            
    @classmethod
    def startup(cls):     
        chrome_options = webdriver.ChromeOptions()   
        abspath = 'C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe'
        dr = webdriver.Chrome(abspath, chrome_options=chrome_options)
        dr.implicitly_wait(10)
        wait = WebDriverWait(dr, 10) #等待的最大时间10
        cls.dr = dr
        cls.wait = wait
        return dr, wait
    
    @classmethod
    def setCookies(cls, url):
        cls.dr.get(url)
        cls.dr.delete_all_cookies()
        host = cls.dr.current_url.split('/')[2]
        with open('./{0}.json'.format(host), 'r')as fp:
            cookies = json.load(fp)
        for cook in cookies:
            cls.dr.add_cookie(cook)
        cls.dr.get(url)# 再次访问页面，便可实现免登陆访问
    
    @classmethod
    def updataCookies(cls):
        cookies = cls.dr.get_cookies()
        host = cls.dr.current_url.split('/')[2]
        with open('./{0}.json'.format(host), 'w') as fp:
            json.dump(cookies, fp)
            
    @classmethod
    def keeplogs(cls):
        logs = cls.dr.get_log('browser')
        host = cls.dr.current_url.split('/')[2]
        with open('./logbr/{0}.json'.format(host), 'w') as fp:
            json.dump(logs, fp)
        logs_driver = cls.dr.get_log('driver')
        with open('./logdr/{0}.json'.format(host), 'w') as fp:
            json.dump(logs_driver, fp)
    

#%%
class EmptylistException(Exception):
    def __init__(self,err='找不到元素,列表是空的'):
        Exception.__init__(self,err)
        
class Xplist(object):
    '''
    生成WebElement标签元素的列表,列表附带有标签的上级标签cont,查找使用的xpath,
    注意对xplist排序，切片后，由于是调用list的方法，所以会返回list类型。
    '''
    def __init__(self, cont, xpath):
        '''上级标签cont,查找使用的xpath'''
        self.cont = cont
        self.xpath = xpath
        
    def upEles(self):
        '''直接更新标签元素的列表'''
        self.alist = self.cont.find_elements_by_xpath(self.xpath)
        if not bool(self.alist):
            print('更新eles失败，尝试点开contclk')
            raise EmptylistException()
            
    def clk2upEles(self,contclk):
        '''点击后更新标签元素的列表'''
        if not contclk.is_displayed():
            contclk.click()
        try:
            contclk.click()
            self.upEles()        
        except EmptylistException:
            contclk.click()
            try:
                self.upEles()
            except EmptylistException:
                print(contclk,'点开还是更新失败！')
    
    @staticmethod
    def clk(ele, contclk=None):
        '''不可见的元素,点击后使它可见'''
        if not ele.is_displayed():
            contclk.click() 
        try:
            ele.click()
        except ElementNotVisibleException:
            contclk.click()
            ele.click()
            print('元素还是不可见')