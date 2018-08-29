import numpy as np
import cv2
import os


def relight(img, alpha=1, b=0):
    img = img.astype(float)
    img = img * alpha + b
    img[img < 0] = 0
    img[img > 255] = 255
    img = img.astype(np.uint8)
    return img


def capture(id):
    cap = cv2.VideoCapture(0)
    classifier = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')
    pList = []
    path = "../TrainImage/" + id
    if not os.path.exists(path):
        os.makedirs(path)
    for i in range(400):
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = classifier.detectMultiScale(gray, 1.3, 5, minSize=(80, 80))
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            face = gray[y:y + h, x:x + w]
            face = cv2.resize(face, (64, 64))
            pList.append(face)
            cv2.imwrite(path + "/%d.png" % i, relight(face, np.random.uniform(0.5, 1.5)))
        cv2.imshow('image', relight(img, 1.5))
        if cv2.waitKey(1) & 0xff == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()
