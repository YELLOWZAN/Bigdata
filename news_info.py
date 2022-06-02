import requests
from lxml import etree
import time
import csv

# 响应模块
def down_load(i):
    url = 'http://sousuo.gov.cn/column/31421/' + str(i) + '.htm'
    headers = {
        'Cookie': '_gscu_603879440 = 54007693ub431y17;_gscbrs_603879440 = 1;_gscs_603879440 = t541826665dtqnh19 | pv:1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.53'}
    response = requests.get(url, headers=headers)
    time.sleep(2)
    tree = etree.HTML(response.text)
    list = tree.xpath('/html/body/div[2]/div/div[2]/div[2]/ul/li')
    for info in list:
        try:
            news_title = info.xpath('./h4/a/text()')[0]
            news_date = info.xpath('./h4/span/text()')[0]
            news_url = info.xpath('./h4/a/@href')[0]
        except IndexError:
            print("本次爬取错误，请检查后台！")
        print(news_title, news_date)
        item = [news_date, news_title, news_url]
        data_writer(item)

# 下载数据模块
def data_writer(item):
    with open('5week_news_info.csv', 'a', encoding='utf-8') as fp:
        writer = csv.writer(fp)
        writer.writerow(item)

# 程序主入口
if __name__ == '__main__':
    # 10-31
    print("程序运行:")
    start = int(input("start page:"))
    end = int(input("end page:"))
    for a in range(start, end + 1):
        try:
            print("准备爬取第" + str(a) + "页")
            down_load(a)
            print("爬取第" + str(a) + "页完成")
            time.sleep(2)
        except:
            print("请检查错误！\n" * 3)
