# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 14:14:53 2018

@author: user
"""

from webpage import Xplist, Page
from dosomething import do

#%%
p = Page() #启动浏览器
url = "http://www.icourse163.org/learn/UJS-1002011030?tid=1002784011"
p.dr.get(url+ '#/learn/content?type=detail&id=1003843713&cid=1004685430') #访问网页
#%%
#页面内找元素xpath规则绑定
cont2 = Xplist(p.dr, "//div[@class='up j-up f-thide']") # 0是章， 1是节
chap12 = Xplist(p.dr, "//div[@class='f-fl j-chapter']//div[@class='f-thide list']")
lesson = Xplist(p.dr, "//div[@class='f-fl j-lesson']//div[@class='f-thide list']")
#开始查找
for j in range(6,12):
    cont2.upEles()
    chap12.clk2upEles(cont2.alist[0])
    Xplist.clk(chap12.alist[j], cont2.alist[0])
       
    cont2.upEles()
    lesson.clk2upEles(cont2.alist[1])
    for i in range(len(lesson.alist)):
        cont2.upEles()
        lesson.clk2upEles(cont2.alist[1])
        Xplist.clk(lesson.alist[i], cont2.alist[1])
        
        do(p.dr, p.wait) #找到后，要做的事情
#%%
p.keeplogs()
p.dr.close()
p.dr = None
p.wait = None
