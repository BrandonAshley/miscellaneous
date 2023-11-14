# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 16:03:24 2022

@author: brand
"""

#https://www.youtube.com/watch?v=9iEPzbG-xLE&list=PLi8F7KCxk5LE_DE2jxr7vaoSDEu7yzDV6&index=2&t=83s
#https://www.youtube.com/watch?v=9ZRqc4EaPRU

import cv2
import time
import numpy as np
import HandTracking_module as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

##################################
wCam,hCam=640,480
############################


cap=cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
pTime=0

detector=htm.handDetector(detectionCon=0.75)



devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMasterVolumeLevel()
volRange=volume.GetVolumeRange()
#volume.SetMasterVolumeLevel(-37, None)
minVol=volRange[0]
maxVol=volRange[1]
volBar=400
vol=0
volPer=0

while True:
    success, img =cap.read()
    
    
    
    #Find Handd
    img=cv2.flip(img, 1)
    img=detector.findHands(img)
    
    lmList=detector.findPosition(img,draw=False)
    if len(lmList)!=0:

        #Filter based on size
        #Find Distance between index and thumb
        #Convert Volume
        #Reduce resolution to make it smoother
        #Check fingers up
        #if pinky is down set volume
        #Drawings
        #framerate
        
        
        
        
        #print(lmList[4],lmList[8])
        
        x1,y1=lmList[4][1],lmList[4][2]
        x2,y2=lmList[8][1],lmList[8][2]
        cx,cy=(x1+x2)//2,(y1+y2)//2
        
        
        cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
        cv2.circle(img,(x2,y2),15,(255,0,255),cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)
        cv2.circle(img,(cx,cy),15,(255,0,255),cv2.FILLED)
        
        length=math.hypot(x2-x1,y2-y1)

        vol=np.interp(length,[15,115],[minVol,maxVol])
        volBar=np.interp(length,[15,115],[400,150])
        volPer=np.interp(length,[15,115],[0,100])
        volume.SetMasterVolumeLevel(vol, None)
        
        
        if length<15:
            cv2.circle(img,(cx,cy),15,(0,255,0),cv2.FILLED)
        
    cv2.rectangle(img, (50,150), (85,400), (0,255,0),3)
    cv2.rectangle(img, (50,int(volBar)), (85,400), (0,255,0),cv2.FILLED)
    cv2.putText(img, str(int(volPer)), (40,450),cv2.FONT_HERSHEY_PLAIN,3,(0,255,0),3)    
        
    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    
    
    cv2.putText(img, str(int(fps)), (10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)    
    
    cv2.imshow("Img",img)
    if cv2.waitKey(1)& 0xFF == ord('q'):
        break




cap.release()
cv2.destroyAllWindows()
