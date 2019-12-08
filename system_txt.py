import jieba
from gensim import corpora,models,similarities
import numpy as np 
import os
import pandas as pd
import math



def distance(X,length):
    
    stopword_list = [line.strip() for line in open('stopword_system.txt').readlines() ]#导入停用词
    #分词
    all_doc = []
    all_doc=[X.iloc[i] for i in range(0,len(X))]
    
    '''
    s.iloc[0]：按位置选取数据
    s.loc[0]：按索引选取数据
    '''
    
    '''
    try:
        all_doc=[X.loc[i] for i in range(0,len(X))]
    
    except KeyError:
        print(X.loc[0].index)
        index = X.loc[0].index[0]
        all_doc=[X.loc[i][index] for i in range(0,len(X))]
    '''
    all_doc_list = []
    for doc in all_doc:
        doc_list = [word for word in jieba.cut(doc) if word not in stopword_list]
        all_doc_list.append(doc_list)
    
    #print(all_doc_list)
    
    doc_test=X[length]
    doc_test_list = [word for word in jieba.cut(doc_test) if word not in stopword_list]
    
    
    #制作语料库
    dictionary = corpora.Dictionary(all_doc_list)
    corpus = [dictionary.doc2bow(doc) for doc in all_doc_list]
    
    
    doc_test_vec = dictionary.doc2bow(doc_test_list)
    
    #相似度分析
    
    tfidf = models.TfidfModel(corpus)
    
    index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=len(dictionary.keys()))
    sim = index[tfidf[doc_test_vec]]
    list_sim=sorted(enumerate(sim), key=lambda item: item[0])#item[1]:以sim[1]为排序标准，-item[1]:负为降序
    #enumerate() 函数用于将一个可遍历的数据对象(如列表、元组或字符串)组合为一个索引序列，同时列出数据和数据下标
#    list_sim=[(i[0]+1,i[1]) for i in list_sim]
    return (list_sim)

def similar_txt(X,length,index):
    '''
    #导入数据
#    print(os.path.dirname(os.path.abspath('__file__')))#返回代码所在目录
    file=os.path.dirname(os.path.abspath('__file__'))
    data_file=os.path.join(file,'second_house_new_clear.csv')#返回数据所在文件位置
#    print(data_file)
    df=pd.read_csv(data_file,engine='python',encoding='gb18030')
    '''
    
    stopword_list = [line.strip() for line in open('stopword_system.txt').readlines() ]#导入停用词
    
    
      
    list_column=[column for column in X]

    names = globals()#此处需要用globals，全局变量，用locals局部变量会出错
    for column in list_column:   
        names['list_sim' + str(list_column.index(column)) ] = distance(X[column],length)

#    list_test=[(list_sim0[i][1],list_sim1[i][1]) for i in range(0,len(list_sim0))]
#    print(list_test)
    
    
        #两个相似度的值求平方根
    list_sim=[(0,0)]*len(list_sim0)
    for j in range(0,len(list_column)):
        list_sim=[(names['list_sim' + str(j) ][i][0],-math.sqrt((list_sim[i][1])**2+(index[j]*names['list_sim' + str(j) ][i][1])**2)) for i in range(0,len(names['list_sim' + str(j) ]))]
#            list_sim=[(list_sim0[i][0],math.sqrt((0.5*list_sim0[i][1])**2+(1.5*list_sim1[i][1])**2)) for i in range(0,len(list_sim1))]
    #    list_sim=sorted(list_sim,key=lambda item: -item[1])
    
    #归一化处理
    max_sim=np.amax(list_sim, axis=0)[1]
    min_sim=np.amin(list_sim, axis=0)[1]
    list_sim=[(list_sim[i][0],(list_sim[i][1]-min_sim)/(max_sim-min_sim)) for i in range(0,len(names['list_sim' + str(j) ]))]
    return(list_sim)

if __name__ == '__main__':
    
        #导入数据
#    print(os.path.dirname(os.path.abspath('__file__')))#返回代码所在目录
    file=os.path.dirname(os.path.abspath('__file__'))
    data_file=os.path.join(file,'second_house_new_clear.csv')#返回数据所在文件位置
#    print(data_file)
    df=pd.read_csv(data_file,engine='python',encoding='gb18030')
    features=df[['房屋标题','核心卖点']]
#    features=df[['房屋标题','核心卖点','房屋总价','元/平','房本面积','室','厅','卫','房屋朝向num','楼层高低num','楼层层数num','装修情况num','产权年限num','建筑年代num','参考首付num','月供num','小区均价num','所在商圈1num','所在商圈2num']]
    X=features
    length=len(X['房屋标题'])
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
    
    '''
            #导入数据
#    print(os.path.dirname(os.path.abspath('__file__')))#返回代码所在目录
    file=os.path.dirname(os.path.abspath('__file__'))
    data_file=os.path.join(file,'movies_info.csv')#返回数据所在文件位置
#    print(data_file)
    df=pd.read_csv(data_file,engine='python',encoding='utf_8')
    features=df[['title']]
#    features=df[['房屋标题','核心卖点','房屋总价','元/平','房本面积','室','厅','卫','房屋朝向num','楼层高低num','楼层层数num','装修情况num','产权年限num','建筑年代num','参考首付num','月供num','小区均价num','所在商圈1num','所在商圈2num']]
    X=features
    length=len(X['title'])
    index={
       'txt':['title'],      
       'weight_txt':[1], 
       }
    X.loc[length,:]=X.loc[1,:].copy()
    list_sim=similar_txt(X,length,index['weight_txt'])
    print("排序前：")
    print(list_sim[0:10])
    list_sim=sorted(list_sim,key=lambda item: item[1])
    print("排序后：")
    print(list_sim[0:10])
    '''
