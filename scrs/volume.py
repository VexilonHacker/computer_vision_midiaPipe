import cv2 
import numpy 
import time
import handtrack as ht
import math 
import alsaaudio

cap = cv2.VideoCapture(0)
ptime, ctime = 0, 0 

detec = ht.HandDetector()

def increase_volume(increment=5):
    mixer = alsaaudio.Mixer()
    current_volume = mixer.getvolume()[0]
    new_volume = min(current_volume + increment, 100)  # Cap at 100
    mixer.setvolume(new_volume)

def decrease_volume(decrement=5):
    mixer = alsaaudio.Mixer()
    current_volume = mixer.getvolume()[0]
    new_volume = max(current_volume - decrement, 0)  # Cap at 0
    mixer.setvolume(new_volume)

def get_volume():
    mixer = alsaaudio.Mixer()
    current_volume = mixer.getvolume()[0]
    return current_volume

st = 0
xs = 0
while True:
    suc, img = cap.read()
    ctime = time.time() 
    img = detec.findHands(img)
    ls = detec.findPosition(img, landmark=8, draw=False)
    
    if len(ls) != 0:
        x1, y1 = ls[4][1], ls[4][2]
        x2, y2 = ls[8][1], ls[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

        leng = math.hypot(x2 - x1, y2 - y1)
        le = int((leng / 100) * 10)
        volume = get_volume()
        
        # Draw the volume percentage text
        cv2.putText(img, f"{volume}% volume", (40, 450), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3)

        # Draw the volume bar || that part was with help of AI
        # bar_width = 30
        # bar_height = 300
        # bar_x = 50
        # bar_y = 100
        # cv2.rectangle(img, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height), (0, 255, 0), 3)  # Outline
        # filled_height = int((volume / 100) * bar_height)
        # cv2.rectangle(img, (bar_x, bar_y + (bar_height - filled_height)), (bar_x + bar_width, bar_y + bar_height), (0, 255, 0), cv2.FILLED)

        if st != 0:
            if le != xs:
                if le > xs:
                    increase_volume(le)
                elif le < xs:
                    decrease_volume(le)

        else:
            increase_volume(le)
        xs = le
        st += 1

    fps = 1 / (ctime - ptime)
    ptime = ctime
    cv2.putText(img, f"{int(fps)}", (40, 70), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3)

    cv2.imshow("hello", img)
    cv2.waitKey(1)

