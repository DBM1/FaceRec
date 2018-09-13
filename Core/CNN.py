import numpy as np
import tensorflow as tf
import os
import cv2
import shutil
import random

x_data = tf.placeholder(tf.float32, [None, 64, 64, 3])
y_data = tf.placeholder(tf.float32, [None, None])

keep_porb1 = tf.placeholder(tf.float32)
keep_porb2 = tf.placeholder(tf.float32)


def makedir(*args):
    for path in args:
        if not os.exits(path):
            os.makedirs(path)


def weightvar(shape):
    temp = tf.random_normal(shape, stddev=0.01)
    weight = tf.Variable(temp)
    return weight


def biasvar(shape):
    temp = tf.random_normal(shape)
    bias = tf.Variable(temp)
    return bias


def conv(x, w):
    return tf.nn.conv2d(x, w, strides=[1, 1, 1, 1], padding="SAME")


def maxpool(x):
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding="SAME")


def dropout(x, keep):
    return tf.nn.dropout(x, keep)


def cnnlayer(classNum):
    w1 = weightvar([3, 3, 3, 64])
    b1 = biasvar([64])
    conv1 = tf.nn.relu(conv(x_data, w1) + b1)
    pool1 = maxpool(conv1)
    drop1 = dropout(pool1, keep_porb1)

    w2 = weightvar([3, 3, 64, 64])
    b2 = biasvar([64])
    conv2 = tf.nn.relu(conv(drop1, w2) + b2)
    pool2 = maxpool(conv2)
    drop2 = dropout(pool2, keep_porb1)

    w3 = weightvar([3, 3, 64, 128])
    b3 = biasvar([128])
    conv3 = tf.nn.relu(conv(drop2, w3) + b3)
    pool3 = maxpool(conv3)
    drop3 = dropout(pool3, keep_porb1)

    w4 = weightvar([8 * 8 * 128, 256])
    b4 = biasvar([256])
    drop2_flat = tf.reshape(drop3, [-1, 8 * 8 * 128])
    dense = tf.nn.relu(tf.matmul(drop2_flat, w4) + b4)
    dropf = dropout(dense, keep_porb2)

    w5 = weightvar([256, classNum])
    b5 = biasvar([classNum])
    out = tf.matmul(dropf, w5) + b5

    return out


def addGaussianNoise(image, percetage):
    G_Noiseimg = image
    G_NoiseNum = int(percetage * image.shape[0] * image.shape[1])
    for i in range(G_NoiseNum):
        temp_x = np.random.randint(0, 63)
        temp_y = np.random.randint(0, 63)
        G_Noiseimg[temp_x][temp_y] = 255
    return G_Noiseimg


def train(trainX, trainY, tfSavePath):
    out = cnnlayer(trainY.shape[1])
    crossEntropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=out, labels=y_data))
    global_step = tf.Variable(0, trainable=False)
    rate = tf.train.exponential_decay(0.001, global_step, 1000, 0.93, True)
    trainStep = tf.train.AdamOptimizer(rate).minimize(crossEntropy, global_step)
    accuracy = tf.reduce_mean(tf.cast(tf.equal(tf.argmax(out, 1), tf.argmax(y_data, 1)), tf.float32))

    length = trainY.shape[0]
    saver = tf.train.Saver()

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        trainXholder = trainX
        trainYholder = trainY
        testX = []
        testY = []
        trainX = []
        trainY = []
        for cutNum in range(length // 400):
            trainX.append(trainXholder[400 * cutNum:400 * cutNum + 300])
            testX.append(trainXholder[400 * cutNum + 300:400 * (cutNum + 1)])
            trainY.append(trainYholder[400 * cutNum:400 * cutNum + 300])
            testY.append(trainYholder[400 * cutNum + 300:400 * (cutNum + 1)])

        trainX = np.concatenate(trainX, 0)
        testX = np.concatenate(testX, 0)
        testX = testX[:800]
        trainY = np.concatenate(trainY, 0)
        testY = np.concatenate(testY, 0)
        testY = testY[:800]
        for i in range(trainX.shape[0]):
            type = random.random()
            if type < 0.30:
                cv2.flip(trainX[i], 0)
                trainX[i] = addGaussianNoise(trainX[i], 0.15)
            elif type > 0.70:
                cv2.flip(trainX[i], 1)
                trainX[i] = addGaussianNoise(trainX[i], 0.1)

        batchSize = 10
        numBatch = trainY.shape[0] // batchSize
        n = 0
        num = 0
        while n < 4:
            r = np.random.permutation(trainX.shape[0])
            trainX = trainX[r, :]
            trainY = trainY[r, :]
            for i in range(numBatch):
                batchX = trainX[i * batchSize:(i + 1) * batchSize]
                batchY = trainY[i * batchSize: (i + 1) * batchSize]
                sess.run([trainStep, crossEntropy],
                         feed_dict={x_data: batchX, y_data: batchY, keep_porb1: 0.5, keep_porb2: 0.5})
            acc = accuracy.eval({x_data: testX, y_data: testY, keep_porb1: 1.0, keep_porb2: 1.0})
            print("Traversal:", n, " Accuary:", acc)
            if (acc > 0.985):
                n += 1
            else:
                n = 0
            num += 1
            if num > 200 and acc >= 0.99:
                break
            print(num)
        saver.save(sess, tfSavePath)


def addTrain(trainX, trainY, tfSavePath):
    out = cnnlayer(trainY.shape[1])
    crossEntropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=out, labels=y_data))
    global_step = tf.Variable(0, trainable=False)
    rate = tf.train.exponential_decay(0.001, global_step, 1000, 0.95, True)
    trainStep = tf.train.AdamOptimizer(rate).minimize(crossEntropy, global_step)
    accuracy = tf.reduce_mean(tf.cast(tf.equal(tf.argmax(out, 1), tf.argmax(y_data, 1)), tf.float32))

    length = trainY.shape[0]
    saver = tf.train.Saver()

    with tf.Session() as sess:
        saver.restore(sess, tfSavePath)
        trainXholder = trainX
        trainYholder = trainY
        testX = []
        testY = []
        trainX = []
        trainY = []
        for cutNum in range(length // 400):
            trainX.append(trainXholder[400 * cutNum:400 * cutNum + 300])
            testX.append(trainXholder[400 * cutNum + 300:400 * (cutNum + 1)])
            trainY.append(trainYholder[400 * cutNum:400 * cutNum + 300])
            testY.append(trainYholder[400 * cutNum + 300:400 * (cutNum + 1)])

        trainX = np.concatenate(trainX, 0)
        testX = np.concatenate(testX, 0)
        testX = testX[:800]
        trainY = np.concatenate(trainY, 0)
        testY = np.concatenate(testY, 0)
        testY = testY[:800]
        for i in range(trainX.shape[0]):
            type = random.random()
            if type < 0.30:
                cv2.flip(trainX[i], 0)
                trainX[i] = addGaussianNoise(trainX[i], 0.15)
            elif type > 0.70:
                cv2.flip(trainX[i], 1)
                trainX[i] = addGaussianNoise(trainX[i], 0.1)

        batchSize = 10
        numBatch = trainY.shape[0] // batchSize
        n = 0
        num = 0
        while n < 3:
            r = np.random.permutation(trainX.shape[0])
            trainX = trainX[r, :]
            trainY = trainY[r, :]
            for i in range(numBatch):
                batchX = trainX[i * batchSize:(i + 1) * batchSize]
                batchY = trainY[i * batchSize: (i + 1) * batchSize]
                sess.run([trainStep, crossEntropy],
                         feed_dict={x_data: batchX, y_data: batchY, keep_porb1: 0.5, keep_porb2: 0.5})
            acc = accuracy.eval({x_data: testX, y_data: testY, keep_porb1: 1.0, keep_porb2: 1.0})
            print("Traversal:", n, " Accuary:", acc)
            if (acc > 0.985):
                n += 1
            else:
                n = 0
            num += 1
            if num > 200 and acc > 0.985:
                break
            print(num)
        saver.save(sess, tfSavePath)
    commitAdd()


def impimg():
    path = "../TrainImage"
    if not os.path.exists(path):
        os.makedirs(path)
    filename = os.listdir(path)
    length = len(filename)
    imgList = []
    labelList = np.zeros([400 * length, 100], int)
    index = 0
    f = open("./id.txt", "w")
    for name in filename:
        pngPath = path + '/' + name
        pngList = os.listdir(pngPath)
        if len(pngList) == 400:
            f.write("*" + name)
            for i in range(400):
                imgList.append(cv2.imread("../TrainImage/%s/%d.png" % (name, i)))
                labelList[400 * index + i][index] = 1
            index += 1
        else:
            print("Incorrect PNG number:" + pngPath)
            shutil.rmtree(pngPath)
    f.close()
    imgList = np.array(imgList)
    return imgList, labelList

def commitAdd():
    addPath = "../NewImage"
    if not os.path.exists"../TrainImage"):
        os.makedirs("../TrainImage")
    filenameNew = os.listdir(addPath)
    f = open("./id.txt", 'a+')
    for name in filenameNew:
        pngPath = addPath + '/' + name
        pngList = os.listdir(pngPath)
        if len(pngList) == 400:
            f.write("*" + name)
            shutil.move(pngPath, "../TrainImage")

def addimpimg():
    path = "../TrainImage"
    addPath = "../NewImage"
    if not os.path.exists(path):
        os.makedirs(path)
    filenameOld = os.listdir(path)
    filenameNew = os.listdir(addPath)
    lengthOld = len(filenameOld)
    lengthNew = len(filenameNew)
    imgListOld = []
    imgListNew = []
    index = 0
    f = open("./id.txt", 'a+')
    for name in filenameOld:
        pngPath = path + '/' + name
        pngList = os.listdir(pngPath)
        if len(pngList) == 400:
            pass
        else:
            print("Incorrect PNG number:" + pngPath)
            shutil.rmtree(pngPath)
            lengthOld -= 1
    for name in filenameNew:
        pngPath = addPath + '/' + name
        pngList = os.listdir(pngPath)
        if len(pngList) == 400:
            pass
        else:
            print("Incorrect PNG number:" + pngPath)
            shutil.rmtree(pngPath)
            lengthNew -= 1

    labelListOld = np.zeros([400 * lengthOld, 100], int)
    labelListNew = np.zeros([400 * lengthNew, 100], int)

    for name in filenameOld:
        for i in range(400):
            imgListOld.append(cv2.imread("../TrainImage/%s/%d.png" % (name, i)))
            labelListOld[400 * index + i][index] = 1
        index += 1

    for name in filenameNew:
        for i in range(400):
            imgListNew.append(cv2.imread("../NewImage/%s/%d.png" % (name, i)))
            labelListNew[400 * (index - lengthOld) + i][index] = 1
        index += 1

    labelListOld = labelListOld[0:400 * lengthOld]
    labelListNew = labelListNew[0:400 * lengthNew]
    r = np.random.permutation(len(imgListOld))
    imgListNew = np.array(imgListNew)
    imgListOld = np.array(imgListOld)[r]
    labelListOld = labelListOld[r]
    if lengthNew > lengthOld:
        imgList = np.concatenate((imgListOld, imgListNew))
        labelList = np.concatenate((labelListOld, labelListNew))
    else:
        imgList = np.concatenate((imgListOld[0:400 * lengthNew], imgListNew))
        labelList = np.concatenate((labelListOld[0:400 * lengthNew], labelListNew))
    f.close()
    return imgList, labelList


def rec(tfsavepath):
    f = open("./id.txt", "r")
    filename = f.read()
    filename = filename.split('*')
    filename.remove("")
    classnum = 100
    cap = cv2.VideoCapture(0)
    classifier = cv2.CascadeClassifier('../Collection/haarcascade_frontalface_alt2.xml')
    output = cnnlayer(classnum)0
    saver = tf.train.Saver()
    jugement = np.zeros([classnum])
    i = 0
    with tf.Session() as sess:
        saver.restore(sess, tfsavepath)
        while 1:
            ret, img = cap.read()
            faces = classifier.detectMultiScale(img, 1.1, 3, minSize=(150, 150))
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                face = img[y:y + h, x:x + w]
                face = cv2.resize(face, (64, 64))
                face = np.expand_dims(face, 0)
                result = sess.run(output, feed_dict={x_data: face, keep_porb1: 1.0, keep_porb2: 1.0})
                if i < 100:
                    jugement[[np.argmax(result)]] += 1
                    i += 1
                else:
                    rate = jugement[np.argmax(jugement)] / 100.0
                    print(jugement)
                    if rate > 0.85:
                        print(filename[np.argmax(jugement)])
                    else:
                        print("Not include!")
                    jugement = np.zeros([classnum])
                    i = 0
            cv2.imshow("test", img)
            if cv2.waitKey(1) & 0xff == ord("q"):
                break
        cap.release()
        cv2.destroyAllWindows()


def test():
    imgpath = "../NewImage/test1"
    filename = os.listdir(imgpath)
    testList = []
    for name in filename:
        img = cv2.imread(imgpath + '/' + name)
        testList.append(img)
    testList = np.array(testList)
    f = open("./id.txt", "r")
    filename = f.read()
    filename = filename.split('*')
    filename.remove("")
    output = cnnlayer(100)
    saver = tf.train.Saver()
    with tf.Session() as sess:
        saver.restore(sess, "./model/testmodel")
        result = sess.run(output, feed_dict={x_data: testList, keep_porb1: 1.0, keep_porb2: 1.0})
        re = np.argmax(result, 1)
        result = 0
        for i in re:
            result += i
        print(result)

