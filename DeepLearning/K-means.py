#    K-means是一个反复迭代的过程，算法分为四个步骤：
#1） 选取数据空间中的K个对象作为初始中心，每个对象代表一个聚类中心
#2） 对于样本中的数据对象，根据它们与这些聚类中心的欧氏距离，按距离最近的准则将它们分到距离它们最近的聚类中心（最相似）所对应的类
#3） 更新聚类中心：将每个类别中所有对象所对应的均值作为该类别的聚类中心，计算目标函数的值
#4） 判断聚类中心和目标函数的值是否发生改变，若不变，则输出结果，若改变，则返回2）

#k-means算法的实现
#-*-coding:utf-8 -*-
from numpy import *
from math import sqrt


import sys
sys.path.append("C:/Users/Administrator/Desktop/k-means的python实现")
 
def loadData(fileName):
    data = []
    fr = open(fileName)
    for line in fr.readlines():
        curline = line.strip().split('\t')
        frline = map(float,curline)
        data.append(frline)
    return data
'''
#test
a = mat(loadData("C:/Users/Administrator/Desktop/k-means/testSet.txt"))
print a
'''
#计算欧氏距离
def distElud(vecA,vecB):
    return sqrt(sum(power((vecA - vecB),2)))

#初始化聚类中心
def randCent(dataSet,k):
    n = shape(dataSet)[1]
    center = mat(zeros((k,n)))
    for j in range(n):
        rangeJ = float(max(dataSet[:,j]) - min(dataSet[:,j]))
        center[:,j] = min(dataSet[:,j]) + rangeJ * random.rand(k,1)
    return center
'''
#test
a = mat(loadData("C:/Users/Administrator/Desktop/k-means/testSet.txt"))
n = 3
b = randCent(a,3)
print b
'''
def kMeans(dataSet,k,dist = distElud,createCent = randCent):
    m = shape(dataSet)[0]
    clusterAssment = mat(zeros((m,2)))
    center = createCent(dataSet,k)
    clusterChanged = True
    while clusterChanged:
        clusterChanged = False
        for i in range(m):
            minDist = inf
            minIndex = -1
            for j in range(k):
                distJI = dist(dataSet[i,:],center[j,:])
                if distJI < minDist:
                    minDist = distJI
                    minIndex = j
            if clusterAssment[i,0] != minIndex:#判断是否收敛
                clusterChanged = True
            clusterAssment[i,:] = minIndex,minDist ** 2
        print center
        for cent in range(k):#更新聚类中心
            dataCent = dataSet[nonzero(clusterAssment[:,0].A == cent)[0]]
            center[cent,:] = mean(dataCent,axis = 0)#axis是普通的将每一列相加，而axis=1表示的是将向量的每一行进行相加
    return center,clusterAssment
'''
#test
dataSet = mat(loadData("C:/Users/Administrator/Desktop/k-means/testSet.txt"))
k = 4
a = kMeans(dataSet,k)
print a
'''