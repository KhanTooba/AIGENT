import numpy
import numpy as np
from numpy import cov
from numpy import trace
from numpy import iscomplexobj
from numpy import asarray
from scipy.linalg import sqrtm
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
"""
To supress the tensorflow warnings. 
0 = all messages are logged (default behavior)
1 = INFO messages are not printed
2 = INFO and WARNING messages are not printed
3 = INFO, WARNING, and ERROR messages are not printed
"""
import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
"""
Setting verbosity of tensorflow to minimum.
"""
from PIL import Image
from numpy import asarray
  

# def loadModel():
#     model = tf.keras.models.load_model(os.path.abspath(os.path.join(os.getcwd(), os.pardir)) +'/Models/mnist.h5')
#     return model

def getImages(folderCount):
    originalImages = []
    adversarialImages = []
    count = 0
    im1 = []
    im2 = []
    w, h = 128, 128
    # folderCount = 1
    
    for path in os.listdir("OriginalImages"+str(folderCount)):
        originalImages.append('OriginalImages'+str(folderCount)+'/'+str(path))
        adversarialImages.append('AdversarialImages'+str(folderCount)+'/'+str(path))
        count = count+1
    
    for i in range(count):
        if "ipynb" in originalImages[i]:
          continue
        img = Image.open(originalImages[i])
        # img = img.resize((28, 28))
        
        numpydata = asarray(img)
        im1.append(numpydata)

        img = Image.open(adversarialImages[i])
        # img = img.resize((28, 28))
        # img = img.reshape(1, 28, 28, 1)
        numpydata = asarray(img)
        im2.append(numpydata)

    im1_t = np.array(im1)
    im2_t = np.array(im2)

    im1 = []
    im2 = []
    for img in im1_t:
      img = img.reshape(w, h, 3)
      im1.append(img)
    im1 = np.array(im1)

    for img in im2_t:
      img = img.reshape(w, h, 3)
      im2.append(img)
    im2 = np.array(im2)
    im1 = im1.reshape((im1.shape[0], w*h*3)).astype('float32')
    im2 = im2.reshape((im2.shape[0], w*h*3)).astype('float32')
    # print(im1[0][-10:])
    im1 = im1/255
    im2 = im2/255

    return im1, im2

def calculate_fid(model, images1, images2):
  act1 = model.predict(images1)
  act2 = model.predict(images2)
  
  mu1, sigma1 = act1.mean(axis=0), cov(act1, rowvar=False)
  mu2, sigma2 = act2.mean(axis=0), cov(act2, rowvar=False)
  
  ssdiff = numpy.sum((mu1 - mu2)**2.0)
  
  # print(sigma1.dot(sigma2))
  covmean = sqrtm(sigma1.dot(sigma2))
  
  if iscomplexobj(covmean):
    covmean = covmean.real
  
  fid = ssdiff + trace(sigma1 + sigma2 - 2.0 * covmean)
  return fid
