import cv2 
import time 
from handtrack import HandDetector
import numpy as np

capture = cv2.VideoCapture(0)
# w = 1024
# h = 576
# capture.set(cv2.CAP_PROP_FRAME_WIDTH, w)
# capture.set(cv2.CAP_PROP_FRAME_HEIGHT, h)


ptime , ctime = 0 , 0
de = HandDetector()
colors = [(0,0,0), (255,255,0), (0, 255, 0), (0, 0, 255),(255,255,255)]
colors_name = ["black","blue","green","red","white"]
# x: 640, y: 480 of camera
imgcan = np.ones((480,640,3),np.uint8) 
draw = False
cc = (0,0,0)
counter_1 = 0
while True:
    sucess , img = capture.read()
    img = de.findHands(img)
    cordinations = de.findPosition(img,landmark=8,draw=False)
    counter = 70
    circles = []
    rectangle = []
    for i in colors:
        rad = 45
        top_left = x , y = (counter-rad,70-rad) # white
        down_right = x1 ,y1 = (counter+rad,70+rad) # black

        cv2.circle(img,(counter,70),rad,i,cv2.FILLED)
        # cv2.rectangle(img,down_right,top_left,(0,255,255),2)

        circles.append([counter,70])

        # rectangle.append([top_left,down_right])
        rectangle.append([top_left,down_right])
        counter += 120

    black_x, black_y = circles[0][:]
    blue_x, blue_y = circles[1][:]
    green_x, green_y = circles[2][:]
    red_x, red_y = circles[3][:]
    white_x, white_y = circles[4][:] 
                                   # [top_left,down_right]
    rectangle_black = rectangle[0] # [(25, 25), (115, 115)]
    rectangle_blue = rectangle[1]
    rectangle_green = rectangle[2]
    rectangle_red = rectangle[3]
    rectangle_white = rectangle[4]
    
    if len(cordinations) != 0:
        lmx , lmy = cordinations[8][1:]
        if lmx > rectangle_black[0][0] and  lmy > rectangle_black[0][1]  and lmx < rectangle_black[1][0] and lmy < rectangle_black[1][1]:
            cc = colors[0]
            draw = True

        elif lmx > rectangle_blue[0][0] and  lmy > rectangle_blue[0][1]  and lmx < rectangle_blue[1][0] and lmy < rectangle_blue[1][1]:
            cc = colors[1]
            draw = True

        elif lmx > rectangle_green[0][0] and  lmy > rectangle_green[0][1]  and lmx < rectangle_green[1][0] and lmy < rectangle_green[1][1]:
            cc = colors[2]
            draw = True
        elif lmx > rectangle_red[0][0] and  lmy > rectangle_red[0][1]  and lmx < rectangle_red[1][0] and lmy < rectangle_red[1][1]:
            cc = colors[3]
            draw = True
        elif lmx > rectangle_white[0][0] and  lmy > rectangle_white[0][1]  and lmx < rectangle_white[1][0] and lmy < rectangle_white[1][1]:
            cc = colors[4]
            draw = True

        th = 5
        if cordinations[8][2] < cordinations[6][2] and cordinations[12][2] < cordinations[10][2]:
            cv2.line(img,(cordinations[8][1],cordinations[8][2]),(cordinations[12][1],cordinations[12][2]),(0,255,255),th)
            cv2.circle(img,(cordinations[12][1],cordinations[12][2]),5,(0,255,255),cv2.FILLED)
            dark = False
            draw = False
        if cordinations[8][2] < cordinations[6][2] and cordinations[20][2] < cordinations[18][2]:
            cv2.line(img,(cordinations[8][1],cordinations[8][2]),(cordinations[20][1],cordinations[20][2]),(255,0,255),th)
            cv2.circle(img,(cordinations[20][1],cordinations[20][2]),5,(255,0,255),cv2.FILLED)
            imgcan[:] = (0, 0, 0)
        what_color_whoami = [(i, y) for i, y in zip(colors_name, colors) if cc == y][0][0]
        print(f"{counter_1} D Stat : {draw} , color : {what_color_whoami}")
        counter_1 += 1
        # color needed in BGR codes
        cv2.putText(img,f"D Stat : {draw}",(10,395),cv2.FONT_HERSHEY_TRIPLEX,0.8,(103,224,255)) 
        cv2.circle(img,(cordinations[8][1],cordinations[8][2]),6,cc,cv2.FILLED)
        cv2.putText(img,f"color : {what_color_whoami}",(400,450),cv2.FONT_HERSHEY_TRIPLEX,1,cc)

        if draw:
            if lmy > rectangle_blue[1][1]+35:
                cv2.circle(imgcan,(cordinations[8][1],cordinations[8][2]),15,cc,cv2.FILLED)

    ctime = time.time()
    fps = 1/(ctime-ptime)
    ptime = ctime 
    imgg = cv2.cvtColor(imgcan,cv2.COLOR_BGR2GRAY)
    _ , imgInv  = cv2.threshold(imgg,50,255,cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
    img2 = cv2.bitwise_and(imgInv,img)
    img = cv2.bitwise_or(img2,imgcan)
    cv2.putText(img,f"FPS : {int(fps)}",(10,450),cv2.FONT_HERSHEY_TRIPLEX,1,(255,0,0))
    cv2.putText(img,"Eraser",(45,70),cv2.FONT_HERSHEY_PLAIN,1,colors[4])
    cv2.imshow("j", img)
    if  cv2.waitKey(1) & 0xFF == 27:
            break
capture.release()
cv2.destroyAllWindows()

