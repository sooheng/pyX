# -*- coding: utf-8 -*-
"""
Created on Mon May 14 17:36:16 2018

@author: user
"""
from selenium.common.exceptions import StaleElementReferenceException, ElementNotVisibleException

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