# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 09:26:58 2020

@author: lx
"""

################################## 爬虫基本框架  ###############################

import urllib #指定URL,获取网页数据
from bs4 import BeautifulSoup #网页解析，获取数据
import re  #正则表达式，进行文字匹配
import xlwt   #进行Excel操作
import sqlite3 #通过Sqlite进行数据库操作
import os
os.getcwd()
os.chdir('C:\\Users\\lx\\Desktop')##更改路径至桌面

def getData(baseurl):
    datalist = []
    return datalist

def saveData(savepath):
    print("done!")

def main():
    #1.爬取网页并解析数据
    baseurl = "https://movie.douban.com/top250?start="
    datalist = getData(baseurl)
    #2.保存数据
    savepath = ".\\豆瓣电影Top250.xls"
    saveData(savepath)

############################ 实例：爬豆瓣电影数据  ##############################
#得到指定一个URL的网页内容
def askURL(url):
    head = { #模拟浏览器头部信息,向豆瓣服务器发送信息
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362"
    }
             #用户代理,表示告诉豆瓣服务器,我们是什么类型的机器,浏览器(本质上是告诉浏览器,我们可以接受什么水平的数据)
    request = urllib.request.Request(url,headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        print(html)
    except urllib.erroe.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
    return html

# askURL("https://movie.douban.com/top250?start=")

#网址信息
baseurl = "https://movie.douban.com/top250?start="

#影片详情链接的规则
findLink = re.compile(r'<a href="(.*?)">') #创建正则表达式对象，表示规则（字符串的模式）
#影片图片
findImgSrc = re.compile(r'<img.*src="(.*?)"',re.S) #re.S让换行符包含在字符中
#影片片名
findTitle = re.compile(r'<span class="title">(.*)</span>')
#影片评分
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
#找到评价人数
findJudge = re.compile(r'<span>(\d*)人评价</span>')
#找到概况
findIng = re.compile(r'<span class="inq">(.*)</span>')
#找到影片相关内容
findBd = re.compile(r'<p class="">(.*?)</p>',re.S)


def getData(baseurl):
    datalist = []
    for i in range(0,10):  #调用获取页面信息的函数，十次
        url = baseurl + str(i*25)
        html = askURL(url) #保存获取到的网页源码
        
        #逐一解析数据
        soup = BeautifulSoup(html,"html.parser")
        for item in soup.find_all('div',class_="item"): #查找符合要求的字符串，形成列表
            #print(item) #测试：查看电影item全部信息
            data = [] #保存一部电影的所有信息
            item = str(item)
            
            link = re.findall(findLink,item)[0] #re库用来通过正则表达式查找指定的字符串
            data.append(link)                   #添加链接
            
            imgSrc = re.findall(findImgSrc,item)[0]
            data.append(imgSrc)                 #添加图片
            
            titles = re.findall(findTitle,item) #片名可能只有一个中文名,没有外国名
            if(len(titles)==2):
               ctitle = titles[0]                 #添加中文名
               data.append(ctitle)
               otitle = titles[1].replace("/","") #去掉无关的符号
               data.append(otitle)                #添加外国名
            else:
               data.append("")                      #外国名字留空
               
            rating = re.findall(findRating,item)[0]
            data.append(rating)                   #添加评分
            
            judgeNum = re.findall(findJudge,item)[0]
            data.append(judgeNum)                 #提加评价人数
            
            inq = re.findall(findIng,item)
            if len(inq) != 0:
                inq = inq[0].replace(".","")      #去掉句号
                data.append(inq)                  #添加概述
            else:
                data.append("")                   #留空
            
            bd = re.findall(findBd,item)[0]
            bd = re.sub('<br(\s+)?/>(\s+)?',"",bd) #去掉<br/>
            bd = re.sub('/',"",bd)                 #替换/
            data.append(bd.strip())                #去掉前后的空格
            
            datalist.append(data)                  #把处理好的一部电影信息放入datalist
    # print(datalist)测试
    return datalist



##存入Excel表格

#简单演示
workbook = xlwt.Workbook(encoding="utf-8") #创建workbook对象
worksheet = workbook.add_sheet('sheet1')   #创建工作表
worksheet.write(0,0,'hello')               #写入数据,"行"、"列"、"内容"
workbook.save('student.xls')               #保存数据表

#小练习：乘法口诀表

#我的答案！（用时十多分钟,编程水平退步了...）
workbook = xlwt.Workbook(encoding="utf-8") #创建workbook对象
worksheet = workbook.add_sheet('sheet1')   #创建工作表
for i in range(9):
    for j in range (9):
     if(i>j):
      worksheet.write(i,j,"")
     else:
      worksheet.write(i,j,str(i+1)+'×'+str(j+1)+'='+str((i+1)*(j+1)))
workbook.save('加减乘除表.xls')             #保存数据表

#别人家的答案！
workbook = xlwt.Workbook(encoding="utf-8") #创建workbook对象
worksheet = workbook.add_sheet('sheet1')   #创建工作表
for i in range(0,9):
    for j in range(0,i+1):
        worksheet.write(i,j,"%d * %d = %d "%(i+1,j+1,(i+1)*(j+1)))
workbook.save('加减乘除表.xls')             #保存数据表
