#https://www.youtube.com/watch?v=8gPONnGIPgw
import cv2
import numpy as np
import HandTracking_module as htm
import time
import math
import autopy

##################################
wCam,hCam=640,480
############################


cap=cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
pTime=0
wScr,hScr=autopy.screen.size()
frameR=100
smoothening=7
plocX,plocY=0,0
clocX,clocY=0,0

detector=htm.handDetector(maxHands=1)

while True:
    #1      Find hand landmarks
    success, img =cap.read()
    img=cv2.flip(img, 1)
    img=detector.findHands(img)
    lmList, bbox=detector.findPosition(img)
    
    
    #2      Get tip of the index and middel finger
    if len(lmList)!=0:
        x1,y1=lmList[8][1:]
        x2,y2=lmList[12][1:]
        
        
    #3      Check which fingers are up
        fingers=detector.fingersUp()
        cv2.rectangle(img, (frameR,frameR),(wCam-frameR,hCam-frameR),(255,0,255),2)
    
    #4      Only index finger(Moving mode)
        if fingers[1]==1 and fingers[2]==0:
            
    #5      Covert Coordinates
            
            x3=np.interp(x1,(frameR,wCam-frameR),(0,wScr))
            y3=np.interp(y1,(frameR,hCam-frameR),(0,hScr))
    #6      Smoothing values
            clocX=plocX+(x3-plocX)/smoothening
            clocY=plocY+(y3-plocY)/smoothening
    
    #7      Move mouse
            autopy.mouse.move(clocX, clocY)
            cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
            plocX,plocY=clocX,clocY
            
    #8      Check if we are in clicking mode(both index and middle finger up)
        if fingers[1]==1 and fingers[2]==1:
            #9      Find distance between fingers
            length, img,lineinfo=detector.findDistance(8,12, img)
            #10     Click mouse if distance is short
            if length<40:
                cv2.circle(img,(lineinfo[4],lineinfo[5]),15,(0,255,0),cv2.FILLED)
                autopy.mouse.click()
    
    
    
    
    #11     Check frame rate
    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img, str(int(fps)), (10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)


    #12     Display
    cv2.imshow("Img",img)
    if cv2.waitKey(1)& 0xFF == ord('q'):
        break




cap.release()
cv2.destroyAllWindows()


