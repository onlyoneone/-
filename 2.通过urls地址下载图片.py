#-*- coding:utf-8 -*-

"""
title:通过图片的urls地址下载(并重新命名)
author:zhangyi
(待)---------个人感觉比较的慢,不想飞的一样快
之前有看过比较简洁的,感觉自己写的有点多了
"""
import multiprocessing as mp
import requests
import time

#返回一组文档中的image_url
def open_file():
    with open('image_urls.txt','r+') as f:
        f.seek(0)
        return f.readlines()

#将图片写入自定义的路径
def save_image(url):
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36'
    }
    #去除imag_url中的空格和回车
    url=url.rstrip()
    image=requests.get(url,headers=headers)
    path=r'C:\Users\76324\Desktop\huo\BASE_image'
    image_name=url.split('/')[-1].split('.')[0]+'.jpg'
    print('正在保存>>>>',image_name,url,image.status_code)
    with open(path+'./'+image_name,'wb') as f:
        f.write(image.content)
        f.close()

if __name__ == '__main__':
    start=time.time()
    pro1=mp.Pool()
    image_urls=open_file()


    #使用多进程池(耗时18.7)
    pro1.map(save_image,image_urls)


    """
    #使用正常方法(耗时45.87)
    for url in image_urls :
        save_image(url)
    """


    print(time.time()-start)
