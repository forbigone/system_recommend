# -*- coding: utf-8 -*-
"""
Created on Sat Jun 15 12:03:39 2019

@author: Administrator
"""

import os
import pandas as pd
import numpy as np
import re
print(os.path.dirname(os.path.abspath('__file__')))#返回代码所在目录
file=os.path.dirname(os.path.abspath('__file__'))
data_file=os.path.join(file,'second_house.csv')#返回数据所在文件位置
print(data_file)
df=pd.read_csv(data_file,engine='python',encoding='gb18030')


#

#
df['室']=0 
df['厅']=0
df['卫']=0
for i in range(0,len(df['房屋总价'])):    
    df['室'][i]=int(re.findall(r"(.+?)室",df['房屋户型'][i])[0])#利用正则表达式提取字符串,再转换为整型数,此时也是list，直接提取第一位【0】
    df['厅'][i]=int(re.findall(r"室(.+?)厅",df['房屋户型'][i])[0])
    df['卫'][i]=int(re.findall(r"厅(.+?)卫",df['房屋户型'][i])[0])
#    
    df['房本面积'][i]=float(re.findall(r"(.+?)㎡",df['房本面积'][i])[0])
   
df['房屋朝向num']=0
df['楼层高低num']=0
df['楼层层数num']=0
df['装修情况num']=0
df['产权年限num']=0
df['建筑年代num']=0
df['参考首付num']=0
df['月供num']=0
df['小区均价num']=0
df['所在商圈1num']=0
df['所在商圈2num']=0
type1=[]#['东北', '南北', '东', '南', '西', '西北', '西南', '北', '东南']房屋朝向
type2=['高','中','低','共']#楼层高低
type3=[]#['毛坯', '简单装修', '精装修', '豪华装修']装修情况
type4=[]#['坪山新区','大鹏新区','布吉','盐田' '光明新区', '福田','罗湖','龙岗区','宝安','龙华新区','南山','深圳周边']所在商圈
type5=[]#所在商圈
for i in range(0,len(df['房屋朝向'])):    
    type1.append(df['房屋朝向'][i])
    type3.append(df['装修情况'][i])
    df['所在商圈1num'][i]=re.findall(r"(.+?)－", df['所在商圈'][i])[0]#用-拆分商圈
    df['所在商圈2num'][i]=df['所在商圈'][i].split('－')[-1]
    type4.append(df['所在商圈1num'][i])
    type5.append(df['所在商圈2num'][i])
type1=list(set(type1))          #去重
type3=list(set(type3)) 
type4=list(set(type4)) 
type5=list(set(type5)) 



for i in range(0,len(df['房屋朝向'])):
    df['房屋朝向num'][i]=type1.index(df['房屋朝向'][i])+1       #返回字符所在list的位置
    df['楼层高低num'][i]=type2.index(df['所在楼层'][i][0:1])+1 #1:高  2:中  3:低  4:共   
    df['楼层层数num'][i]=re.findall(r"\d+\.?\d*", df['所在楼层'][i])[0]#提取数字
    df['装修情况num'][i]=type3.index(df['装修情况'][i])+1
    df['产权年限num'][i]=re.findall(r"\d+\.?\d*", df['产权年限'][i])[0]
    df['建筑年代num'][i]=re.findall(r"\d+\.?\d*", df['建筑年代'][i])[0]
    
    df['参考首付num'][i]=float(re.findall(r"(.+?)万",df['参考首付'][i])[0])
    df['月供num'][i]=int(re.findall(r"月供(.+?)元/月",df['参考首付'][i])[0])
    
    df['小区均价num'][i]=int(df['小区均价'][i][:-5])#去掉.0元这后缀，剩下整型数

    df['所在商圈1num'][i]=type4.index(df['所在商圈1num'][i])+1
    df['所在商圈2num'][i]=type5.index(df['所在商圈2num'][i])+1

 
    

if(os.path.exists(os.path.join(file,'second_house_new.csv'))):#如果输出结果表格已经存在，则删除
    os.remove(os.path.join(file,'second_house_new.csv'))
df.to_csv('second_house_new.csv',index=False,encoding='utf_8_sig') #去掉index，输出表格csv
