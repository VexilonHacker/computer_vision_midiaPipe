import cv2 
import time

from facetrack import FaceDetector

cap = cv2.VideoCapture(0)
ptime  = ctime = 0
det = FaceDetector()

while True:
    suc, frame = cap.read()  # Use cap.read() instead of cv2.read()
    if not suc:
        break
    faces = det.findfaces(frame,incr=50,draw=False)
    if faces:
        xmin , ymin = (faces[0][0][0]) , (faces[0][0][1])        
        xmax , ymax  = (faces[0][0][2]) , (faces[0][0][3]) 
        blr = 100
        print(xmax)
        frame[ymin:ymin + ymax , xmin:xmin +xmax] = cv2.blur(frame[ymin:ymin + ymax , xmin:xmin +xmax ],(blr,blr))
    ctime = time.time()
    fps = int(1/(ctime-ptime))
    ptime  = ctime 
    cv2.putText(frame,f"FPS: {fps}",(30,30),cv2.FONT_HERSHEY_TRIPLEX,1,(0,255,0),3)
    cv2.imshow("t",frame)
    if  cv2.waitKey(1) == 27 :
        break

