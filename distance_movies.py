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

from pandas import Series,DataFrame


#基于连续属性相似的推荐距离系统
import continuous

#基于连续属性相似的推荐距离系统
import dispersed

#基于文本相似度的文本推荐距离系统
import system_txt


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
#独热化
def OneHot(X):    
    enc=preprocessing.OneHotEncoder().fit(X)
    X_encoded=enc.transform(X).toarray()
    return(X_encoded)
    

def distance(X,index,length,list_return):
    
    #局部变量，常用的lsit长度
    
    

       
    #*-*-*离散属性独热化*-*-*
    if(index['weight_part'][1]!=0):#当离散属性权重不为0时，计算离散属性推荐距离
        distance_dispersed=dispersed.dispersed_distance(X,index,length)        
    if(index['weight_part'][1]==0):
        distance_dispersed=[(0,0)]*length
    print('*-*-*离散属性独热化*-*-*')
    print(distance_dispersed[0:10])
    
    
    #*-*-*文本*-*-*
    if(index['weight_part'][2]!=0):#当文本权重不为0时，计算文本推荐距离
        distance_txt=system_txt.similar_txt(X[index['txt']],length,index['weight_txt'])
    if(index['weight_part'][2]==0):
        distance_txt=[(0,0)]*length
    print('*-*-*文本*-*-*')
    print(distance_txt[0:10])
    
    
    
    #*-*-*连续属性*-*-*
    if(index['weight_part'][0]!=0):#当连续属性权重不为0时，计算连续属性推荐距离
        distance_continuous=continuous.continuous_distance(X,index,length)
    if(index['weight_part'][0]==0):
        distance_continuous=[(0,0)]*length
    print('*-*-*连续属性*-*-*')
    print(distance_continuous[0:10])
    
    
    #*-*-*总体权重分配*-*-*
    list_sim0=[(i,math.sqrt((index['weight_part'][0]*distance_continuous[i][1])**2+(index['weight_part'][1]*distance_dispersed[i][1])**2+(index['weight_part'][2]*(distance_txt[i][1]))**2)) for i in range(0,length)]
    #for i in range(num,len(list_sim0)):
    #list_sim0[i][0]=list_sim0[i][0]+1
    list_sim=sorted(list_sim0, key=lambda item: item[1])#item[1]:以sim[1]为排序标准，-item[1]:负为降序
        #enumerate() 函数用于将一个可遍历的数据对象(如列表、元组或字符串)组合为一个索引序列，同时列出数据和数据下标    
        #list(enumerate(list0))
    print("综合权重后的推荐前11")
    print(list_sim[0:11])
    
    if(list_return == 2):
        return (list_sim)
    #list_sim，取0到11作为推荐索引，即先取11个，再删去索引num，再取前10个
    list_sim_recommend=[list_sim[i][0] for i in range(0,length)]
    if length in list_sim_recommend:
        list_sim_recommend.remove(length)
    if (list_return == 1):
        return (list_sim_recommend)

    
'''
[(0.482, '单价'), (0.297, '小区均价'), (0.235, '房屋总价'), (0.182, '月供'), (0.172, '参考首付'), 
(0.091, '商圈2'), (0.075, '商圈1'), (0.042, '楼层层数'), (0.018, '楼层高低'), (-0.008, '装修情况'), 
(-0.009, '厅'), (-0.013, '房屋朝向'), (-0.015, '室'), (-0.016, '建筑年代'), (-0.02, '卫'), (-0.074, '房本面积')]    
'''    
    
    
if __name__ == '__main__':
#导入数据(数据库中导入)
        
    
    
    print(os.path.dirname(os.path.abspath('__file__')))#返回代码所在目录
    file=os.path.dirname(os.path.abspath('__file__'))
    data_file=os.path.join(file,'movies_info.csv')#返回数据所在文件位置
    print(data_file)
    df=pd.read_csv(data_file,engine='python',encoding='utf_8')
    
    features=df[['movies_id','title','release_date','Action','Adventure','Animation',"Children",'Comedy','Crime','Documentary','Drama','Fantasy','Film-Noir','Horror','Musical','Mystery','Romance','Sci-Fi','Thriller','War','Western','pessimistic_degree','optimism_degree','action_degree','child_degree','terror_degree','romantic_degree','brain_degree']]
    X=features
    length=len(X['movies_id'])

    index={
       'continuous':['release_date','pessimistic_degree','optimism_degree','action_degree','child_degree','terror_degree','romantic_degree','brain_degree'],
       'dispered':['Action','Adventure','Animation',"Children",'Comedy','Crime','Documentary','Drama','Fantasy','Film-Noir','Horror','Musical','Mystery','Romance','Sci-Fi','Thriller','War','Western'],
       'txt':['title'],
       'clicks':[],
       'predict_x':[],
       'predict_y':[],
       'weight_continuous':[1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0],
       'weight_dispered':[1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0],
       'weight_txt':[1],
       'weight_part':[1.0,1.0,0.5,0,0]#各部分的权重（连续属性，离散属性，文本，性价比,点击量）       
       } 
        
    
    #运行核心函数，得到推荐的10个索引
    X.loc[length,:]=X.loc[1,:].copy()
    list_sim_recommend=distance(X,index,length,1)
    list_sim_recommend.remove(1)#去掉第i个
    list_sim_10=list_sim_recommend[0:10]


    
    
    
    
    
    
    
    