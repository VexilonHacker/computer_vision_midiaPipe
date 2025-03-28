import cv2 
from cv2.aruco import detectMarkers
import mediapipe as mp 
import time
import handtrack

cap = cv2.VideoCapture(0)
resolution = "1024x576"
# Split the resolution into width and height
width, height = map(int, resolution.split('x'))

cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

ctime , ptime = 0 , 0 
detect = handtrack.HandDetector()
bi  = [8,12,16,20,4]
sa = [6,10,14,18,3]
while True:
    su , img = cap.read()
    img = detect.findHands(img)
    ls = detect.findPosition(img)
    if len(ls) != 0:

        fs = 0
        counter = 0
        x = False
        data = []
        for id , (i,i1) in enumerate(zip(bi,sa)):
            # Hand position Detection right/left
            if ls[0][1] > ls[4][1]:
                hand_postion = "lh"
            elif ls[0][1] < ls[4][1]:
                hand_postion = "rh"

            # Finger Status Detection
            y = ls[i][2]
            y1 = ls[i1][2]
            if y > y1:
                msg = f"finger {id+1} is downed"
                print(msg)
                if id == fs:
                    cv2.putText(img,str(id+1),(40,140),cv2.FONT_HERSHEY_PLAIN,3,(255,255,0),4)
                    x = True
                    data.append(id)
                elif id != fs :
                    counter += 50
                    cv2.putText(img,str(id+1),(40,140+counter),cv2.FONT_HERSHEY_PLAIN,3,(255,255,0),4)
                    x = True
                    data.append(id)
                
                fs = id

             
            elif id == 4:
                x0 = ls[i][1]
                x1 = ls[i1][1]
                if hand_postion == "lh":
                    cv2.putText(img,"left Hand",(400,70),cv2.FONT_HERSHEY_TRIPLEX,1,(0,255,255))
                    if x0> x1 :
                        counter += 50

                        cv2.putText(img,str(id+1),(40,140+counter),cv2.FONT_HERSHEY_PLAIN,3,(255,255,0),4)
                        msg = f"finger {id+1} is downed"
                        print(msg)
                        x = True
                        data.append(id)

                if hand_postion == "rh":
                    cv2.putText(img,"right Hand",(400,70),cv2.FONT_HERSHEY_TRIPLEX,1,(0,255,255))
                    if x0 < x1 :
                        counter += 50
                        data.append(id)
                        cv2.putText(img,str(id+1),(40,140+counter),cv2.FONT_HERSHEY_PLAIN,3,(255,255,0),4)
                        msg = f"finger {id+1} is downed"
                        print(msg)
                        x = True

        if x:
            how_much = int(len(data)/5 * 100)
            cv2.putText(img,f"Fingers {how_much}%",(15,400),cv2.FONT_HERSHEY_PLAIN,3,(255,215,0),4)
            data.clear()
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    ctime = time.time()
    fps = 1/(ctime-ptime)
    ptime = ctime
    cv2.putText(img,f"FPS: {int(fps)}",(10,70),cv2.FONT_HERSHEY_PLAIN,3,(0,255,0),3)
    cv2.imshow('Hand Tracking', img)
    if cv2.waitKey(1) & 0xFF == 27:
        break


cap.release()
cv2.destroyAllWindows()

