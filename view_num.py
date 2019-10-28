import re
import time
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import random


# 定义了一个获取网页的方法 (http请求)
def getHtml(url):
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'}
#    proxies=get_random_ip(ip_list)
#    response = requests.get(url=url, proxies=proxies,headers=headers) 
    response = requests.get(url=url, headers=headers) 
    response.encoding='utf-8'
    html=response.text
    return html  # 返回给调用者


def view_num(url0):
    id=url0.split("/")[-1].strip('x.shtml')
    url='https://jst1.58.com/counter?infoid={}'.format(id)
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
             'referer':'https://sz.58.com/ershoufang/'}
    js = requests.get(url=url, headers=headers) 
#    js=requests.get(api)
    print(js.text)
    views=js.text.split('=')[-1]
    print(views)
    return views



# 定义了一个解析网页的方法 (解析器)
def parserHtml(html,web_list):  # 将一个下载好的html传入解析器
    soup=bs(html,'lxml')
    description = soup.find(attrs={"name":"description"})['content']
    print(re.findall(r"售价：(.+?)万元",description)[0])
    print(re.findall(r"万元（(.+?)元/㎡）",description)[0])
    b=soup.find(attrs={"http-equiv":"mobile-agent"})['content']
    print(b)
    url0=b.split('=')[-1]
    print(url0)
    view_num(url0)
# 主函数
#ip_list=get_ip_list()
web_list=[]
for i in range(1, 2):  # 遍历30次(看了一下网站 大概只有30页 )
    print('第{}页'.format(i))  # 打印正在爬取第几页
    url='https://sz.58.com/ershoufang/39037822369936x.shtml?from=1-list-0&iuType=z_1&PGTID=0d30000c-0000-4481-17be-1e11ca220919&ClickID=3&adtype=3'
    html = getHtml(url)  # 下载html (将格式化好的url1传入 getHtml 方法中)
    web_list=parserHtml(html,web_list)  # 解析html (将下载好的 html 传入 parserHtml 方法中解析)
    time.sleep(5)  # 暂停一秒 (有时候有检测会封 ip 然后将暂停时间调大一点 手动进入浏览器将验证码输入一遍就可以重新爬取了.

'''
space='D:\信工电协\python课件及代码\练习代码/'+'web_house.txt'
with open(space,'w+',encoding='utf-8') as ff:
    for i in web_list:
        ff.write(i+'\n')
        
'''        