#!/usr/bin/python3
# --*-- coding:utf-8 --*--
# @作者: 大数据20班 黄德攒
# @软件： Pycharm Pro 2021.4
# @GitHub仓库： https://github.com/YELLOWZAN/Bigdata

import time
import requests
from lxml import etree
import csv


# 定义爬虫主体函数
def spider():
    # 定义标头（随便去浏览器那里扒拉一个下来就行了）
    global house_dizhi3
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3534.4 Safari/537.36'}
    # 这个url并非固定模式，需要按照情况决定是否选用if-else引入url的特殊变量以切换界面。
    for i in range(1,6):
        if i==1:
            url = 'https://sh.lianjia.com/zufang/#contentList'
        else:
            url = 'https://sh.lianjia.com/zufang/pg' + str(i) + '/#contentList'
        response = requests.get(url, headers=headers)  # 获取响应数据
        time.sleep(2)  # 时间间隔放慢点
        selector = etree.HTML(response.text)  # 将响应的数据进行etree处理
        house_list = selector.xpath("//*[@id='content']/div[1]/div[1]/div/div")  # 获取房源列表
        for house in house_list:  # 遍历房源列表
            # Xpath路径如下(经过多次错误发现在旧版微软Edge浏览器里面存在xpath显示定位错误问题，
            # 需要更新至新版edge浏览器以解决定位异常的bug)
            # 0.房名：p[1]/a
            # 1.出租屋户型：p[2]/text()[5]
            # 2.租金：span/text()
            # 3.所在地址p[2]/a[1]  |  p[2]/a[2]  |  p[2]/a[3]
            # 4.面积 p[2]/text()[3]
            # 5.官方信息  p[3]/text()
            # 6.房型网页详情页面p[1]/a/@href
            try:
                house_name = house.xpath("p[1]/a/text()")[0]
                house_style = house.xpath("p[2]/text()[7]")[0]
                house_money = house.xpath("span/em/text()")[0]
                house_dizhi1 = house.xpath("p[2]/a[1]/text()")[0]  # 由于网站设计十分傻逼，房子地址中间的分隔符是没有标签定位的，所以使用贪婪大法来匹配数据
                house_dizhi2 = house.xpath("p[2]/a[2]/text()")[0]
                house_dizhi3 = house.xpath("p[2]/a[3]/text()")[0]
                house_area = house.xpath("p[2]/text()[5]")[0]
                guanfang_info = house.xpath("p[3]/i/text()")[0]
                house_info = house.xpath("p[1]/a/@href")[0]
            except:
                print("写入错误，进行下一条数据获取")
            item = [house_name, house_style, house_money+'元/月', house_dizhi1+'-'+house_dizhi2+'-'+house_dizhi3, house_area, guanfang_info, house_info]
            data_writer(item)  # 传递item列表到data_writer(item)函数
        print("正在爬取中第" + str(i) + "页......")


# 定义保存模块函数
def data_writer(item):
    with open('lianjia_scrapy.csv', 'a', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(item)


# 程序入口（接口）
if __name__ == '__main__':
    spider()
