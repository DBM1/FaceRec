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
    i = 0
    path = "../TestImage/" + id
    if id == "":
        print("id is empty!")
        return
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        print("path is existed!")
        return
    while i < 400:
        ret, img = cap.read()
        faces = classifier.detectMultiScale(img, 1.1, 3, minSize=(150, 150))
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            face = img[y:y + h, x:x + w]
            face = cv2.resize(face, (64, 64))
            pList.append(face)
            cv2.imwrite(path + "/%d.png" % i, relight(face, np.random.uniform(0.5, 1.5)))
            i += 1
        cv2.imshow('image', img)
        if cv2.waitKey(1) & 0xff == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()

