# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 11:50:34 2019

@author: Administrator
"""
import math
import numpy as np 
import pandas as pd
from pandas import Series,DataFrame

import pymysql#导入数据库的数据集

#基于连续属性相似的推荐距离系统


#基于机器学习模型得到的性价比的推荐距离系统
import second_house_model

#基于点击量得到的推荐距离系统
import clicks


def distance(X,length):
    
    index={
       'clicks':['浏览量'],
       'predict_x':['房本面积','室','厅','卫','房屋朝向num','楼层高低num','楼层层数num','装修情况num','产权年限num','建筑年代num','参考首付num','月供num','小区均价num','所在商圈1num','所在商圈2num'],
       'predict_y':['房屋总价'],
       'weight_part':[1,1]#各部分的权重（性价比,点击量）       
       } 
    
    
    

       
    #*-*-*性价比*-*-*
    #基于预测价格的推荐距离，只用执行一次，所以只用在i=0时执行即可
    if(index['weight_part'][0]!=0):#但性价比的权重不为0时，执行一次
        x=X.loc[:,index['predict_x']]
        y=np.log(X.loc[:,index['predict_y'][0]])
        distance_price=second_house_model.predict_model(x,y)
        #print(price_distance[0:10])
    if(index['weight_part'][0]==0):#但性价比权重为0时，价格距离都为0
        distance_price=(0,0)*length
        #print(price_distance[0:10])
    
    
    #*-*-*点击量*-*-*
    #基于点击量的推荐距离，只用执行一次，所以只用在num=0时执行即可
    if(index['weight_part'][1]!=0):#但点击量的权重不为0时，执行一次
        distance_click=clicks.click_distance(X,index['clicks'])  
        #print(click_distance[0:10])
    if(index['weight_part'][1]==0):#但性价比权重为0时，价格距离都为0
        distance_click=(0,0)*length
        #print(click_distance[0:10])
    
    
    #*-*-*总体权重分配*-*-*
    list_sim0=[(i,math.sqrt(((index['weight_part'][0]*(distance_price[i][1]))**2+(index['weight_part'][1]*(distance_click[i][1]))**2))) for i in range(0,length)]
    #for i in range(num,len(list_sim0)):
    #list_sim0[i][0]=list_sim0[i][0]+1
    list_sim=sorted(list_sim0, key=lambda item: item[1])#item[1]:以sim[1]为排序标准，-item[1]:负为降序
        #enumerate() 函数用于将一个可遍历的数据对象(如列表、元组或字符串)组合为一个索引序列，同时列出数据和数据下标    
        #list(enumerate(list0))
    print("综合权重后的推荐前11")
    print(list_sim[0:11])
    
    #list_sim，取0到11作为推荐索引，即先取11个，再删去索引num，再取前10个
    list_sim_recommend=[list_sim[i][0] for i in range(0,length)]
    if length in list_sim_recommend:
        list_sim_recommend.remove(length)
    
    return (list_sim_recommend)

    
'''
[(0.482, '单价'), (0.297, '小区均价'), (0.235, '房屋总价'), (0.182, '月供'), (0.172, '参考首付'), 
(0.091, '商圈2'), (0.075, '商圈1'), (0.042, '楼层层数'), (0.018, '楼层高低'), (-0.008, '装修情况'), 
(-0.009, '厅'), (-0.013, '房屋朝向'), (-0.015, '室'), (-0.016, '建筑年代'), (-0.02, '卫'), (-0.074, '房本面积')]    
'''    
    
    
if __name__ == '__main__':
    #导入数据(数据库中导入)
    
    dbconn=pymysql.connect(
    host="localhost",
    database="recommend_system",
    user="root",
    password="lizikang",
    port=3306,
    charset='gb18030'
    )

    #sql语句
    sqlcmd="select * from second_house_new_clear"

    #利用pandas 模块导入mysql数据
    df=pd.read_sql(sqlcmd,dbconn)
    '''
    print(os.path.dirname(os.path.abspath('__file__')))#返回代码所在目录
    file=os.path.dirname(os.path.abspath('__file__'))
    data_file=os.path.join(file,'second_house_new_clear.csv')#返回数据所在文件位置
    print(data_file)
    df=pd.read_csv(data_file,engine='python',encoding='gb18030')
    '''
    features=df.loc[:,['商品id','浏览量','房屋标题','核心卖点','房屋总价','元/平','房本面积','室','厅','卫','房屋朝向num','楼层高低num','楼层层数num','装修情况num','产权年限num','建筑年代num','参考首付num','月供num','小区均价num','所在商圈1num','所在商圈2num']]
    X=features
    length=len(X.loc[:,'商品id'])
    
    

#运行核心函数，得到推荐的10个索引
    list_sim_recommend=distance(X,length)    
    list_sim_10=list_sim_recommend[0:10]
    

    
    
    
    
    
    
    
    
    