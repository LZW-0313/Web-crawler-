# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 16:10:39 2020

@author: lx
"""
import pandas as pd
import requests 
import json 
# 引用requests,json模块 
url = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp'
headers = { 
    'referer':'https://y.qq.com/portal/search.html', 
    # 请求来源 
    'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    # 标记了请求从什么设备，什么浏览器上发出 11

} 
for x in range(1): 
    params = {
        'ct':'24',
        'qqmusic_ver': '1298', 
        'new_json':'1', 
        'remoteplace':'sizer.yqq.lyric_next', 
        'searchid':'94267071827046963', 
        'aggr':'1',
        'cr':'1', 
        'catZhida':'1', 
        'lossless':'0', 
        'sem':'1', 
        't':'7', 
        'p':str(x+1), 
        'n':'50', 
        'w':'周杰伦', 
        'g_tk':'1714057807', 
        'loginUin':'0', 
        'hostUin':'0', 
        'format':'json', 
        'inCharset':'utf8', 
        'outCharset':'utf-8', 
        'notice':'0', 
        'platform':'yqq.json', 
        'needNewCode':'0' 
    }
    res = requests.get(url, params = params) 
    #下载该网页，赋值给res 
    jsonres = json.loads(res.text) 
    #使用json来解析res.text 
    list_lyric = jsonres['data']['lyric']['list'] 
    #一层一层地取字典，获取歌词的列表 
    for lyric in list_lyric: 
        # lyric是一个列表，x是它里面的元素 
        print(lyric['content']+'\n') 
        #以content为键，查找歌词 

#将结果保存在一个列表中#
result=[]
for lyric in list_lyric: 
        # lyric是一个列表，x是它里面的元素 
        result.append(lyric['content']) 
        #以content为键，查找歌词 
print(result)

#词切分后,导出数据,保存为csv格式2(目前词切分还未完成！！！！)#
data=pd.core.frame.DataFrame(result)
data0 = data[0].str.split('-',1,expand=True) #按""进行切分
data1 = data0[1].str.split('词',1,expand=True) #按""进行切分
data2 = data1[1].str.split('曲',1,expand=True) 
data3 = data2[1].str.split('编曲',1,expand=True) 
data.to_csv('data.csv',encoding='gbk')    ##输出数据