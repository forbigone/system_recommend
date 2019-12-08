# -*- coding: utf-8 -*-  
'''
Created on 2017年9月18日
@author: Jason.F
'''
 
import math
import random
import os
from itertools import islice
import pandas as pd
import distance_movies

 
class ItemBasedCF:
    def __init__(self, datafile_user = None, datafile_item = None):
        self.datafile_user = datafile_user
        self.datafile_item = datafile_item
        self.readData()
        self.splitData()
      
    def readData(self,datafile_user = None, datafile_item = None):
        self.datafile_user = datafile_user or self.datafile_user
        self.datafile_item = datafile_item or self.datafile_item
        self.data = []
        self.df = pd.read_csv(self.datafile_item, engine='python', encoding='utf_8')
        self.df = self.df[index['continuous']+index['dispered']+index['txt']+['movies_id']]
        file = open(self.datafile_user,'r')
        for line in islice(file, 1, None): #file.readlines():跳过第一行（start=0），从第二行（start=1）读取数据
            userid, itemid, record = line.split(',')
            self.data.append((userid,itemid,float(record)))
        
     
    def abc(self):
        return(self.df)                        
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
                              
    def recommend(self,user,train = None, k = 10,nitem = 5):  #user为用户序号，k为跟i最相似的k个物品；nitem为最终推荐的5个物品
        train = train or self.traindata
        rank = dict()
        ru = train.get(user,{})  #取出与user=345相关的数据,没有键345，只剩键345对应的键值{}
        for i,pi in ru.items():  #转化为dict_items类型，即物品i，以及i的评分。  i为物品，pi为用户user对物品i的评分（对于隐反馈，此处pi=1）
            item_i_j = sorted(self.itemSim[i].items(), key = lambda x:x[1], reverse = True)[0:k] #根据相似度矩阵对物品i的相似物品j进行排序，wj是相似值，得到前K个物品
            
            #属性相似计算
            list_sim_tf,list_sim = self.similar(i,item_i_j)  #list_sim_tf为属性相似计算是否运行成功,list_sim为运行结果得到i和j的属性相似度 
            
            
            for j in range(len(item_i_j)):                  
                if item_i_j[j][0] in ru:  #过滤掉看过的 if 1 in {1:2}:
                    continue
                rank.setdefault(item_i_j[j][0],0)
                if(list_sim_tf == 1):
                    rank[item_i_j[j][0]] += (pi*item_i_j[j][1]) / list_sim[j][1] #推荐值排序，物品j的评分pi->item_i_j[j][0]，乘以相似值wj->item_i_j[j][1], list_sim[j][1]为物品ij之间的属性相似度
                else:
                    rank[item_i_j[j][0]] += (pi*item_i_j[j][1])  #推荐值排序，物品j的评分pi->item_i_j[j][0]，乘以相似值wj->item_i_j[j][1]
        
        return dict(sorted(rank.items(), key = lambda x:x[1], reverse = True)[0:nitem])  # 对最终的推荐进行排序，返回前nitem个值
    

    def similar(self,i,item_i_j):
        if (int(i) in self.df['movies_id'].values):  #先判断物品i是否在物品库当中
                list_item = []
                for j,wj in item_i_j:
                    list_item.append(int(j))  # 
#                print(list_item)
                df0=self.df[self.df['movies_id'].isin(list_item)]  #提取电影集中id对应的，没有的跳过不提取；此时的index还是原来的默认的index
                print(df0)
                length = len(df0)
                df0.index = range(length)  #将index初始化为0,1,2,3，....
#                print(self.df[self.df['movies_id']==int(i)])
#                print(df0)
                
                df0.loc[length,:]=self.df[self.df['movies_id']==int(i)].iloc[0] #df[df['movies_id']==int(11)]为dataframe格式，需要提取第一行来转换为Series
                sim = distance_movies.distance(df0,index,length,2)
                list_sim = sorted(sim,key=lambda item: item[0])
                list_sim = [(df0.loc[j,"movies_id"],list_sim[j][1]) for j in range(len(list_sim))]
                print(list_sim)
                list_sim_tf = True
        else:
                print("物品i（id=%d）不在物品库当中" %i)  #%d 输出物品i的id
                list_sim_tf = False
        return (list_sim_tf,list_sim)  
    
    
    def recallAndPrecision(self,train = None,test = None,k = 8,nitem = 5):  #准确率（precision）/召回率（recall）度量
        train = train or self.traindata
        test = test or self.testdata
        hit = 0
        recall = 0
        precision = 0
        for user in test.keys():
            tu = test.get(user,{})
            rank = self.recommend(user,train = train,k = k,nitem = nitem)
            for item,_ in rank.items():
                if item in tu:
                    hit += 1
            recall += len(tu)
            precision += nitem
        return (hit / (recall * 1.0),hit / (precision * 1.0))
    
    def coverage(self,train = None,test = None,k = 8,nitem = 5):  #覆盖率（coverage）描述一个推荐系统对物品长尾的发掘能力。
        train = train or self.traindata
        test = test or self.testdata
        recommend_items = set()
        all_items = set()
        for user in test.keys():
            for item in test[user].keys():
                all_items.add(item)
            rank = self.recommend(user, train, k = k, nitem = nitem)
            for item,_ in rank.items():
                recommend_items.add(item)
        return len(recommend_items) / (len(all_items) * 1.0)
    
    def popularity(self,train = None,test = None,k = 8,nitem = 5):  #我们还需要评测推荐的新颖度，这里用推荐列表中物品的平均流行度度量推荐结果的新颖度。
                                                                    #如果推荐出的物品都很热门，说明推荐的新颖度较低，否则说明推荐结果比较新颖。
        train = train or self.traindata
        test = test or self.testdata
        item_popularity = dict()
        for user ,items in train.items():
            for item in items.keys():
                item_popularity.setdefault(item,0)
                item_popularity[item] += 1
        ret = 0
        n = 0
        for user in test.keys():
            rank = self.recommend(user, train, k = k, nitem = nitem)
            for item ,_ in rank.items():
                ret += math.log(1+item_popularity[item])
                n += 1
        return ret / (n * 1.0)
        
    def testRecommend(self,user):
        rank = self.recommend(user,k = 10,nitem = 5)
        for i,rvi in rank.items():
            items = self.traindata.get(user,{})
            record = items.get(i,0)
            print ("%5s: %.4f--%.4f" %(i,rvi,record))
                                
if __name__ == "__main__":
    #数据集1.userld：用户；2.movield：喜欢的电影；3.rating：评分
    
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
    ibc=ItemBasedCF(datafile_user = os.getcwd()+'\\ratings.csv', datafile_item = os.getcwd()+'\\movies_info.csv')#初始化数据
    
    
    df=ibc.abc()

    '''
    s.iloc[0]：按位置选取数据
    s.loc['index_one']：按索引选取数据
    '''

    
    ibc.ItemSimilarity()#计算物品相似度矩阵
    ibc.testRecommend(user = "345") #单用户推荐
    print ("%3s%20s%20s%20s%20s" % ('K',"recall",'precision','coverage','popularity'))
    
    
    
    for k in [5,10,15,20]:
        recall,precision = ibc.recallAndPrecision( k = k)
        
        #coverage =ibc.coverage(k = k)
        #popularity =ibc.popularity(k = k)
        #print ("%3d%19.3f%%%19.3f%%%19.3f%%%20.3f" % (k,recall * 100,precision * 100,coverage * 100,popularity))
        print ("%3d%19.3f%%%19.3f" % (k,recall * 100,precision * 100))
'''
对于数据齐全的用户（已经登录），最完整的做法：基于商品的协同过滤和基于内容相似的混合算法：   
#将rating评分改为基于浏览、购物车、收藏、购买对应的喜爱值，计算商品i，j相似度时，增加i，j的属性相似值（猜你喜欢）
#基于浏览记录的，推测“目标商品”的算法 （猜你在找这个）适合用于购买某种需要深思熟虑的商品，如房子，车子---recommend_user_history.py  和  recommend_user_movies.py
1.用随机抽取检验对比不同方法的准确率和召回率  2.加入时间的惩罚函数
对于新用户（没有登录）
#开始页面：基于点击量和性价比等能反映商品价值的推荐（大家都爱这个）---recommend_user_new.py  ---应对用户冷启动
#某商品页面下，基于协同过滤的算法（看了这个的人，大多还看了）---ItemCF_item.py  ---应对用户冷启动
#某商品页面下，基于商品属性的推荐（跟这个相似的还有）---distance_house.py 和 distance_movies.py  ---应对物品冷启动
'''      
        
        
'''

        #导入数据
#    print(os.path.dirname(os.path.abspath('__file__')))#返回代码所在目录
    file=os.path.dirname(os.path.abspath('__file__'))
    data_file=os.path.join(file,'ratings.csv')#返回数据所在文件位置
#    print(data_file)
    df=pd.read_csv(data_file,engine='python',encoding='utf_8')    
    df.drop(['timestamp'], axis=1,inplace=True)
    
    if(os.path.exists(os.path.join(file,'ratings.csv'))):#如果输出结果表格已经存在，则删除
        os.remove(os.path.join(file,'ratings.csv'))
    df.to_csv('ratings.csv',index=False,encoding='utf_8')
'''