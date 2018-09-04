import numpy as np
import tensorflow as tf
import os
import cv2

x_data = tf.placeholder(tf.float32, [None, 64, 64, 3])
y_data = tf.placeholder(tf.float32, [None, None])

keep_porb1 = tf.placeholder(tf.float32)
keep_porb2 = tf.placeholder(tf.float32)


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

    w3 = weightvar([3, 3, 64, 64])
    b3 = biasvar([64])
    conv3 = tf.nn.relu(conv(drop2, w3) + b3)
    pool3 = maxpool(conv3)
    drop3 = dropout(pool3, keep_porb1)

    w4 = weightvar([8 * 8 * 64, 512])
    b4 = biasvar([512])
    drop2_flat = tf.reshape(drop3, [-1, 8 * 8 * 64])
    dense = tf.nn.relu(tf.matmul(drop2_flat, w4) + b4)
    dropf = dropout(dense, keep_porb2)

    w5 = weightvar([512, classNum])
    b5 = biasvar([classNum])
    out = tf.matmul(dropf, w5) + b5

    return out


def train(trainX, trainY, tfSavePath):
    out = cnnlayer(trainY.shape[1])
    crossEntropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=out, labels=y_data))
    trainStep = tf.train.AdamOptimizer(0.001).minimize(crossEntropy)
    accuracy = tf.reduce_mean(tf.cast(tf.equal(tf.argmax(out, 1), tf.argmax(y_data, 1)), tf.float32))

    saver = tf.train.Saver()

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        trainXholder = trainX
        trainYholder = trainY
        trainX = np.vstack((trainXholder[0:300], trainXholder[400:700], trainXholder[800:1100], trainXholder[1200:1500],
                            trainXholder[1600:1900]))
        testX = np.vstack(
            (trainXholder[300:400], trainXholder[700:800], trainXholder[1100:1200], trainXholder[1500:1600],
             trainXholder[1900:2000]))
        trainY = np.vstack((trainYholder[0:300], trainYholder[400:700], trainYholder[800:1100], trainYholder[1200:1500],
                            trainYholder[1600:1900]))
        testY = np.vstack(
            (trainYholder[300:400], trainYholder[700:800], trainYholder[1100:1200], trainYholder[1500:1600],
             trainYholder[1900:2000]))
        batchSize = 10
        numBatch = trainY.shape[0] // batchSize
        for n in range(20):
            r = np.random.permutation(len(trainX))
            trainX = trainX[r, :]
            trainY = trainY[r, :]
            for i in range(numBatch):
                batchX = trainX[i * batchSize:(i + 1) * batchSize]
                batchY = trainY[i * batchSize: (i + 1) * batchSize]
                sess.run([trainStep, crossEntropy],
                         feed_dict={x_data: batchX, y_data: batchY, keep_porb1: 0.75, keep_porb2: 0.75})
            acc = accuracy.eval({x_data: testX, y_data: testY, keep_porb1: 1.0, keep_porb2: 1.0})
            print("Traversal:", n, " Accuary:", acc)
        # for j in range(3):
        #     trainX = np.vstack((trainX[0:800], trainXholder[400 * (j + 2):400 * (j + 2)+300]))
        #     print(trainX.shape)
        #     trainY = np.vstack((trainY[0:800], trainYholder[400 * (j + 2):400 * (j + 2)+300]))
        #     print(trainY.shape)
        #     for n in range(10):
        #         r = np.random.permutation(len(trainX))
        #         trainX = trainX[r, :]
        #         trainY = trainY[r, :]
        #         for i in range(numBatch):
        #             batchX = trainX[i * batchSize:(i + 1) * batchSize]
        #             batchY = trainY[i * batchSize: (i + 1) * batchSize]
        #             sess.run([trainStep, crossEntropy],
        #                      feed_dict={x_data: batchX, y_data: batchY, keep_porb1: 0.75, keep_porb2: 0.75})
        #         acc = accuracy.eval(
        #             {x_data: trainX[0:800, :], y_data: trainY[0:800, :], keep_porb1: 1.0, keep_porb2: 1.0})
        #         print("Traversal add:", n, " Accuary:", acc)
        # r = np.random.permutation(len(trainXholder))
        # trainXholder = trainXholder[r, :]
        # trainYholder = trainYholder[r, :]
        # acc = accuracy.eval(
        #     {x_data: trainXholder[0:800], y_data: trainYholder[0:800], keep_porb1: 1.0, keep_porb2: 1.0})
        # print(acc)
        saver.save(sess, tfSavePath)


def makedir(*args):
    for path in args:
        if not os.exits(path):
            os.makedirs(path)


def impimg():
    path = "../TrainImage"
    filename = os.listdir(path)
    print(filename)
    length = len(filename)
    imgList = []
    labelList = np.zeros([400 * length, length], int)
    index = 0
    for name in filename:
        for i in range(400):
            imgList.append(cv2.imread("../TrainImage/%s/%d.png" % (name, i)))
            labelList[400 * index + i][index] = 1
        index += 1
    imgList = np.array(imgList)
    return imgList, labelList


def rec(tfsavepath, classnum):
    cap = cv2.VideoCapture(0)
    classifier = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')
    output = cnnlayer(classnum)
    path = "../TrainImage"
    filename = os.listdir(path)
    print(filename)
    saver = tf.train.Saver()
    jugement = np.zeros([classnum])
    i = 0
    with tf.Session() as sess:
        saver.restore(sess, tfsavepath)
        while 1:
            ret, img = cap.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = classifier.detectMultiScale(gray, 1.1, 3, minSize=(120, 120))
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


# trainX, trainY = impimg()
# train(trainX, trainY, "./model/testmodel1")
rec("./model/testmodel1", 5)
