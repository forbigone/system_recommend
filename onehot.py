
from sklearn.preprocessing import OneHotEncoder
import math
import numpy as np 
import os
import pandas as pd
from sklearn import preprocessing 
import re
from pandas import Series,DataFrame
#独热化

print(os.path.dirname(os.path.abspath('__file__')))#返回代码所在目录
file=os.path.dirname(os.path.abspath('__file__'))
data_file=os.path.join(file,'second_house_new_new.csv')#返回数据所在文件位置
print(data_file)
df=pd.read_csv(data_file,engine='python',encoding='utf_8_sig')
features=df[['房屋总价','房本面积','室','厅','卫','房屋朝向num','楼层高低num','楼层层数num','装修情况num','产权年限num','建筑年代num','参考首付num','月供num','小区均价num','所在商圈1num','所在商圈2num']]
X=features
enc=preprocessing.OneHotEncoder().fit(X[['所在商圈1num','所在商圈2num','房屋朝向num','装修情况num']])
X_encoded=enc.transform(X[['所在商圈1num','所在商圈2num','房屋朝向num','装修情况num']]).toarray()
print(X_encoded)





