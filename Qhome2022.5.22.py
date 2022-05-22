#!/usr/bin/python3
# --*-- coding:utf-8 --*--
# @作者: 大数据20班 黄德攒
# @软件： Pycharm Pro 2021.4
# @GitHub仓库： https://github.com/YELLOWZAN/Bigdata
import urllib.request
import requests
from lxml import etree
from selenium import webdriver
import time
import csv

# 请求数据
def create_request(i):
    # 定制url，不同网站的url定制方法不同，自行判断
    if i == 1:
        url = 'https://shenzhen.qfang.com/sale/f1'
    else:
        url = 'https://shenzhen.qfang.com/sale/f' + str(i)
    # 请求头随便扒拉一个
    path = 'msedgedriver.exe'
    browser = webdriver.Edge(path)
    browser.get(url)
    # 浏览器页面分辨率为1420*9240，分段滑动，一次往下滑100px，需要滑动（9240/100）次
    # browser.save_screenshot('page' + str(i) + '.png')
    # 房源信息：//*[@id="cycleListings"]/ul/li/div[2]/div[1]/a
    for c in range(28):
        js = 'window.scrollBy(0,300)'
        browser.execute_script(js)
        time.sleep(0.5)  # 每次滑动时间间隔0.5秒

    request = browser.page_source
    time.sleep(5)
    return request

# 获取响应数据
def get_content(request):
    content = request
    return content

# 下载图片模块
def down_load(content):
    # urllib.request.urlretrieve()

    tree = etree.HTML(content)
    # 获取图片源列表
    src_list = tree.xpath(
        "//*[@id='cycleListings']/ul/li/div[1]/a/img/@src")  # //*[@id="cycleListings"]/ul/li/div[1]/a/img/@src
    name_list = tree.xpath(
        "//*[@id='cycleListings']/ul/li/div[1]/a/img/@alt")  # //*[@id="cycleListings"]/ul/li/div[1]/a/img/@alt
    # 读取name_list列表数据，并建立索引，将解析得到的名字写入文件
    for i in range(len(name_list)):
        try:
            name = name_list[i]  # 图片名列表
            src = src_list[i]
            # 图片源列表
            url = src
            urllib.request.urlretrieve(url=url, filename='./Qfang_img/' + name + '.jpg')  # './jpg/'意思为存放图片的路径
            print("正在下载第" + str(i + 1) + "张图片:" + name + ':' + src)

        except IndexError:
            print("爬取出错，正在跳过本项，进行下一项数据爬取")

    base_url = 'https://shenzhen.qfang.com'
    house_info_page_url = tree.xpath('//*[@id="cycleListings"]/ul/li/div[2]/div[1]/a/@href')
    for i in house_info_page_url:
        page_url = base_url+str(i)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3534.4 Safari/537.36'}
        page_response = requests.get(page_url, headers=headers)
        time.sleep(2)
        select_info = etree.HTML(page_response.text)
        try:
            # 房屋户型A //*[@id="scrollto-1"]/div[2]/ul/li[1]/div[2]
            # 所在楼层B //*[@id="scrollto-1"]/div[2]/ul/li[2]/div[2]
            # 建筑面积C //*[@id="scrollto-1"]/div[2]/ul/li[3]/div[2]
            # 户型结构D //*[@id="scrollto-1"]/div[2]/ul/li[4]/div[2]
            # 房屋朝向E //*[@id="scrollto-1"]/div[2]/ul/li[5]/div[2]
            # 装修情况F //*[@id="scrollto-1"]/div[2]/ul/li[6]/div[2]
            # 配备电梯G //*[@id="scrollto-1"]/div[2]/ul/li[7]/div[2]
            # 房屋用途H //*[@id="scrollto-1"]/div[3]/ul/li[1]/div[2]
            # 上次交易I //*[@id="scrollto-1"]/div[3]/ul/li[2]/div[2]
            # 房屋年限J //*[@id="scrollto-1"]/div[3]/ul/li[3]/div[2]
            # 建筑年代K //*[@id="scrollto-1"]/div[3]/ul/li[4]/div[2]
            # 抵押信息L //*[@id="scrollto-1"]/div[3]/ul/li[5]/div[2]
            # 房本备件M //*[@id="scrollto-1"]/div[3]/ul/li[6]/div[2]
            # 挂牌时间N //*[@id="scrollto-1"]/div[3]/ul/li[7]/div[2]
            # 房源编码O //*[@id="scrollto-1"]/div[3]/ul/li[8]/div[2]
            A = select_info.xpath('//*[@id="scrollto-1"]/div[2]/ul/li[1]/div[2]/text()')[0]
            B = select_info.xpath('//*[@id="scrollto-1"]/div[2]/ul/li[2]/div[2]/text()')[0]
            C = select_info.xpath('//*[@id="scrollto-1"]/div[2]/ul/li[3]/div[2]/text()')[0]
            D = select_info.xpath('//*[@id="scrollto-1"]/div[2]/ul/li[4]/div[2]/text()')[0]
            E = select_info.xpath('//*[@id="scrollto-1"]/div[2]/ul/li[5]/div[2]/text()')[0]
            F = select_info.xpath('//*[@id="scrollto-1"]/div[2]/ul/li[6]/div[2]/text()')[0]
            G = select_info.xpath('//*[@id="scrollto-1"]/div[2]/ul/li[7]/div[2]/text()')[0]

            H = select_info.xpath('//*[@id="scrollto-1"]/div[3]/ul/li[1]/div[2]/text()')[0]
            I = select_info.xpath('//*[@id="scrollto-1"]/div[3]/ul/li[2]/div[2]/text()')[0]
            J = select_info.xpath('//*[@id="scrollto-1"]/div[3]/ul/li[3]/div[2]/text()')[0]
            K = select_info.xpath('//*[@id="scrollto-1"]/div[3]/ul/li[4]/div[2]/text()')[0]
            L = select_info.xpath('//*[@id="scrollto-1"]/div[3]/ul/li[5]/div[2]/text()')[0]
            M = select_info.xpath('//*[@id="scrollto-1"]/div[3]/ul/li[6]/div[2]/text()')[0]
            N = select_info.xpath('//*[@id="scrollto-1"]/div[3]/ul/li[7]/div[2]/text()')[0]
            O = select_info.xpath('//*[@id="scrollto-1"]/div[3]/ul/li[8]/div[2]/text()')[0]

        except:
            print('error')
        item = [A, B, C, D, E, F, G, H, I, J, K, L, M, N, O]
        data_writer(item)
        time.sleep(1)

# 下载数据模块
def data_writer(item):
    with open('fangyuan_info.csv', 'a', encoding='utf-8') as fp:
        writer = csv.writer(fp)
        writer.writerow(item)

# 程序主入口
if __name__ == '__main__':
    start = int(input('输入开始页：'))
    end = int(input('输入结束页：'))
    # 调用模块函数
    for a in range(start, end + 1):
        try:
            print("准备爬取第" + str(a) + "页")
            request = create_request(a)
            content = get_content(request)
            down_load(content)
            print("爬取第" + str(a) + "页完成")
            time.sleep(5)
        except:
            print("请检查错误！\n" * 3)
