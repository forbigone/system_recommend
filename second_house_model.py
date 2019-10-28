import numpy as np
import pandas as pd
import math
import os

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline

import time

from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.ensemble import RandomForestRegressor


def power(a,b):
		s=a**b
		return s

def polynomial_model(degree=1):
    polynomial_features = PolynomialFeatures(degree=degree, include_bias=False)
    linear_regression = LinearRegression(normalize=True)
    pipeline = Pipeline([("polynomial_features", polynomial_features), ("linear_regression", linear_regression)])
    return pipeline


def predict_model_4(X,Y):
    #训练模型
    from sklearn.model_selection import train_test_split
    
    #选20%的样本作为测试数据集
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=4)
    model1=DecisionTreeRegressor(max_depth=3)#树最大深度,默认gini指数    
    model2=GradientBoostingRegressor(n_estimators=30)
    model3=AdaBoostRegressor(model1,n_estimators=10)
    model4 = RandomForestRegressor(n_estimators=100, random_state=10)
    
    model1.fit(X_train,Y_train)
    model2.fit(X_train,Y_train)
    model3.fit(X_train,Y_train)
    model4.fit(X_train,Y_train)
    train_score = model1.score(X_train, Y_train)
    cv_score = model1.score(X_test, Y_test)
    #elaspe 模型的训练时间
    #train_score 对训练样本拟合的好坏程度
    #cv_score 对测试样本的得分
    print('train_score1: {0:.6f}; cv_score1: {1:0.6f}'.format(train_score, cv_score))
    
    train_score = model2.score(X_train, Y_train)
    cv_score = model2.score(X_test, Y_test)
    #elaspe 模型的训练时间
    #train_score 对训练样本拟合的好坏程度
    #cv_score 对测试样本的得分
    print('train_score2: {0:.6f}; cv_score2: {1:0.6f}'.format(train_score, cv_score))
    
    train_score = model3.score(X_train, Y_train)
    cv_score = model3.score(X_test, Y_test)
    #elaspe 模型的训练时间
    #train_score 对训练样本拟合的好坏程度
    #cv_score 对测试样本的得分
    print('train_score3: {0:.6f}; cv_score3: {1:0.6f}'.format(train_score, cv_score))
    
    train_score = model4.score(X_train, Y_train)
    cv_score = model4.score(X_test, Y_test)
    #elaspe 模型的训练时间
    #train_score 对训练样本拟合的好坏程度
    #cv_score 对测试样本的得分
    print('train_score4: {0:.6f}; cv_score4: {1:0.6f}'.format(train_score, cv_score))
    
    Y_predict1=model1.predict(X)
    Y_predict2=model2.predict(X)
    Y_predict3=model3.predict(X)
    Y_predict4=model4.predict(X)
def predict_model(X,Y):


    #训练模型
    from sklearn.model_selection import train_test_split
    
    #选20%的样本作为测试数据集
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=4)
    
    #训练模型并测试模型的准确性评分

    #模型优化
    #将数据归一化处理（创建线性回归模型时增加normalize=True参数）
    model1=DecisionTreeRegressor(max_depth=3)#树最大深度,默认gini指数 
    model3=AdaBoostRegressor(model1,n_estimators=10)
    #优化欠拟合的方法：1、挖掘更多的输入特征，2、增加多项式特征
    #此处采用增加多项式特征的方法     
    
    
    
    
    model3.fit(X_train,Y_train)
    train_score = model3.score(X_train, Y_train)
    cv_score = model3.score(X_test, Y_test)
    #elaspe 模型的训练时间
    #train_score 对训练样本拟合的好坏程度
    #cv_score 对测试样本的得分
    print('train_score3: {0:.6f}; cv_score3: {1:0.6f}'.format(train_score, cv_score))
    Y_predict3=model3.predict(X)
    
#    X['price_predict1']=Y_predict3
    list_price_predict=list(enumerate(Y_predict3))
#    print(power(math.e, list_price_predict[238][1]))
    length=len(list_price_predict)
    #list_price_predict原价格与预测价格的价格差.
    #***注意***这里采用的是预测-原价格，因为要推荐的，需要是最小的，即推荐距离要最小，所以取反，归一化后，越性价比的越小
    #list_predict原价格与预测价格的价格差与原价格的比
    list_price_predict=[(list_price_predict[i][0],Y[i]-list_price_predict[i][1]) for i in range(0,length)]    
    list_predict=[(list_price_predict[i][0],(list_price_predict[i][1])/Y[i]) for i in range(0,length)]
    
    
    #归一化处理
    max_price=np.amax(list_price_predict, axis=0)[1]
    min_price=np.amin(list_price_predict, axis=0)[1]
    max_predict=np.amax(list_predict, axis=0)[1]
    min_predict=np.amin(list_predict, axis=0)[1]
    
    list_price_predict=[(list_price_predict[i][0],(list_price_predict[i][1]-min_price)/(max_price-min_price)) for i in range(0,length)]    
    list_predict=[(list_price_predict[i][0],(list_predict[i][1]-min_predict)/(max_predict-min_predict)) for i in range(0,length)]
    
    list_sim=[(list_price_predict[i][0],(0.7*list_price_predict[i][1])+(0.3*list_predict[i][1])) for i in range(0,length)]    
    
    return(list_sim)
'''
def predict_model_LinearRegression(X,Y):


    #训练模型
    from sklearn.model_selection import train_test_split
    
    #选20%的样本作为测试数据集
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=4)
    
    #训练模型并测试模型的准确性评分

    #模型优化
    #将数据归一化处理（创建线性回归模型时增加normalize=True参数）
    model = LinearRegression(normalize=True)
    #优化欠拟合的方法：1、挖掘更多的输入特征，2、增加多项式特征
    #此处采用增加多项式特征的方法     
    
    
    
    
    for i in range(1,2):#节省时间就只取一阶
        #一，二，三，四，五阶
        model = polynomial_model(degree=i)
        start = time.clock()
        model.fit(X_train, Y_train)
        
        
        #预测   
    
        Y_predict0=model.predict(X)
        Y_predict1=power(math.e, Y_predict0)
            
        
        train_score = model.score(X_train, Y_train)
        cv_score = model.score(X_test, Y_test)
        #elaspe 模型的训练时间
        #train_score 对训练样本拟合的好坏程度
        #cv_score 对测试样本的得分
        print('elaspe: {0:.6f}; train_score: {1:0.6f}; cv_score: {2:.6f}'.format(time.clock()-start, train_score, cv_score))
    
    X['price_predict1']=Y_predict1
    list_price_predict=list(enumerate(Y_predict0))
#    print(power(math.e, list_price_predict[238][1]))
    length=len(list_price_predict)
    #list_price_predict原价格与预测价格的价格差.
    #***注意***这里采用的是预测-原价格，因为要推荐的，需要是最小的，即推荐距离要最小，所以取反，归一化后，越性价比的越小
    #list_predict原价格与预测价格的价格差与原价格的比
    list_price_predict=[(list_price_predict[i][0],Y[i]-list_price_predict[i][1]) for i in range(0,length)]    
    list_predict=[(list_price_predict[i][0],(list_price_predict[i][1])/Y[i]) for i in range(0,length)]
    
    
    #归一化处理
    max_price=np.amax(list_price_predict, axis=0)[1]
    min_price=np.amin(list_price_predict, axis=0)[1]
    max_predict=np.amax(list_predict, axis=0)[1]
    min_predict=np.amin(list_predict, axis=0)[1]
    
    list_price_predict=[(list_price_predict[i][0],(list_price_predict[i][1]-min_price)/(max_price-min_price)) for i in range(0,length)]    
    list_predict=[(list_price_predict[i][0],(list_predict[i][1]-min_predict)/(max_predict-min_predict)) for i in range(0,length)]
    
    list_sim=[(list_price_predict[i][0],(0.7*list_price_predict[i][1])+(0.3*list_predict[i][1])) for i in range(0,length)]    
    
    return(list_sim)
'''
if __name__=='__main__':
    #导入数据
    print(os.path.dirname(os.path.abspath('__file__')))#返回代码所在目录
    file=os.path.dirname(os.path.abspath('__file__'))
    data_file=os.path.join(file,'second_house_new_clear.csv')#返回数据所在文件位置
    print(data_file)
    df=pd.read_csv(data_file,engine='python',encoding='gb18030')


    features=df[['房本面积','室','厅','卫','房屋朝向num','楼层高低num','楼层层数num','装修情况num','产权年限num','建筑年代num','参考首付num','月供num','小区均价num','所在商圈1num','所在商圈2num']]
    X=features
    '''
    Y=np.log(df['房屋总价'])    
    '''
    
    
    Y=df['房屋总价']
    #将数据代入机器学习模型
    list_sim=predict_model(X,Y)
    
    
    
    '''
    #输出（将预测价格输出表格）
    if(os.path.exists(os.path.join(file,'second_house_new_new.csv'))):#如果输出结果表格已经存在，则删除
        os.remove(os.path.join(file,'second_house_new_new.csv'))
    df_test.to_csv('second_house_new_new.csv',index=False,encoding='utf_8_sig') #去掉index，输出表格csv
    '''