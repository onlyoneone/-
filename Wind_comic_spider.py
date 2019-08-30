# -*- coding:utf-8 -*-
"""
title:获取风之动漫的漫画集(/笑)
author:zhangyi
心血来潮,并没有使用item和pipelines管道,有待改进
"""
import re
import os
import scrapy
from xxx.items import XxxItem


class WindSpider(scrapy.Spider):
    name = 'wind_comic'
    start_urls=['https://manhua.fzdm.com/']
    # 设置存储路径
    path=r'E:/风之动漫/'
    # 设置存储文件夹name()
    file_name = '大剑'

    #真心懵逼,现有图片url提取不出,只能另辟新径,所以还要个图片的基础网址
    base_image_url='http://p0.manhuapan.com/'

    #定义想要爬取的内容,提取其目录网址
    def parse(self, response):
        #此处可修改你想要的comic_name(后缀+漫画)
        first_url=response.url+response.xpath('//*[@id="mhmain"]/ul/div/li[1]/a[@title="{}漫画"]/@href'.format(self.file_name)).extract_first()
        comic_file_path=self.path+self.file_name
        #创建主文件
        if not os.path.exists(comic_file_path):
            os.mkdir(comic_file_path)
        yield scrapy.Request(first_url,callback=self.parse_two,meta={'file_name':comic_file_path},dont_filter=True)

    #提取漫画目录章节的地址s
    def parse_two(self,response):

        chapter_urls=response.xpath('//*[@id="content"][1]/li/a/@href').extract()
        chapter_names=response.xpath('////*[@id="content"][1]/li/a/@title').extract()
        for chapter_url,chapter_name in zip(chapter_urls,chapter_names):
            #创建章节文件夹
            chapter_file_path = response.meta['file_name'] +'/'+chapter_name
            if not os.path.exists(chapter_file_path):
                os.mkdir(chapter_file_path)
            yield scrapy.Request(response.url+chapter_url,callback=self.parse_three,meta={'chapter_file_path':chapter_file_path})


    #get_image_url
    def parse_three(self,response):
        biaoda=re.compile(r'(.*/)index_(.*)',re.S)
        biaodashi=re.compile(r'.*="(.*jpg).*',re.S)
        next_url=response.xpath('//*[@id="pjax-container"]/div[@class="navigation"]/a[contains(text(),"下一页")]/@href').extract_first()
        if next_url:
            if response.url.split('/')[-1]=='':
                yield scrapy.Request(response.url+next_url,callback=self.parse_three,meta={'chapter_file_path':response.meta['chapter_file_path']})
            else:
                self.log(response.meta['chapter_file_path'])
                yield scrapy.Request(re.findall(biaoda,response.url)[0][0]+next_url,callback=self.parse_three,meta={'chapter_file_path':response.meta['chapter_file_path']})
        try:
            xurl=re.findall(biaodashi,response.xpath('//*[@id="pjax-container"]/script[2]').extract_first())[0]
            image_url=self.base_image_url+xurl
            yield scrapy.Request(image_url, callback=self.parse_five,
                                 meta={'chapter_file_path': response.meta['chapter_file_path']})
        except:
            pass



    #save_to_image
    def parse_five(self,response):
        image_name='0'+response.url.split('/')[-1]
        with open(response.meta['chapter_file_path']+'/'+image_name,'wb') as file:
            file.write(response.body)
            file.close()








