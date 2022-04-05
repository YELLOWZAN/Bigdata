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
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3534.4 Safari/537.36'}
    # 这个url并非固定模式，需要按照情况决定是否选用if-else引入url的特殊变量以切换界面。
    url = 'https://shenzhen.qfang.com/sale/f'
    for x in range(1, 11):
        response = requests.get(url + str(x), headers=headers)  # 获取响应数据
        time.sleep(2)  # 时间间隔放慢点（已经挨Q房网网站管理员电话问候了）
        selector = etree.HTML(response.text)  # 将响应的数据进行etree处理
        house_list = selector.xpath("//*[@id='cycleListings']/ul/li")  # 获取房源列表
        for house in house_list:  # 遍历房源列表
            # Xpath路径如下(经过多次错误发现在旧版微软Edge浏览器里面存在xpath显示定位错误问题，需要更新至新版edge浏览器以解决定位异常的bug)
            # 1.小区：//*[@id="cycleListings"]/ul/li/div[2]/div[3]/div
            # 2.户型：//*[@id="cycleListings"]/ul/li/div[2]/div[2]/p[1]
            # 3.面积：//*[@id="cycleListings"]/ul/li/div[2]/div[2]/p[2]
            # 4.建成时间：//*[@id="cycleListings"]/ul/li/div[2]/div[2]/p[6]（由于存在索引越界问题该项暂时不爬取）
            # 5.总价：//*[@id="cycleListings"]/ul/li/div[3]/p[1]
            # 6.房源特色：//*[@id="cycleListings"]/ul/li/div[2]/div[2]/p[3]（由于存在索引越界问题该项暂时不爬取）
            house_name = house.xpath("div[2]/div[1]/a/text()")[0]
            xiaoqu = house.xpath("div[2]/div[3]/div/text()")[0]
            huxing = house.xpath("div[2]/div[2]/p[1]/text()")[0]
            area = house.xpath("div[2]/div[2]/p[2]/text()")[0]
            money = house.xpath("div[3]/p[1]/text()")[0]

            item = [house_name, xiaoqu, huxing, area, money, ]
            data_writer(item)  # 传递item列表到data_writer(item)函数
            print("正在爬取中......第" + str(x) + "页")


# 定义保存模块函数
def data_writer(item):
    with open('Qfang_scrapy.csv', 'a', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(item)


# 程序入口（接口）
if __name__ == '__main__':
    spider()
