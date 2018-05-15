# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 14:14:53 2018

@author: user
"""


from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, ElementNotVisibleException
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from random import randint
from modul_icourse163 import Xplist, Page

#%%
def pinglun(dr):
    sleep(randint(0,5))
    dr.find_element_by_xpath("//ul[@class='j-unitslist unitslist f-cb']/li[2]").click()
    sleep(randint(0,5))
    dr.find_element_by_xpath("//span[@class='f-icon u-icon-discuss2']").click()
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
    
def seeDoc(dr,wait):
    wait.until(EC.presence_of_element_located((By.XPATH, "//ul[@class='j-unitslist unitslist f-cb']/li[3]")))
    try:
        sleep(randint(0,5))
        dr.find_element_by_xpath("//ul[@class='j-unitslist unitslist f-cb']/li[3]").click()
        dr.find_element_by_xpath("//span[@class='f-icon u-icon-doc']").click()
    except:
        print('doc无法点击，停1秒再点')
        sleep(1)
        dr.find_element_by_xpath("//ul[@class='j-unitslist unitslist f-cb']/li[3]").click()
        dr.find_element_by_xpath("//span[@class='f-icon u-icon-doc']").click()
    sleep(18)

def do_something(dr, wait):
    print('进入页面', j+1, i+1)
    cur_url.append((j+1, i+1, p.dr.current_url))
    seeDoc(dr, wait)
    pinglun(dr)
#4-4
#%%
p = Page() #启动浏览器
url = "http://www.icourse163.org/learn/UJS-1002011030?tid=1002784011"
p.setCookies(url) #设置cookies
p.dr.get(url+ '#/learn/content?type=detail&id=1003843713&cid=1004685430') #访问网页
cur_url = []
#%%
#页面内找元素
cont2 = Xplist(p.dr, "//div[@class='up j-up f-thide']") # 0是章， 1是节
chap12 = Xplist(p.dr, "//div[@class='f-fl j-chapter']//div[@class='f-thide list']")
lesson = Xplist(p.dr, "//div[@class='f-fl j-lesson']//div[@class='f-thide list']")
for j in range(5,12):
    try:
        cont2.upEles()
        chap12.clk2upEles(cont2.alist[0])
        Xplist.clk(chap12.alist[j], cont2.alist[0])
    except:
        print('1')
        sleep(1)
        cont2.upEles()
        chap12.clk2upEles(cont2.alist[0])
        Xplist.clk(chap12.alist[j], cont2.alist[0])
    
    
    cont2.upEles()
    lesson.clk2upEles(cont2.alist[1])
    for i in range(len(lesson.alist)):
        try:
            cont2.upEles()
            lesson.clk2upEles(cont2.alist[1])
            Xplist.clk(lesson.alist[i], cont2.alist[1])
        except :
            print('2')
            sleep(1)
            cont2.upEles()
            lesson.clk2upEles(cont2.alist[1])
            Xplist.clk(lesson.alist[i], cont2.alist[1])
        
        do_something(p.dr, p.wait)
p.keeplogs()
p.updataCookies()