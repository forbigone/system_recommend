# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 16:59:36 2019

@author: Administrator
"""
import pandas as pd
import os
import re


file=os.path.dirname(os.path.abspath('__file__'))
data_file=os.path.join(file,'ml-latest-small/movies.csv')#返回数据所在文件位置
print(data_file)
df=pd.read_csv(data_file,engine='python',encoding='utf-8')
#df = df.loc[0:100,:]
movies_id=df["movieId"]
release_date=df.loc[:,"title"].copy()
title=df.loc[:,"title"].copy()
for i in range(len(release_date)):
    
    try:
       release_date[i] = int(re.findall(r'[(](.*?)[)]',release_date.loc[i])[-1])  # 提取上映日期#运行别的代码
    except IndexError:
       release_date[i] = 0#如果在try部份引发了'name'异常
data={'movies_id':movies_id,'title':title,'release_date':release_date}
data_form=pd.DataFrame(data)
types = ['Action','Adventure','Animation',"Children",'Comedy','Crime','Documentary','Drama','Fantasy','Film-Noir','Horror','Musical','Mystery','Romance','Sci-Fi','Thriller','War','Western']

for i in types:
    data_form[i] = 0

degree = ['pessimistic_degree','optimism_degree','action_degree','child_degree','terror_degree','romantic_degree','brain_degree']
for i in degree:
    data_form[i] = 0
    
for i in range(len(release_date)):
    list_type = re.split(re.compile(r'\|'),df.loc[i,'genres'])
    for j in list_type:
        data_form.loc[i,j] = 1
        if (j=='Action'):
            data_form.loc[i,'action_degree'] = data_form.loc[i,'action_degree'] + 1
            continue
        if (j=='Adventure'):
            data_form.loc[i,'action_degree'] = data_form.loc[i,'action_degree'] + 0.25
            continue
        if (j=='Animation'):
            data_form.loc[i,'optimism_degree'] = data_form.loc[i,'optimism_degree'] + 0.5
            data_form.loc[i,'child_degree'] = data_form.loc[i,'child_degree']* + 1
            continue
        if (j=="Children"):
            data_form.loc[i,'optimism_degree'] = data_form.loc[i,'optimism_degree'] + 1
            data_form.loc[i,'child_degree'] = data_form.loc[i,'child_degree']* + 1
            continue
        if (j=='Comedy'):
            data_form.loc[i,'optimism_degree'] = data_form.loc[i,'optimism_degree'] + 1
            continue
        if (j=='Crime'):
            data_form.loc[i,'action_degree'] = data_form.loc[i,'action_degree'] + 1
            data_form.loc[i,'terror_degree'] = data_form.loc[i,'terror_degree'] + 0.25
            data_form.loc[i,'brain_degree'] = data_form.loc[i,'brain_degree'] + 0.25
            continue
        if (j=='Documentary'):
            data_form.loc[i,'brain_degree'] = data_form.loc[i,'brain_degree'] + 0.5
            continue
        if (j=='Drama'):
            data_form.loc[i,'romantic_degree'] = data_form.loc[i,'romantic_degree'] + 0.25
            continue
        if (j=='Fantasy'):
            data_form.loc[i,'optimism_degree'] = data_form.loc[i,'optimism_degree'] + 0.5
            data_form.loc[i,'romantic_degree'] = data_form.loc[i,'romantic_degree'] + 0.25
            continue
        if (j=='Film-Noir'):
            data_form.loc[i,'pessimistic_degree'] = data_form.loc[i,'pessimistic_degree'] + 1
            data_form.loc[i,'terror_degree'] = data_form.loc[i,'terror_degree'] + 0.25
            continue
        if (j=='Horror'):
            data_form.loc[i,'terror_degree'] = data_form.loc[i,'terror_degree'] + 1
            data_form.loc[i,'pessimistic_degree'] = data_form.loc[i,'pessimistic_degree'] + 0.25
            continue
        if (j=='Musical'):
            data_form.loc[i,'romantic_degree'] = data_form.loc[i,'romantic_degree'] + 0.5
            continue
        if (j=='Mystery'):
            data_form.loc[i,'brain_degree'] = data_form.loc[i,'brain_degree'] + 1
            continue
        if (j=='Romance'):
            data_form.loc[i,'romantic_degree'] = data_form.loc[i,'romantic_degree'] + 1
            continue
        if (j=='Sci-Fi'):
            data_form.loc[i,'brain_degree'] = data_form.loc[i,'brain_degree'] + 0.25
            continue
        if (j=='Thriller'):
            data_form.loc[i,'terror_degree'] = data_form.loc[i,'terror_degree'] + 1
            data_form.loc[i,'brain_degree'] = data_form.loc[i,'brain_degree'] + 0.25
            continue
        if (j=='War'):
            data_form.loc[i,'action_degree'] = data_form.loc[i,'action_degree'] + 1
            continue
        if (j=='Western'):
            data_form.loc[i,'brain_degree'] = data_form.loc[i,'brain_degree'] + 0.25
            continue
            
file=os.path.dirname(os.path.abspath('__file__'))   
if(os.path.exists(os.path.join(file,'movies_info.csv'))):#如果输出结果表格已经存在，则删除
    os.remove(os.path.join(file,'movies_info.csv'))
data_form.to_csv('movies_info.csv',index=False,encoding='utf_8')        





