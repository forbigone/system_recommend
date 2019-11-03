# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 22:07:04 2019

@author: Administrator
"""

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.preprocessing import normalize
from scipy.sparse import csr_matrix
import numpy as np
from pandas import Series,DataFrame

items = ['this is the first document, this really is',
             'nothing will stop this from been the second doument, second is not a bad order',
             'I wonder if three documents would be ok as an example, example like this is stupid',
             'ok I think four documents is enough, I I I I think so.']

# will simply using tfidf as the item - profile
# row = item(documents) column = feature(term)
vectorizer = CountVectorizer(min_df=1)
counts = vectorizer.fit_transform(items)
# column  = item(documents) row = feature(term)
transformer = TfidfTransformer()
tfidf = transformer.fit_transform(counts).transpose()



# user's rating for this four documents 
# cloumn = user row = items(documents) 
ratings = csr_matrix([[5, 0, 0, 2], [3, 3, 0, 0], [2, 1, 1, 1], [0, 0, 1, 1]], dtype = u'double') 
# normalize
usersn = ratings - ratings.mean(0)

userprofile =  tfidf.dot(usersn)

userprofile = csr_matrix(userprofile)




#U(X,I)=cos(a)=X·I/normal(X)/normal(I)
# smaller score suggest more similarity between user and item
for i in range(4):
    # iterative over 4 users
    scores = []
    u = userprofile[:,i]
    for j in range(4):
        # iterative over 4 documents
        v = tfidf[:,j]
        #用户档案 i 与物品档案 x 之间的相似程度
        scores.append(sum(u.transpose().dot(v).todense())/np.linalg.norm(u.todense())/np.linalg.norm(v.todense()))
    print ("document recommended for user {0} is document number {1}".format(i+1, scores.index(max(scores))+1))

#document recommended for user 1 is document number 1
#document recommended for user 2 is document number 2
#document recommended for user 3 is document number 4
#document recommended for user 4 is document number 1


#dot()返回的是两个数组的点积  1.如果处理的是一维数组，则得到的是两数组的內积      2.如果是二维数组（矩阵）之间的运算，则得到的是矩阵积
#np.linalg.norm(a)默认参数(矩阵整体元素平方和开根号，不保留矩阵二维特性)
avals = [0,0.5,1,2]
for aval in avals:
    df =DataFrame([[1,0,1,0,1,2],[1,1,0,0,1,6],[0,1,0,1,0,2]],
                index = ['A', 'B', 'C'])
    df[5] = df[5]*aval
    a = df.loc['A']
    b = df.loc['B']
    c = df.loc['C']
    ab = np.dot(a,b)/np.linalg.norm(a)/np.linalg.norm(b)
    ac = np.dot(a,c)/np.linalg.norm(a)/np.linalg.norm(c)
    bc = np.dot(b,c)/np.linalg.norm(c)/np.linalg.norm(b)
    print ('alpha is {0}'.format(aval))
    print ('AB {} AC {} BC {}'.format(np.arccos(np.clip(ab, -1, 1)),np.arccos(np.clip(ac, -1, 1)),np.arccos(np.clip(bc, -1, 1))))

