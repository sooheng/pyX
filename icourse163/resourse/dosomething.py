# -*- coding: utf-8 -*-

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from random import randint
from webpage import Xplist

#%%
def pinglun(dr):
    sleep(randint(0,5))
    dr.find_element_by_xpath("//ul[@class='j-unitslist unitslist f-cb']/li[2]").click()
    sleep(randint(0,5))
    dr.find_element_by_xpath("//span[@class='f-icon u-icon-discuss2']").click()
    sleep(randint(0,5))
    cmt16 = dr.find_elements_by_xpath('//div[@style="z-index: 0;"]')
    pinglun = cmt16[randint(0,10)].find_elements_by_xpath('./div/div')[1].text   
    dr.find_element_by_xpath('//iframe').click()
    sleep(randint(0,5))
    dr.find_element_by_xpath('//iframe').send_keys(pinglun)
    sleep(randint(0,5))
    dr.find_element_by_xpath("//a[text()='发表回复']").click()
    
def seeDoc(dr,wait):
    wait.until(EC.presence_of_element_located((By.XPATH, "//span[@class='f-icon u-icon-doc']")))
    ele = dr.find_element_by_xpath("//span[@class='f-icon u-icon-doc']")
    Xplist.clk(ele)
#    sleep(5)

def do(dr, wait):
#    seeDoc(dr, wait)
#    pinglun(dr)
    sleep(1)