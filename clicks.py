import numpy as np 
import os
import pandas as pd
import math


def click_distance(X,index):
    '''
    #导入数据
#    print(os.path.dirname(os.path.abspath('__file__')))#返回代码所在目录
    file=os.path.dirname(os.path.abspath('__file__'))
    data_file=os.path.join(file,'second_house_new_clear.csv')#返回数据所在文件位置
#    print(data_file)
    df=pd.read_csv(data_file,engine='python',encoding='gb18030')
    '''
    
     

    list_sim0=X[index[0]]
    length=len(list_sim0)
    list_sim0=[-list_sim0[i] for i in range(0,length)]
    list_sim=list(enumerate(list_sim0))
    
    #归一化处理
    max_sim=np.amax(list_sim, axis=0)[1]
    min_sim=np.amin(list_sim, axis=0)[1]
    list_sim=[(list_sim[i][0],(list_sim[i][1]-min_sim)/(max_sim-min_sim)) for i in range(0,length)]
    
    
    return(list_sim)

if __name__ == '__main__':
        #导入数据
#    print(os.path.dirname(os.path.abspath('__file__')))#返回代码所在目录
    file=os.path.dirname(os.path.abspath('__file__'))
    data_file=os.path.join(file,'second_house_new_clear.csv')#返回数据所在文件位置
#    print(data_file)
    df=pd.read_csv(data_file,engine='python',encoding='gb18030')
    features=df[['浏览量']]
#    features=df[['房屋标题','核心卖点','房屋总价','元/平','房本面积','室','厅','卫','房屋朝向num','楼层高低num','楼层层数num','装修情况num','产权年限num','建筑年代num','参考首付num','月供num','小区均价num','所在商圈1num','所在商圈2num']]
    X=features
    index={
       'continuous':['房屋总价','元/平','房本面积','室','厅','卫','楼层层数num','产权年限num','建筑年代num','参考首付num','月供num','小区均价num'],
       'dispered':['所在商圈1num','所在商圈2num','房屋朝向num','楼层高低num','装修情况num'],
       'txt':['房屋标题','核心卖点'],
       'clicks':['浏览量'],
       'weight_continuous':[1.2,1.3,1.2,0.8,0.5,0.5,0.5,0.7,0.5,0.8,1.1,1.1],
       'weight_dispered':[1,1,1,1],
       'weight_txt':[0.8,1.2],
       'weight_part':[1.5,0.8,0.2,0.2],#各部分的权重（属性，文本，性价比,点击量）
       'predict_x':['房本面积','室','厅','卫','房屋朝向num','楼层高低num','楼层层数num','装修情况num','产权年限num','建筑年代num','参考首付num','月供num','小区均价num','所在商圈1num','所在商圈2num'],
       'predict_y':['房屋总价']
       } 
    list_sim=click_distance(X,index['clicks'])
    list_sim=sorted(list_sim,key=lambda item: item[1])

