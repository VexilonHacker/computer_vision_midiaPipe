import cv2 
import time 
ptime , ctime = 0 , 0 
cap = cv2.VideoCapture(0)
# resolution = "1920x1080"
#
# # Split the resolution into width and height
# width, height = map(int, resolution.split('x'))
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
while True :
    suc , img = cap.read()
    ctime = time.time()
    fps = int(1/(ctime-ptime))
    cv2.putText(img,f"FPS : {fps}",(100,100),cv2.FONT_HERSHEY_TRIPLEX,1,(0,255,0),3)
    ptime = ctime
    cv2.imshow("f",img)
    cv2.waitKey(1)
