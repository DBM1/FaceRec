import sys
sys.path.append('../')
from Core import CNN

trainX, trainY = CNN.addimpimg()
CNN.addTrain(trainX, trainY, "./model/testmodel")
