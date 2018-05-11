# -*- coding: utf-8 -*-
"""
Created on Wed May  9 21:05:01 2018

@author: user

"""
import requests
from time import sleep, time, localtime
from requests import HTTPError
import pickle

# data
with open('./lyqZH.pkl', 'rb') as fp:
    zhangHao, mima  = pickle.load(fp)
#pa = {
#        '路由器状态':{'code':2,'asyn':1}
#        '换宽带账号':{'code':1,'asyn':0},
#        '认证':{'code':7,'asyn':0},
#}
urlId = ''
url = 'http://falogin.cn/'

# function
def secEncode(a, b="RDpbLfCPsJZ7fiv", c="yLwVl0zKqws7LgKPRQ84Mdt708T1qQ3Ha7xv3H7NyU84p21BriUWBU43odz3iP4rBL3cD02KZciXTysVXiV8ngg6vL48rPJyAUw0HurW20xqxv9aYb4M9wK1Ae0wlro510qXeU07kV57fQMc8L6aLgMLwygtc0F10a0Dg70TOoouyFhdysuRMO51yY5ZlOZZLEal1h0t9YQW0Ko7oBwmCAHoic4HYbUyVeU3sfQ1xtXcPcf1aT303wAQhv66qzW"):    
    '''路由器认证加密函数'''
    d = ''; k = 187; l = 187; f = len(a); h = len(b); m = len(c)
    if f > h:
        e = f
    else:
        e = h
    for g in range(e):
        l = k = 187
        if g >= f:
            l = ord(b[g])
        elif g >= h:
            k = ord(a[g])
        else:
            k = ord(a[g])
            l = ord(b[g])
        d = d + c[(k^l) % m]
    return d

def authId(r):
    '''路由器认证id计算函数'''
    key = secEncode(a = mima)
    infoli = r.text.splitlines()
    return secEncode(infoli[3], key, infoli[4])

def postHtml(url, params, data=None):
    '''post'''
    global urlId
    params['id'] = urlId
    try:
        r = requests.post(url, params= params, data= data)
        r.raise_for_status()
        print(r.url, r.status_code)
    except HTTPError as e:
        print('认证过期,重新认证', e)
        urlId = authId(r)
        
        print('开始认证')
        params['code'] = 7; params['asyn']= 0
        params['id'] = urlId
        try:
            r2 = requests.post(url, params= params)
            r2.raise_for_status()
            print(r2.url, r2.status_code)
        except:
            print('认证失败')
        finally:
            return ''    
    return r
# 过程
def trafStat():
    '''获取路由器状态'''
    for i in range(50):
        r = postHtml(url, params={'code':2,'asyn':1}, data='13')   
        sleep(2)
        
def chgZH():
    '''换宽带账号'''
    today = localtime(time())[2]
    who = (today-1) // 10
    r = ''
    while not r:
        r = postHtml(url, params={'code':1,'asyn':0}, data=zhangHao[who])
    print(r.text, '00000表示成功')
#trafStat()
chgZH()