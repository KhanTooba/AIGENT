import os
from re import I
from PIL import Image
from numpy import asarray
import numpy as np
import cv2
import numpy as np
import random
import csv

def convertChannel(path):
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img2 = np.zeros_like(img)
    img2[:,:,0] = gray
    img2[:,:,1] = gray
    img2[:,:,2] = gray
    cv2.imwrite(path, img2)

def convertImage(image, w, h):
    img = Image.open(image)
    img = img.resize((w, h))
    if len(np.shape(img))==2:
        convertChannel(image)
        img = Image.open(image)
        img = img.resize((w, h))
    numpydata = asarray(img).reshape(w*h*3)/255
    return numpydata

def convertToMtarix(array, m, n, channels):
    print(np.shape(array))
    for i in range(128*128*3):
        array[i] = 255*array[i]
    matrix = np.array(array)
    return matrix.reshape((m, n, channels))

def showing(pixelMatrix, m, n, channels):
    print(np.shape(pixelMatrix))
    pixelMatrix = convertToMtarix(pixelMatrix, 128, 128, 3)
    data = np.array(pixelMatrix)
    im = Image.fromarray(data.astype(np.uint8), mode='RGB')
    # im = im.resize((m, n, channels))
    # im.show()
    return im

def getTrainData(w, h):
    labels = {}
    i = 0
    for path in os.listdir("Data/train"):
        labels[path] = i
        i = i+1
    
    X_train = []
    Y_train = []

    print("Fetching data...")
    for folder in os.listdir("Data/train"):
        i = 0
        print("Loading for:", folder)
        for path in os.listdir("Data/train/"+folder):
            img = convertImage("Data/train/"+folder+"/"+path, w, h)
            X_train.append(img)
            Y_train.append([labels[folder]])
        #     showing(X_train, 128, 128, 3)
            i += 1
            if i>=40:
                break
        #     break
        # break
    print(np.shape(X_train))
    # for x in range(10):
    #     showing(X_train[x], 128, 128, 3)
    temp = list(zip(X_train, Y_train))
    random.shuffle(temp)
    res1, res2 = zip(*temp)
    res1, res2 = list(res1), list(res2)
    # print("Storing data...")

    # with open('Data/input.csv', 'w', encoding='UTF8', newline='') as f:
    #     writer = csv.writer(f)
    #     writer.writerows(X_train)
    
    # with open('Data/output.csv', 'w', encoding='UTF8', newline='') as f:
    #     writer = csv.writer(f)
    #     writer.writerows(Y_train)

    return np.array(res1), np.array(res2)

def getValData(w, h):
    labels = {}
    i = 0
    for path in os.listdir("Data/val"):
        labels[path] = i
        i = i+1

    X_test = []
    Y_test = []
    for folder in os.listdir("Data/val"):
        for path in os.listdir("Data/val/"+folder):
            img = convertImage("Data/val/"+folder+"/"+path, w, h)
            X_test.append(img)
            Y_test.append(labels[folder])

    temp = list(zip(X_test, Y_test))
    random.shuffle(temp)
    res1, res2 = zip(*temp)
    res1, res2 = list(res1), list(res2)
    return np.array(res1), np.array(res2)
