# -*- coding: utf-8 -*-

import pandas as pd


from pandas import Series,DataFrame

import os

#导入数据(数据库中导入)
    
print(os.path.dirname(os.path.abspath('__file__')))#返回代码所在目录
file=os.path.dirname(os.path.abspath('__file__'))
data_file=os.path.join(file,'second_house_complete.csv')#返回数据所在文件位置
print(data_file)
df=pd.read_csv(data_file,engine='python',encoding='gb18030')
'''
print(os.path.dirname(os.path.abspath('__file__')))#返回代码所在目录
file=os.path.dirname(os.path.abspath('__file__'))
data_file=os.path.join(file,'second_house_new_clear.csv')#返回数据所在文件位置
print(data_file)
df=pd.read_csv(data_file,engine='python',encoding='gb18030')
'''
features=df[['浏览量','房屋标题','核心卖点','房屋总价','元/平','房本面积','室','厅','卫','房屋朝向num','楼层高低num','楼层层数num','装修情况num','产权年限num','建筑年代num','参考首付num','月供num','小区均价num','所在商圈1num','所在商圈2num']]
X=features
length=len(X['房屋标题'])
for i in range(0,10):
    df['recommend'+str(i)]=[0]*length
index={
   'value':['房屋总价','元/平','房本面积','室','厅','卫','楼层层数num','产权年限num','建筑年代num','参考首付num','月供num','小区均价num'],
   'OneHot':['所在商圈1num','所在商圈2num','房屋朝向num','楼层高低num','装修情况num'],
   'txt':['房屋标题','核心卖点'],
   'clicks':['浏览量'],
   'predict_x':['房本面积','室','厅','卫','房屋朝向num','楼层高低num','楼层层数num','装修情况num','产权年限num','建筑年代num','参考首付num','月供num','小区均价num','所在商圈1num','所在商圈2num'],
   'predict_y':['房屋总价'],
   'weight_value':[1.2,1.3,1.2,0.8,0.5,0.5,0.5,0.7,0.5,0.8,1.1,1.1],
   'weight_OneHot':[1,1,1,1,1],
   'weight_txt':[0.8,1.2],
   'weight_part':[1.5,0.4,0.2,0.2,0.2]#各部分的权重（连续属性，离散属性，文本，性价比,点击量）       
   } 
