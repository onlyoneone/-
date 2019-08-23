"""
title:http://www.doutula.com/
author:zhangyi
test_____
采用自动化运维的方式,提取(多线程)
流程：
1.进入主界面,在search_input输入自定义文字,按下button,进入下一界面
2.(进入该网页没有分页,必须先点击'查看更多')获取相应页码
3.获取(每一页)每一张的图片地址(作为一个集合)
4.启用多进程池
5.下载每一张图片,并保存至不同文件夹(以格式分类)
6.退出
"""

from bs4 import BeautifulSoup                                     #美味的汤
from selenium.webdriver import Chrome                             #浏览器
from selenium.webdriver.chrome.options import Options             #无头模式
from selenium.webdriver.common.by import By                       #定义模式
from selenium.webdriver.support import expected_conditions as EC  #浏览状态
from selenium.webdriver.support.ui import WebDriverWait as Wait   #等待
import multiprocessing as mp                                      #多线程
import time
import requests


def initx(driver):
    driver.get('https://www.doutula.com/so/')
    W=Wait(driver,timeout=10)
    search_input=W.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.form-control')))
    search_button=W.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'button.btn.btn-default')))
    search_input.send_keys('熊猫')#输入想要的图片名!!!<<<<<<<<<<<<<<<<<<<
    search_button.click()
    play_ajax()


    image_urls=get_image_urls(driver)

    return image_urls


def get_image_urls(driver):
    image_urls=[]
    soup_one=BeautifulSoup(driver.page_source,'lxml')
    urls=soup_one.find(class_='random_picture').find_all(class_='col-xs-6')
    for url in urls:
        image_url=url.find(class_='img-responsive').get('src')
        if image_url=='//static.doutula.com/img/loader.gif?30':
            continue
        print(image_url)
        image_urls.append(image_url)

    return image_urls




def download_image(image_url):
    image_style=image_url.split('.')[-1]
    image_name=image_url.split('/')[-1]
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36'
    }
    new_content=requests.get(image_url,headers=headers)
    print('downloading_image>>>',image_name)
    if image_style=='gif':
        with open('./doutu_gif/'+image_name,'wb') as f:
            f.write(new_content.content)
            f.close()
    else:
        with open('./doutu_image/'+image_name,'wb') as f:
            f.write(new_content.content)
            f.close()


def next_page():
    time.sleep(2)
    next_button=driver.find_elements_by_css_selector('.page-item')[-1].find_element_by_css_selector('a')
    next_button.click()
    print('over')



#让页面下拉,实现ajax动态加载(使用JS,不太理解)
def play_ajax():
    for i in range(3):
        js = "document.documentElement.scrollTop=%d"%(i*1200)
        driver.execute_script(js)
        time.sleep(1)

def total_download():
    #点击'more'
    more_button=Wait(driver,timeout=10).until(EC.element_to_be_clickable((By.CLASS_NAME,'more')))
    more_button.click()
    page=int(driver.find_elements_by_class_name('page-link')[-2].text)
    print(page)
    for i in range(page-1):
        play_ajax()
        urls=get_image_urls(driver)
        pc1.map(download_image,urls)
        next_page()



if __name__ == '__main__':
    #设置无头模式
    #option=Options()
    #option.add_argument('--headless')
    driver=Chrome()#options=option)
    urls=initx(driver)

    pc1=mp.Pool()
    pc1.map(download_image,urls)

    total_download()

    print('>>>>>>>>total download sucessful!')

