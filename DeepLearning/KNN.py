#coding:utf-8

from numpy import * 
import operator

#give training data & their classes
def createDataSet():
	group = array([[1.0, 2.0],[1.2, 0.1],[0.1, 1.4],[0.3, 3.5]])
	labels = ['A','A','B','B']
	return group,labels

def classify(input,dataSet,label,k):
	dataSize = dataSet.shape[0]
	diff = tile(input, (dataSize,1)) - dataSet
	sqdiff = diff ** 2
	squareDist = sum(sqdiff,axis = 1)
	dist = squareDist ** 0.5

	sortedDistIndex = argsort(dist)

	classCount = {}
	for i in range(k):
		voteLabel = label[sortedDistIndex[i]]
		classCount[voteLabel] = classCount.get(voteLabel,0) + 1

	maxCount = 0
	for key,value in classCount.items():
		if value > maxCount:
			maxCount = value
			classes = key

	return classes

#import sys
#sys.path.append("...file path...")
#import KNN
#from numpy import *
#dataSet,labels = KNN.createDataSet()
#input = array([1.1,0.3])
#K = 3
#output = KNN.classify(input,dataSet,labels,K)
#print("test data:",input,"classify result: ",output)