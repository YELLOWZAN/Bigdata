#!/usr/bin/python3
# --*-- coding:utf-8 --*--
# @作者: 大数据20班 黄德攒
# @软件： Pycharm Pro 2021.4
# @GitHub仓库： https://github.com/YELLOWZAN/Bigdata
import urllib.request
from lxml import etree
# 可能需要用到time模块来进行时间间隔获取数据，过快会导致网站崩溃，将面临律师函警告
# 下载前十页图片
# 请求数据
def create_request(i):
    # 定制url，不同网站的url定制方法不同，自行判断
    if i == 1:
        url = 'https://sc.chinaz.com/PSD/index.html'
    else:
        url = 'https://sc.chinaz.com/PSD/index_' + str(i) + '.html'
    # 请求头随便扒拉一个
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3534.4 Safari/537.36'}
    # 访问网站
    request = urllib.request.Request(url=url, headers=headers)
    return request


# 获取响应数据
def get_content(request):
    # 获取数据
    response = urllib.request.urlopen(request)
    # 解码数据
    content = response.read().decode('utf-8')
    return content


def down_load(content):
    # urllib.request.urlretrieve()
    # etree化获得的content数据
    tree = etree.HTML(content)
    # 获取图片源列表
    src_list = tree.xpath("//*[@id='container']/div/a/img/@src")  # //*[@id="container"]/div/a/img/@src
    name_list = tree.xpath("//*[@id='container']/div/a/img/@alt")
    # 读取name_list列表数据，并建立索引，将解析得到的名字写入文件
    for i in range(len(name_list)):
        name = name_list[i]  # 图片名列表
        src = src_list[i]  # 图片源列表
        url = 'https:' + src
        urllib.request.urlretrieve(url=url, filename='./img/' + name + '.jpg')


if __name__ == '__main__':
    start = int(input('输入开始页：'))
    end = int(input('输入结束页：'))
    # 调用模块函数
    for i in range(start, end + 1):
        request = create_request(i)
        content = get_content(request)
        down_load(content)
