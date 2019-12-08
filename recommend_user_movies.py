# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import pymysql
from sklearn import preprocessing 
from pandas import Series,DataFrame
import os

import system_txt
import distance_movies
import recommend_user_new


def user_history(X,index,list_user):
    
    #初始化
    X_value=X.loc[0,:].copy()
    X_continuous_weigth=X.loc[0,index['continuous']].copy()
    X_dispered_weigth=X.loc[0,index['dispered']].copy()
    X_txt_weigth=X.loc[0,index['txt']].copy()
    X_clicks_weigth=X.loc[0,index['clicks']].copy()
    X_weight_part=[0,0,0,0,0] 
    
    
    #continuous连续属性
    #continuous
    X_value.loc[index['continuous']]=X.loc[list_user,index['continuous']].mean()#取平均值
    #weight
    min_max_scaler = preprocessing.MinMaxScaler()#归一化  
    X_minMax = min_max_scaler.fit_transform(X[index['continuous']+index['clicks']])       
    X_minMax=DataFrame(X_minMax,columns=index['continuous']+index['clicks'])  
    X_continuous_weigth.loc[index['continuous']]=X_minMax.loc[list_user,index['continuous']].std()#取标准差
    
    sum_X_weigth_continuous=sum(X_continuous_weigth.loc[index['continuous']])#取标准差作为权重初始标准
    X_weight_part[0]=sum_X_weigth_continuous       
    #某一属性标准差越大，其所占权重越小
    for i in range(0,len(index['continuous'])):
        X_continuous_weigth.loc[index['continuous'][i]]=(sum_X_weigth_continuous-X_continuous_weigth.loc[index['continuous'][i]]/sum_X_weigth_continuous)**4
    
    
    
    
    
    
    #dispered离散属性
    #value
    X_value.loc[index['dispered']]=X.loc[list_user,index['dispered']].mode().iloc[0,:]#取众数
    #weight
    for i in range(0,len(index['dispered'])):#取记录离散个数/总离散个数
        X_dispered_weigth.loc[index['dispered'][i]]=len(set(X.loc[list_user,index['dispered'][i]])) / len(set(X.loc[:,index['dispered'][i]]))
    sum_X_weigth_dispered=sum(X_dispered_weigth.loc[index['dispered']]) 
    X_weight_part[1]=sum_X_weigth_dispered
    for i in range(0,len(index['dispered'])): #取倒数，作为权重值   
        X_dispered_weigth.loc[index['dispered'][i]]=1/X_dispered_weigth.loc[index['dispered'][i]]
    sum_X_weigth_dispered=sum(X_dispered_weigth.loc[index['dispered']])      
    for i in range(0,len(index['dispered'])):#占sum和的比例，作为权重
        X_dispered_weigth.loc[index['dispered'][i]]=X_dispered_weigth.loc[index['dispered'][i]]/sum_X_weigth_dispered     
    
    
    
    
    
    
    
    #txt文本
    #value
    for i in range(0,len(index['txt'])):
        X_value.loc[index['txt'][i]]=''
    for i in list_user:
        X_value.loc[index['txt']]+=X.loc[i,index['txt']]#将记录文本拼接成一个文本
    #weight
    length_list_user = len(list_user)
    X_txt=X.loc[list_user,index['txt']]
    X_txt.index=Series(range(0,len(list_user)))#重新定义列名
    #两两求文本相似度，再取平均值最为权重标准
    names = globals()
    for i in range(0,len(index['txt'])):
        names['list'+str(i)]=[]
    for i in range(0, length_list_user):
        for j in range(0,len(index['txt'])):
#            print(index['txt'][j])
            a=system_txt.distance(X_txt.loc[:,index['txt'][j]],i)#两两求文本相似度
         
            for k in a:
                names['list'+str(j)].append(k[1])
#            print(names['list'+str(j)])
            del(names['list'+str(j)][i+(length_list_user-1)*i])#删去自己的文本相似度
    
     
    for i in range(0,len(index['txt'])):
        b=0
        for l in names['list'+str(i)]:
            b+=l 
        X_txt_weigth.loc[index['txt'][i]]=b/len(names['list'+str(i)]) #求平均
    
    sum_X_weigth_txt=sum(X_txt_weigth.loc[index['txt']])
    X_weight_part[2]=sum_X_weigth_txt      
    for i in range(0,len(index['txt'])):
        X_txt_weigth.loc[index['txt'][i]]=X_txt_weigth.loc[index['txt'][i]]*len(index['txt'])/sum_X_weigth_txt        
               
    
    #clicks点击量
    X_value.loc[index['clicks']]=X.loc[list_user,index['clicks']].mean()    
    X_clicks_weigth.loc[index['clicks']]=X_minMax.loc[list_user,index['clicks']].std()
    
    
    #连续属性权重分配，大致区间[0.5,1.6]【0.5,2】
    X_weight_part[0]=-1.36*X_weight_part[0]+2.68 
    #离散属性权重分配，大致区间[0.8,2]【0.5,2】
    X_weight_part[1]=-1.25*X_weight_part[1]+3 
    #文本属性权重分配，大致区间[0.05,0.15-]【0.5,2】
    X_weight_part[2]=15*X_weight_part[2]-0.25      
    '''
    if (X_weight_part[0]<=0.6): 
        X_weight_part[0]=-4*X_weight_part[0]+4    
    elif(X_weight_part[0]<=1):
        X_weight_part[0]=-2*X_weight_part[0]+2.8
    elif(X_weight_part[0]>1):
        X_weight_part[0]=-0.3*X_weight_part[0]+1.1
    '''       
    return(X_value,X_continuous_weigth,X_dispered_weigth,X_txt_weigth,X_weight_part)    
               
if __name__=='__main__':          
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
    
    #利用pandas 模块导入mysql数据
    data_file=os.path.join(file,'ratings.csv')#返回数据所在文件位置
    df_user=pd.read_csv(data_file,engine='python',encoding='utf_8')
    #用户浏览记录list
    user_list=list(set(df_user['userId'].tolist()))
    history_list=df_user[df_user['userId']==user_list[0]]['movieId'].tolist()  #0表示提取第一个用户浏览信息
    for i in range(0,len(history_list)):#将用户记录中的商品id转换为对应的行数（索引index）,转换为普通列表格式时用tolist()方法
        history_list[i]=X[X['movies_id']==history_list[i]].index.tolist()[0]
    
    
    
    #对于没有浏览记录的新用户
    if(len(history_list)==0):
        list_sim_recommend=recommend_user_new.distance(X,length)
     
    #用户只有一个浏览记录时
    if(len(history_list)==1):
        X.loc[length,:]=X.loc[history_list[0],:].copy()
        #distance_price=[(0,0)]*length
        #distance_click=[(0,0)]*length
        list_sim_recommend=distance_movies.distance(X,index,length,1)
        list_sim_recommend.remove(history_list[0])
    
    #用户浏览记录在2以上
    if(len(history_list)>1):
        #求出属性值，以及权重      
        X_value,X_continuous_weigth,X_dispered_weigth,X_txt_weigth,X_weight_part=user_history(X,index,history_list)       
        #修改index的权重
        index['weight_continuous']=X_continuous_weigth.values
        index['weight_dispered']=X_dispered_weigth.values.astype(np.float64)#这里的数组类型dtype=object，需要强制转换为float
        index['weight_txt']=X_txt_weigth.values.astype(np.float64)#这里的数组类型dtype=object，需要强制转换为float
        index['weight_part']=X_weight_part
        
        X.loc[length,:]=X_value.copy()
        #distance_price=[(0,0)]*length
        #distance_click=[(0,0)]*length
        #list_sim_recommend=distance_house.distance(X,index,length,distance_price,distance_click)  #套用二手房的distance_house.py依旧能得到一样的推荐结果
        list_sim_recommend=distance_movies.distance(X,index,length,1)  # 用distance_movies.py
        for i in history_list:
            if i in list_sim_recommend:
                list_sim_recommend.remove(i)
    
    #商品id推荐列表list
    id_recommend=X.loc[list_sim_recommend,'movies_id'].tolist()#转换为普通列表格式时用tolist()方法
        
        
        
        
        
    '''
    file=os.path.dirname(os.path.abspath('__file__'))   
    df.insert(0,'商品id',range(10000000,10000000+length))
    if(os.path.exists(os.path.join(file,'second_house_complete.csv'))):#如果输出结果表格已经存在，则删除
        os.remove(os.path.join(file,'second_house_complete.csv'))
    df.to_csv('second_house_complete.csv',index=False,encoding='utf_8_sig')
    '''