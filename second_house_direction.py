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
data_file=os.path.join(file,'second_house_new.csv')#返回数据所在文件位置
print(data_file)
df=pd.read_csv(data_file,engine='python',encoding='utf_8_sig')



for i in range(0,len(df['房屋朝向'])):
    if(df['房屋朝向'][i]=='南北'):
        df['房屋朝向'][i]='北'
        df['房屋朝向num'][i]=8

 
    

if(os.path.exists(os.path.join(file,'second_house_new_new.csv'))):#如果输出结果表格已经存在，则删除
    os.remove(os.path.join(file,'second_house_new_new.csv'))
df.to_csv('second_house_new_new.csv',index=False,encoding='utf_8_sig') #去掉index，输出表格csv
