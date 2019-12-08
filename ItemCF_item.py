# -*- coding: utf-8 -*-  
'''
Created on 2017年9月18日
@author: Jason.F
'''
 
import math
import random
import os
from itertools import islice

 
class ItemBasedCF:
    def __init__(self, datafile = None):
        self.datafile = datafile
        self.readData()
        self.splitData()
      
    def readData(self,datafile = None):
        self.datafile = datafile or self.datafile
        self.data = []
        file = open(self.datafile,'r')
        for line in islice(file, 1, None): #file.readlines():跳过第一行（start=0），从第二行（start=1）读取数据
            userid, itemid, record = line.split(',')
            self.data.append((userid,itemid,float(record)))
                              
    def splitData(self,data=None,k=3,M=10,seed=10):
        self.testdata = {}
        self.traindata = {}
        data = data or self.data
        random.seed(seed)#生成随机数10个(0~1)的随机数
        for user,item,record in self.data:
            self.traindata.setdefault(user,{})
            self.traindata[user][item] = record #全量训练{1: {1: 4,3: 4,6: 4,...},2:{318:3,333:4,...},...}
            if random.randint(0,M) == k:#测试集
                self.testdata.setdefault(user,{})
                self.testdata[user][item] = record              
                                  
    def ItemSimilarity(self, train = None):
        train = train or self.traindata   #train是我们得到的数据集
        self.itemSim = dict()  #定义相似度矩阵
        item_user_count = dict() #喜欢某物品的人数统计矩阵（对应公式的N(i))
        count = dict() #同时喜欢i，j物品的人数矩阵（对应公式的N(i)&N(j))
        for user,item in train.items(): #dict_items([(1, {1: 4, 3: 4}), (2, {333: 0})]),每一次遍历只遍历一个用户
            for i in item.keys():  #user:[1,2,3..]  ,item:[{1: 4, 3: 4},{333: 0}]，item.keys():[1,3,...]
                item_user_count.setdefault(i,0)  # 对当前用户的所有商品都建立键值
                item_user_count[i] += 1  # 并统计出现多少次，即多少人喜欢（因为每个人不会重复出现）
                for j in item.keys():
                    count.setdefault(i,{})  # 对当前的i商品建立键值
                    if i == j:
                        continue
                    
                    count[i].setdefault(j,0)  # 在每一个键值中，再对其他每一个商品建立键值； 
                    count[i][j] += 1  # 当前user的同时喜欢i，j商品的人数都初始为0，因为在这个user循环中，就他自己，所以先为0，然后再+1； 而当之前的user的“两个”商品，两个也出现在当前user时，不用初始化，继续+1，此时变成2了
                    
        for i, related_items in count.items():  #i是商品1，related_items是{商品2：共同喜欢人数}
            self.itemSim.setdefault(i,dict())
            for j, cuv in related_items.items():
                self.itemSim[i].setdefault(j,0)
                self.itemSim[i][j] = cuv / math.sqrt(item_user_count[i] * item_user_count[j] * 1.0)  #i,j的相似度
                              
        
    def testRecommend(self,item):
        return self.itemSim[item]
                                
if __name__ == "__main__":
    #数据集1.userld：用户；2.movield：喜欢的电影；3.rating：评分
    ibc=ItemBasedCF(os.getcwd()+'\\ratings.csv')#初始化数据
    ibc.ItemSimilarity()#计算物品相似度矩阵
    dict_sim=ibc.testRecommend(item = "345") #单商品推荐
    list_sim=[(i,dict_sim[i]) for i in dict_sim]
    list_sim=sorted(list_sim, key=lambda item: -item[1])
    print (list_sim[0:10])
    '''
    for k in [5,10,15,20]:
        recall,precision = ibc.recallAndPrecision( k = k)
        coverage =ibc.coverage(k = k)
        popularity =ibc.popularity(k = k)
        print ("%3d%19.3f%%%19.3f%%%19.3f%%%20.3f" % (k,recall * 100,precision * 100,coverage * 100,popularity))
    '''    
