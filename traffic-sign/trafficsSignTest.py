# import the necessary packages
from numpy.core.fromnumeric import reshape
from skimage.util.dtype import img_as_float32
from tensorflow.keras.models import load_model
from skimage import transform
from skimage import exposure
from skimage import io
from imutils import paths
import numpy as np
import pickle
import argparse
import imutils
import random
import cv2
import os

threshold = 0.90
frameWidth = 640
frameHeight= 480
brightness= 70


cap = cv2.VideoCapture(0)
cap.set (3, frameWidth)
cap.set(4, frameHeight)
cap.set(10, brightness)

# pickle_in = open("output/trafficssignnet.model/saved_model.pb", "r")

# model= pickle.load(pickle_in)
model = load_model("output/trafficssignnet.model")#outputFullData/trafficsignnetFullData.model
def grayscale(img):
    img= cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img

def equalize(img):
    img= cv2.equalizeHist(img)
    return img

def preprocessing(img):
    # img= grayscale(img)
    # img= equalize(img)
    img= img/255
    return img

def getClassName(classNo):
    if classNo == 0: return "stop sign"
    if classNo == 1: return "turn right"
    if classNo == 2: return "turn left"
    if classNo == 3: return "straight forward"
# def getClassName(classNo):
#     if classNo == 0: return "speed limit 20 km/u"
#     if classNo == 1: return "speed limit 30 km/u"
#     if classNo == 2: return "speed limit 50km/u"
#     if classNo == 3: return "speed limit 60km/u"
#     if classNo == 4: return "speed limit 70km/u"
#     if classNo == 5: return "speed limit 80km/u"
#     if classNo == 6: return "end speed limit 80km/u"
#     if classNo == 7: return "speed limit 100km/u"
#     if classNo == 8: return "speed limit 120km/u"
#     if classNo == 9: return "no passing cars"
#     if classNo == 10: return  "no passing truck"
#     if classNo == 11: return "right of way"
#     if classNo == 12: return "Priority"
#     if classNo == 13: return "yeild right of way"
#     if classNo == 14: return "stop"
#     if classNo == 15: return "prohibited for all vehicles"
#     if classNo == 16: return "prohibited for tractors and trucks"
#     if classNo == 17: return "entry prohibited"
#     if classNo == 18: return "danger"
#     if classNo == 19: return "single curve left"
#     if classNo == 20: return "single curve right"
#     if classNo == 21: return "double curve"
#     if classNo == 22: return "road bumps"
#     if classNo == 23: return "slippery road"
#     if classNo == 24: return "road narrows"
#     if classNo == 25: return "reparing road"
#     if classNo == 26: return "signal lights ahead"
#     if classNo == 27: return "pedestrian crosswalk ahead"
#     if classNo == 28: return "children"
#     if classNo == 29: return "bicycle road"
#     if classNo == 30: return "snow road"
#     if classNo == 31: return "wild animal crossing"
#     if classNo == 32: return "end of restriction"
#     if classNo == 33: return "right direction"
#     if classNo == 34: return "left direction"
#     if classNo == 35: return "straight direction"
#     if classNo == 36: return "straight or right"
#     if classNo == 37: return "straight or left"
#     if classNo == 38: return "right under"
#     if classNo == 39: return "left under"
#     if classNo == 40: return "traffic circle"
#     if classNo == 41: return "end no passing cars"
#     if classNo == 42: return "end no passing trucks"
    
    

while True:

    success , imgOrginal = cap.read()
    # img= cv2.cvtColor(imgOrginal, cv2.COLOR_BGR2RGB)
    # print(imgOrginal.shape)
    img =np.asfarray(imgOrginal , dtype=np.float32)
    img= cv2.resize(img ,(32,32))
    # img = preprocessing(img)
    
    
    img= img.reshape(1,32,32,-1)
    
    cv2.putText(imgOrginal, "Class" , (20, 35), cv2.FONT_HERSHEY_PLAIN , 0.75, (0,0,255), 2, cv2.LINE_AA)
    cv2.putText(imgOrginal, "Prob" , (20, 75), cv2.FONT_HERSHEY_PLAIN , 0.75, (0,0,255), 2, cv2.LINE_AA)
    
    predictions = model.predict(img)
    classIndex= model.predict_classes(img)

    probValue= np.amax(predictions)
    print(probValue,predictions)
    if(probValue> threshold):
        cv2.putText(imgOrginal, str(classIndex)+" "+ str(getClassName(classIndex)),(120,35), cv2.FONT_HERSHEY_PLAIN, 1,(0,0,255),2, cv2.LINE_AA)
        cv2.putText(imgOrginal, str(round(probValue*100,2))+"%",(180,75), cv2.FONT_HERSHEY_PLAIN, 1,(0,255,255),2, cv2.LINE_AA)

    cv2.imshow("Result", imgOrginal)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()