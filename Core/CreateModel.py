import sys
sys.path.append('../')
from Core import CNN

trainX, trainY = CNN.impimg()
CNN.train(trainX, trainY, "./model/testmodel")