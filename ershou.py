#!/usr/bin/env python
#-*- coding:utf-8 -*-
import requests
from lxml import etree
import time
import random
from fake_useragent import UserAgent

class LianjiaSpider(object):
    def __init__(self):
        #self.url = 'https://sh.lianjia.com/ershoufang/pg{}/'
        #self.url = 'https://sh.lianjia.com/ershoufang/pg{}y4sf1l2l3a3a4p3p4p5/' #限定价格 2房3房 面积房龄
        self.url = 'https://sh.lianjia.com/ershoufang/pudong/pg{}y4sf1l2l3a3a4p3p4p5/' #浦东
        

    def parse_html(self,url):
        #headers = {'User-Agent':UserAgent().random}
        headers = {'User-Agent': 'Mozilla/5.0(Macintosh;Intel Mac OS X 10_13_3) AppleWebKit/537.36(KHTML,like Gecko) Chorme/65.0.3325.162 Safari/537.36'}
        #当请求没响应时，再循环请求两次，没响应抛出异常。当响应成功，退出当前循环。继续下一页数据抓取
        for i in range(3):
            try:
                #Requests模块：向网站发请求并获取响应对象html内容，用content属性保险点,响应超时时间为3秒
                #html = requests.get(url=url,headers=headers).content.decode('utf-8','ignore',timeout=3)
                html = requests.get(url=url,headers=headers)
                self.get_data(html)
            except Exception as e:
                print('Retry')
                print(e)
        
    def get_data(self,html):
        #lxml模块：创建解析对象
        p = etree.HTML(html)
        #解析对象调用匹配房源信息的xpath表达式，返回值为节点对象列表：[li1,li2,li3]
        li_list = p.xpath('''/ul[@class="sellListContent"]/li[@class=
                        "clear LOGVIEWDATA LOGCLICKDATA"]''')
        item = {}
        #for循环遍历列表，获取每一个房源信息中的每一个具体信息，放入字典
        for p in li_list:
            #注意遍历厚继续xpath，xpath表达式要以 .开头,代表在当前节点下(不在整个html下)
            #小区名
            name_list = p.xpath('.//div[@class="positioninfo"]/a[1]/text()') #返回值是个列表
            #为防name_list没匹配出来，没匹配出来向数据库中存一个None
            item['name'] = name_list[0].strip() if name_list else None
            
            #区域
            region = p.xpath('.//div[@class="positioninfo"]/a[2]/text()')
            item['region'] = region[0].strip() if region else None
            
            #二手房信息
            houseinfo = p.xpath('.//div[@class="houseInfo"]/text()')
            #houseinfo = [“户型+面积+方位+是否精装+楼层+年代+类型"]
            #谨慎点，如果匹配出houseinfo 就拿数据，如果为空，就直接存一个None
            if houseinfo:
                houseinfo = houseinfo[0].split('|') #返回值是个列表
                #谨慎点，houseinfo列表里需要有7条数据,否则直接置为None
                if len(houseinfo) == 7:
                    item['housetype'] = houseinfo[0].strip()
                    item['area'] = houseinfo[1].strip()
                    item['direction'] = houseinfo[2].strip()
                    item['decoration'] = houseinfo[3].strip()
                    item['level'] = houseinfo[4].strip()
                    item['time'] = houseinfo[5].strip()[:-2]    #用切片取出数字，去掉最后两个汉字
                    item['type'] = houseinfo[6].strip()
                else:
                    item['housetype'] = item['area'] = item['direction'] = \
                    item['decoration'] = item['level'] = item['time'] = item['type']  \
                    = None
            else:
                item['housetype'] = item['area'] = item['direction'] =  \
                    item['decoration'] = item['level'] = item['time'] = item['type']  \
                    = None
            
            #总价
            total_list = p.xpath('.//div[@class="totalPrice"]/span/text()')
            item['total'] = total_list[0].strip() if total_list else None
            #每平米单价
            unit_list = p.xpath('.//div[@class="unitPrice"]/span/text()')
            item['unit'] = unit_list[0].strip() if unit_list else None

        print(item)

    def run(self):
        for page in range(1,63):
            url = self.url.format(page)
            self.parse_html(url)
            time.sleep(random.randint(1,2))

if __name__ == '__main__':
    spider = LianjiaSpider()
    spider.run()

