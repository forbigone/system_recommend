# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 16:59:36 2019

@author: Administrator
"""
import pandas as pd
import os
import re


file=os.path.dirname(os.path.abspath('__file__'))
data_file=os.path.join(file,'ratings.csv')#返回数据所在文件位置
print(data_file)
df_user=pd.read_csv(data_file,engine='python',encoding='utf-8')
data_file=os.path.join(file,'movies_info.csv')#返回数据所在文件位置
df_m=pd.read_csv(data_file,engine='python',encoding='utf-8')



for i in range(len(df_user['movieId'])):     
    if(df_user.loc[i,'movieId'] in df_m['movies_id'].values):
        continue
        
    else:
        df_user.drop(index=i)
file=os.path.dirname(os.path.abspath('__file__'))   
if(os.path.exists(os.path.join(file,'ratings.csv'))):#如果输出结果表格已经存在，则删除
    os.remove(os.path.join(file,'ratings.csv'))
df_user.to_csv('ratings.csv',index=False,encoding='utf_8')        





