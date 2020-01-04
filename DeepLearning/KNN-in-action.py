#KNN-in-action
from numpy import *
import operator
from collections import Counter
import matplotlib
import matplotlib.pyplot as plt

#input data
def file2matrix(filename):
	#read all contents from 'filename'
	fr = open(filename)
	contain = fr.readlines()
	count = len(contain)
	returnMat = zeros((count, 3))
	classLabelVector = []
	index = 0
	for line in contain:
		line = line.strip()
		listFromLine = line.split('\t')
		returnMat[index,:] = listFromLine[0:3]
		classLabelVector.append(listFromLine[-1])
		index += 1

	#transform str into data to calculate
	dictClassLabel = Counter(classLabelVector)
	classLabel = []
	kind = list(dictClassLabel)
	for item in classLabelVector:
		if item == kind[0]:
			item = 1
		elif item == kind[1]:
			item = 2
		else:
			item = 3
		classLabel.append(item)
	return returnMat,classLabel

datingDataMat,datingLabels = file2matrix('.txt')
fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(datingDataMat[:,0],datingDataMat[:,1],15.0*array(dictClassLabel),15.0*array(datingLabels))
plt.show()

def autoNorm(dataSet):
	minVals = dataSet.min(0)
	maxVals = dataSet.max(0)
	ranges = maxVals - minVals
	normDataSet = zeros(shape(dataSet))
	m = dataSet.shape[0]
	for i in range(1,m):
		normDataSet[i,:] = (dataSet[i,:]-minVals) / ranges
	return normDataSet,ranges,minVals

#KNN
def classify(input,dataSet,label,k):
	dataSize = dataSet.shape[0]
	diff = tile(input,(dataSize,1)) - dataSet
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

#test.py
import sys
sys.path.append("...filepath...")
import KNN
from numpy import *
dataSet,labels = KNN.createDataSet()
input = array([1.1,0.3])
K = 3
output = KNN.classify(input,dataSet,labels,K)
print("test data:",input,"classify results:",output)