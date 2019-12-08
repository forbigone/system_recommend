# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 11:50:34 2019

@author: Administrator
"""
import math
import numpy as np 
import pandas as pd
from sklearn import preprocessing 
import re
from pandas import Series,DataFrame

import pymysql#导入数据库的数据集


def eculidDisSim(x,y):
    '''
    欧几里得相似度计算方法
    '''
    return math.sqrt(sum(pow(a-b,2) for a,b in zip(x,y)))


#独热化
def OneHot(X):    
    enc=preprocessing.OneHotEncoder(categories='auto').fit(X)
    X_encoded=enc.transform(X).toarray()
    return(X_encoded)
    '''
    FutureWarning: The handling of integer data will change in version 0.22. Currently, the categories are determined based on the range [0, max(values)], while in the future they will be determined based on the unique values.
    If you want the future behaviour and silence this warning, you can specify “categories=‘auto’”.
    In case you used a LabelEncoder before this OneHotEncoder to convert the categories to integers, then you can now use the OneHotEncoder directly.
    '''

def dispersed_distance(X,index,length):
    
    #局部变量，常用的lsit长度
    
    
    X=X.loc[:,index['dispered']]
    #将测试数据加在原数据最后一行
    

       
    #*-*-*离散属性独热化*-*-*
    list_distance_onehot=[0]*length
    if(index['weight_part'][1]!=0):
        
        for i in range(0,len(index['dispered'])):
            #独热化                
            X_encoded=OneHot(X[[index['dispered'][i]]])
            list_distance_onehot0=[]
            for j in range(0,length):
                #独热化后，计算欧氏距离
                distance_onehot=eculidDisSim(X_encoded[length,:],X_encoded[j,:])
                list_distance_onehot0.append(distance_onehot)
            #部分权重分配       权重数值从index['weight_dispered']中获取
            list_distance_onehot=[math.sqrt((list_distance_onehot[k])**2+(index['weight_dispered'][i]*list_distance_onehot0[k])**2) for k in range(0,length)]
        list_distance_onehot=list(enumerate(list_distance_onehot))
    #    print('--------')
    #    print(list_distance_onehot[0:10])
        
        #归一化处理
        max_sim=np.amax(list_distance_onehot, axis=0)[1]
        min_sim=np.amin(list_distance_onehot, axis=0)[1]
        list_distance_onehot=[(list_distance_onehot[i][0],(list_distance_onehot[i][1]-min_sim)/(max_sim-min_sim)) for i in range(0,length)]
    #    print(enc.transform(X[index['dispered']]))
    #    print(X_encoded)
    

    return (list_distance_onehot)

    
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
    
    
    features=df[['浏览量','房屋标题','核心卖点','房屋总价','元/平','房本面积','室','厅','卫','房屋朝向num','楼层高低num','楼层层数num','装修情况num','产权年限num','建筑年代num','参考首付num','月供num','小区均价num','所在商圈1num','所在商圈2num']]
    X=features
    length=len(X['房屋标题'])
    for i in range(0,10):
        df['recommend'+str(i)]=[0]*length
    index={
       'continuous':['房屋总价','元/平','房本面积','室','厅','卫','楼层层数num','产权年限num','建筑年代num','参考首付num','月供num','小区均价num'],
       'dispered':['所在商圈1num','所在商圈2num','房屋朝向num','楼层高低num','装修情况num'],
       'txt':['房屋标题','核心卖点'],
       'clicks':['浏览量'],
       'predict_x':['房本面积','室','厅','卫','房屋朝向num','楼层高低num','楼层层数num','装修情况num','产权年限num','建筑年代num','参考首付num','月供num','小区均价num','所在商圈1num','所在商圈2num'],
       'predict_y':['房屋总价'],
       'weight_continuous':[1.2,1.3,1.2,0.8,0.5,0.5,0.5,0.7,0.5,0.8,1.1,1.1],
       'weight_dispered':[1,1,1,1,1],
       'weight_txt':[0.8,1.2],
       'weight_part':[1.5,0.4,0.2,0.2,0.2]#各部分的权重（连续属性，离散属性，文本，性价比,点击量）       
       } 
    X.loc[length,:]=X.loc[0,:].copy()
    list_sim=dispersed_distance(X,index,length)
    print("排序前：")
    print(list_sim[0:10])
    list_sim=sorted(list_sim,key=lambda item: item[1])
    print("排序后：")
    print(list_sim[0:10])

    
    
    
    
    
    
    
    
    
    