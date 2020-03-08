# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 08:54:13 2020

@author: 27452
"""

#utf-8
from selenium import webdriver
#from selenium.webdriver.common.action_chains import ActionChains
#import re
import time
import datetime
import csv
#import codecs
import pymysql
 
 
 
# 设置谷歌驱动器的环境
options = webdriver.ChromeOptions()
# 设置chrome不加载图片，提高速度
options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
# 创建一个谷歌驱动器
browser = webdriver.Chrome(options=options,executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')#executable_path是驱动器chromedriver的路径
 
browser.minimize_window()#最小化窗口，方便输入要检索的页数和关键词
 

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36"}
url="https://news.qq.com//zt2020/page/feiyan.htm"

def feiyan_spider():
    now = datetime.datetime.now()
    month = now.month
    day = now.day
    data_time = str(month) + "." +str(day)
    colora = "rgb(83,6,6)"
    colorb = "rgb(100,30,30)"
    colorc = "rgb(120,40,40)"
    colord = "rgb(190,130,130)"
    colorf = "rgb(195,180,180)"
    
    browser.get(url)
    time.sleep(10)
    coon = pymysql.connect(host = "localhost",
        user ="root",
        password ="",
        db ="one",)

    #省市数据
    sqlBa = "TRUNCATE TABLE one.datab"
    curBa = coon.cursor()
    curBa.execute(sqlBa)
    coon.commit()
    
    for i in range(1,35):
        
        xpath = '//*[@id="listWraper"]/table[2]/tbody['+str(i)+']/tr[1]/'
        xpath_name=xpath+'th/span'
        xpath_confirm=xpath+'td[2]'
        xpath_heal=xpath+'td[3]'
        xpath_dead=xpath+'td[4]'
        #//*[@id="listWraper"]/table[2]/tbody[1]/tr[1]/td[2]
        
                    
        location = browser.find_elements_by_xpath(xpath_name)[0].text
        confirmed = browser.find_elements_by_xpath(xpath_confirm)[0].text
        cured = browser.find_elements_by_xpath(xpath_heal)[0].text
        dead = browser.find_elements_by_xpath(xpath_dead)[0].text
        
        if int(confirmed)<10:
            color = colorf
        elif 100<int(confirmed)<1000:
            color = colord
        elif 1000<int(confirmed)<5000:
            color = colorc
        elif 5000<int(confirmed)<10000:
            color = colorb
        elif int(confirmed)>10000:
            color = colora
        
        sqlB = "INSERT INTO one.datab(location,confirmed,cured,dead,time,color) VALUES (%s,%s,%s,%s,%s,%s)"
        curB = coon.cursor()
        curB.execute(sqlB,(location,confirmed,cured,dead,data_time,color))
        coon.commit()
        
        #全国数据
    with open('C:\\HTML\\data/'+str(now.date())+'.csv', 'a', encoding='gb2312', newline='') as csvfile:#'改为你的路径'+str(now.date())+'.csv'
        writer = csv.writer(csvfile)#数据保存
 
        xpath1='//*[@id="app"]/div[2]/div[2]/div[1]/div[2]/div[1]/div[2]'#累计确诊
        xpath2='//*[@id="app"]/div[2]/div[2]/div[1]/div[2]/div[2]/div[2]'#累积治愈
        xpath3='//*[@id="app"]/div[2]/div[2]/div[1]/div[2]/div[3]/div[2]'#累计死亡
        xpath4='//*[@id="app"]/div[2]/div[2]/div[1]/div[2]/div[4]/div[2]'#现有确诊
        xpath5='//*[@id="app"]/div[2]/div[2]/div[1]/div[2]/div[5]/div[2]'#现有疑似
        xpath6='//*[@id="app"]/div[2]/div[2]/div[1]/div[2]/div[6]/div[2]'#重症
        xpathHB = '//*[@id="listWraper"]/table[2]/tbody[1]/tr[1]/td[2]'#HB累计确诊
 
        icba_confirm=browser.find_element_by_xpath(xpath1)#累计确诊
        icbar_cure=browser.find_element_by_xpath(xpath2)#累积治愈
        icbar_dead=browser.find_element_by_xpath(xpath3)#累计死亡
        icbar_now_confirm=browser.find_element_by_xpath(xpath4)#现有确诊
        icbar_suspect=browser.find_element_by_xpath(xpath5)#现有疑似
        icba_server=browser.find_element_by_xpath(xpath6)#重症
        icba_confirm_hb=browser.find_element_by_xpath(xpathHB)
        #print(icbar_cure.text)
        #print(icbar_dead.text)
        
        #更新数据
        sqlAa = "SELECT numALL,date,numHB,numDead,numCure FROM one.dataall"
        cur = coon.cursor()
        cur.execute(sqlAa)
        data = cur.fetchall()
        data_ori_num = (data[0])[0]
        data_ori_date = (data[0])[1]
        data_ori_numHB = (data[0])[2]
        #print(data)
        data_numALl = eval(data_ori_num)
        data_numHB = eval(data_ori_numHB)
        data_date = eval(data_ori_date)
        if data_time == data_date[-1]:
            data_numALl[-1] = icba_confirm.text
            data_numHB[-1] = icba_confirm_hb.text
        elif data_time != data_date[-1]:
            data_numALl.append(icba_confirm.text)
            data_numHB.append(icba_confirm_hb.text)
            data_date.append(data_time)
        sqlAb = "UPDATE one.dataall SET date = %s,numALL = %s,numHB = %s,detailTIME = %s,numDead = %s,numCure = %s"
        cur.execute(sqlAb,(str(data_date),str(data_numALl),str(data_numHB),str(now),icbar_dead.text,icbar_cure.text))
        coon.commit()
        
        #文件保存
        writer.writerow(("全国现有确诊","累计确诊", "现有疑似病例", "现有重症","治愈人数", "死亡人数","时间"))
        #print(icbar_now_confirm.text,icba_confirm.text, icbar_suspect.text, icba_server.text,icbar_cure.text, icbar_dead.text)
        writer.writerow((icbar_now_confirm.text,icba_confirm.text, icbar_suspect.text, icba_server.text,icbar_cure.text, icbar_dead.text,now))
        print("over")
feiyan_spider()
        


''' 
def main():
    h=8
    m=0
    while True:
        now = datetime.datetime.now()
        if now.hour==h and now.minute == m:
            feiyan_spider()
        time.sleep(60)
        //*[@id="listWraper"]/table[2]/tbody[1]/tr[1]/th/span
 
 
if __name__=="__main__":
    main()
    feiyan_spider()#任何时间都可以运行
    browser.close()'''