import cv2 
import time
from handtrack import HandDetector

cap = cv2.VideoCapture(0)
ctime,ptime = 0 , 0 
de = HandDetector()

while True:
    su , img = cap.read()
    img = de.findHands(img)
    ls = de.findPosition(img)
    bbox  = de.get_bounding_box(img,True)
    if len(ls) != 0:
        print(bbox)

    ctime = time.time()
    fps = int(1/(ctime-ptime))
    ptime = ctime
    cv2.putText(img,f"FPS :{fps}",(15,40),cv2.FONT_HERSHEY_TRIPLEX,1,(0,255,0))
    cv2.imshow("s",img)
    if cv2.waitKey(1) & 0xFF == 27 :
        break
cap.release()
cv2.destroyAllWindows()
