# -*- coding:utf-8 -*-
"""
title:爬取bing首页最新背景图
author:zhangyi
(待)-------还没能实现每日自动运行------
"""

import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36'
    }
    bing=requests.get('https://cn.bing.com',headers=headers)
    if bing.status_code==200:
        soup=BeautifulSoup(bing.text,'lxml')
        print(soup)
    else:
        exit()
    image_url=soup.find(id='bgLink').get('href')
    image=requests.get('https://cn.bing.com'+image_url)
    path=r'C:\Users\76324\Desktop\huo\bing_image'
    name=image_url.split('.')[1].split('_')[0]
    print(image.content)
    with open(path+'./'+name+'.jpg','ab') as f:
        f.write(image.content)
        f.close()