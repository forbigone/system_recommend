# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 11:50:34 2019

@author: Administrator
"""
import math
import numpy as np 
import os
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

'''
def MahalanobisDisSim(x,y):
    
#    马氏距离计算方法
    
    npvec1,npvec2=np.array(x),np.array(y)
    npvec=np.array([npvec1, npvec2])
    sub=npvec.T[0]-npvec.T[1]
    inv_sub=np.linalg.inv(np.cov(npvec1, npvec2))
    return math.sqrt(np.dot(inv_sub, sub).dot(sub.T))
'''

    

def continuous_distance(X,index,length):
    
    #局部变量，常用的lsit长度
    
   
    
    
    #*-*-*连续属性*-*-*
    if(index['weight_part'][0]!=0):
        #归一化
        min_max_scaler = preprocessing.MinMaxScaler()  
        X_minMax = min_max_scaler.fit_transform(X[index['continuous']]) 
        
        X_minMax=DataFrame(X_minMax,columns=index['continuous'])  
        
        #部分权重分配，    权重数值从index['weight_continuous']中获取
        for i in range(0,len(index['weight_continuous'])):
            X_minMax[index['continuous'][i]]*=index['weight_continuous'][i]#对应列乘以index里面的权重
        
        list_distance0=[]
        #small_distance=[]
        for i in range(0,length):
            distance=eculidDisSim(X_minMax.iloc[length,:],X_minMax.iloc[i,:])#计算第num个和剩下的房子数据的欧几里得距离
            #print ('eculidDisSim:',eculidDisSim(X.iloc[0,:],X.iloc[i,:]))
            list_distance0.append(distance)#将所有欧式距离依次存在数组里面
        
        list_distance=list(enumerate(list_distance0))
    if(index['weight_part'][0]==0):
        list_distance=(0,0)*length
    
    
    #归一化处理
    max_sim=np.amax(list_distance, axis=0)[1]
    min_sim=np.amin(list_distance, axis=0)[1]
    list_distance=[(list_distance[i][0],(list_distance[i][1]-min_sim)/(max_sim-min_sim)) for i in range(0,length)]
    return (list_distance)

    
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
    list_sim=continuous_distance(X,index,length)
    print("排序前：")
    print(list_sim[0:10])
    list_sim=sorted(list_sim,key=lambda item: item[1])
    print("排序后：")
    print(list_sim[0:10])    

    
    
    
    
    
    
    