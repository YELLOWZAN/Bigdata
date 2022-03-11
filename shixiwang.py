import requests  #网络请求
import urllib3
urllib3.disable_warnings()  #关闭警告信息
from lxml import etree #解析
import pandas as pd
'''
一、爬取数据
1、获取单页数据
2、解析第一层页面获取目标内容
3、解析第二层页面获取工作描述
4、批量爬取数据
5、数据保存

'''

#请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
}
#目标地址
web_url = 'https://www.shixi.com/search/index?key=%E6%95%B0%E6%8D%AE%E6%8C%96%E6%8E%98&page='
Job_name = []
Job_address = []
Company = []
Xinzi = []
Xueli = []
Job_time = []
for i in range(1,5):
    print('正在爬取第',i, '页信息')
    url = web_url +  str(i)
    web = requests.get(url, headers=headers, verify=False) #获取网页源码
    # web.encoding = "utf-8"
    # print(web.text)
    dom = etree.HTML(web.text) #将网页源码解析成dom树

    job_name = dom.xpath('//a[@class="job-name"]/text()')
    # print(job_name)
    job_name_url = dom.xpath('//a[@class="job-name"]/@href')
    # print(job_name_url)
    job_address = dom.xpath('//a[@class="job-address"]/text()')
    # print(job_address)
    company = dom.xpath('//div[@class="company-info-title"]/a/text()')
    # print(company)
    xinzi = dom.xpath('//div[@class="company-info-des"]/text()')
    # print(xinzi)
    xueli = dom.xpath('//span[@class="job-educational"]/text()')
    # print(xueli)
    job_time = dom.xpath('//span[@class="job-time"]/text()')
    # print(job_time)
    home = 'https://www.shixi.com'
    desurl = [home + i for i in job_name_url]
    # print(desurl)
    Des = []
    #第二层解析
    for j in desurl:
        web2 = requests.get(j, headers=headers, verify=False) #获取网页源码
        # web.encoding = "utf-8"
        # print(web.text)
        dom2 = etree.HTML(web2.text) #将网页源码解析成dom树
        # dom2.encoding = 'gbk'
        workdes = dom2.xpath('//div[@class="work_b"]/text()')
        # print(workdes)
        Des.extend(workdes)
    Job_name.extend(job_name)
    Job_address.extend(job_address)
    Company.extend(company)
    Xinzi.extend(xinzi)
    Xueli.extend(xueli)
    Job_time.extend(job_time)


    data = pd.DataFrame()
    data['岗位名称'] = Job_name
    data['地址'] =Job_address
    data['公司名称'] = Company
    data['薪资'] = Xinzi
    data['学历'] = Xueli
    data['日期'] = Job_time
    data['工作描述'] = Des

# data.to_csv('20220311.csv', encoding='gbk', index_label=['序号'],index=True)
data.to_excel('0311.xls',encoding='gbk', index_label=['序号'],index=True)