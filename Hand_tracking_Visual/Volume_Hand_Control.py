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

detector=htm.handDetector(detectionCon=0.75,maxHands=1)



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
area=0
colorVol=(255,0,0)

while True:
    success, img =cap.read()
    
    #Find Handd
    img=cv2.flip(img, 1)
    img=detector.findHands(img)
    
    lmList,bbox=detector.findPosition(img,draw=True)
    if len(lmList)!=0:
        
        #Filter based on size
        area=(bbox[2]-bbox[0])*(bbox[3]-bbox[1])//100
        
        if 250<area<1000:
            #Find Distance between index and thumb
            length,img,lineInfo=detector.findDistance(4, 8, img)
            
            #Convert Volume
            volBar=np.interp(length,[15,200],[400,150])
            volPer=np.interp(length,[15,200],[0,100])
            #volume.SetMasterVolumeLevelScalar(volPer/100,None)
            
            #Reduce resolution to make it smoother
            smoothness=5
            volPer=smoothness*round(volPer/smoothness)
            
            #Check fingers up
            fingers=detector.fingersUp()
            
            #if pinky is down set volume
            if not fingers[4]:
                volume.SetMasterVolumeLevelScalar(volPer/100,None)
                cv2.circle(img,(lineInfo[4],lineInfo[5]),15,(0,255,0),cv2.FILLED)
                colorVol=(0,255,0)
                
            else:
                colorVol=(255,0,0)
            
            #Drawings
            cv2.rectangle(img, (50,150), (85,400), (0,255,0),3) 
            cv2.rectangle(img, (50,int(volBar)), (85,400), (0,255,0),cv2.FILLED)
            cv2.putText(img, str(int(volPer)), (40,450),cv2.FONT_HERSHEY_PLAIN,3,(0,255,0),3)
            cVol=int(volume.GetMasterVolumeLevelScalar()*100)
            cv2.putText(img, str(int(cVol)), (400,50),cv2.FONT_HERSHEY_PLAIN,3,colorVol,3)
            #framerate
            cTime=time.time()
            fps=1/(cTime-pTime)
            pTime=cTime
            cv2.putText(img, str(int(fps)), (10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)   
            
            
            #print(lmList[4],lmList[8])
 


        
    
    
     
    
    cv2.imshow("Img",img)
    if cv2.waitKey(1)& 0xFF == ord('q'):
        break




cap.release()
cv2.destroyAllWindows()
