import re
import time
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import random
from fake_useragent import UserAgent
from pandas import Series,DataFrame
#def get_ip_list():
#	f = open('ip_proxy.txt','r')
#	ip_list = f.readlines()
#	# print(ip_list)
#	f.close()
#	return ip_list
# 
#def get_random_ip(ip_list):
#	proxy_ip = random.choice(ip_list)
#	proxy_ip = proxy_ip.strip('\n')
#	proxies = {'https': proxy_ip}
#	return proxies

# 定义了一个获取网页的方法 (http请求)
def getHtml(url):
#    ua = UserAgent(use_cache_server=False)
#    headers={'User-Agent': ua.random}
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
#    print(js.text)
    views=js.text.split('=')[-1]
#    print(views)
    return views
# 定义了一个解析网页的方法 (解析器)
def parserHtml(html):  # 将一个下载好的html传入解析器
    soup=bs(html,'lxml')
    print()
    try:
        description = soup.find(attrs={"name":"description"})['content']
        house_price=re.findall(r"售价：(.+?)万元",description)[0]#房价/万元
        m_price=re.findall(r"万元（(.+?)元/㎡）",description)[0]#元/平
        b=soup.find(attrs={"http-equiv":"mobile-agent"})['content']#得到隐藏的浏览量的url
#        print(b)
        url0=b.split('=')[-1]
#        print(url0)
        views=view_num(url0)
        general=soup.find_all('div', class_="general-item-wrap")[0]
        left=general.find_all('ul',class_="general-item-left")[0]
        right=general.find_all('ul',class_="general-item-right")[0]
        information=[]
        
        information.append(soup.find_all('h1',class_="c_333 f20")[0].string.strip())#房屋标题
        information.append(description)#简述
        information.append(views)#浏览量
        
        
        information.append(house_price)#房屋总价
        information.append(m_price)#元/平
        information.append(left.find_all('span',class_="c_000")[1].string.strip())#房屋户型
        information.append(left.find_all('span',class_="c_000")[2].string.strip())#房本面积
        information.append(left.find_all('span',class_="c_000")[3].string.strip())#房屋朝向
        information.append(right.find_all('span',class_="c_000")[0].string.strip())#所在楼层
        information.append(right.find_all('span',class_="c_000")[1].string.strip())#装修情况
        information.append(right.find_all('span',class_="c_000")[2].string.strip())#产权年限
        information.append(right.find_all('span',class_="c_000")[3].string.strip())#建筑年代
        
        information.append(soup.find_all('p',class_="pic-desc-word")[0].text.strip())#核心卖点
        information.append(soup.find_all('p',class_="pic-desc-word")[1].text.strip())#业主心态
        information.append(soup.find_all('p',class_="pic-desc-word")[2].text.strip())#服务介绍
        information.append(soup.find_all('p',class_="pic-desc-word")[3].text.strip())#核验编码
    
        first=soup.find_all('div', class_="general-item general-expense")[0]
        information.append(first.find_all('span',class_="c_000")[3].text.strip())#参考首付
        
        xiaoqu=soup.find_all('ul', class_="xiaoqu-desc")[0]
        information.append(xiaoqu.find_all('span',class_="c_333 mr_20")[0].text.strip())#小区均价
        information.append(xiaoqu.find_all('span',class_="c_333")[1].text.strip().replace('\n','').replace(' ',''))#所在商圈
        information.append(xiaoqu.find_all('span',class_="c_333")[2].text.strip())#物业费
        information.append(xiaoqu.find_all('span',class_="c_333")[3].text.strip())#容积率
        information.append(xiaoqu.find_all('span',class_="c_333")[4].text.strip())#绿化率
        information.append(xiaoqu.find_all('span',class_="c_333")[5].text.strip())#车位信息
        
        print(information)
        return information
    except:
        print('**************访问过于频繁，本次访问做以下验证码校验************')
        time.sleep(30)
        return 0
    
   
# 主函数
names = locals()

for i in range(0,23):
    names['list' + str(i) ] = []


#ip_list=get_ip_list()
space='D:\信工电协\python课件及代码\练习代码/'+'web_house.txt'
with open(space,'r',encoding='utf-8') as ff:    
    for url in ff.readlines():
        html = getHtml(url)  # 下载html (将格式化好的url1传入 getHtml 方法中)
        information=parserHtml(html)  # 解析html (将下载好的 html 传入 parserHtml 方法中解析)
        if (information!=0):
            for i in range(0,23):
                locals()['list' + str(i)].append(information[i])
            time.sleep(5)  # 暂停一秒 (有时候有检测会封 ip 然后将暂停时间调大一点 手动进入浏览器将验证码输入一遍就可以重新爬取了.
data={'房屋标题':list0,'简述':list1,'浏览量':list2,'房屋总价':list3,'元/平':list4,'房屋户型':list5,'房本面积':list6,'房屋朝向':list7,'所在楼层':list8,'装修情况':list9,'产权年限':list10,'建筑年代':list11,'核心卖点':list12,'业主心态':list13,'服务介绍':list14,'核验编码':list15,'参考首付':list16,'小区均价':list17,'所在商圈':list18,'物业费':list19,'容积率':list20,'绿化率':list21,'车位信息':list22}
data_form=DataFrame(data)
#data_form=data_form[data_form['cpu_size']!='']       #取型号不为空‘’ 的dataframe，效果即删除空值
data_form.to_csv('second_house.csv',index=False,encoding='gb18030') #去掉index，输出表格csv 



