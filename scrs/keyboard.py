import cv2 
import time
from handtrack import HandDetector
# camera 480 / 640
capture  = cv2.VideoCapture(0)

# resolution = "1024x576"
resolution = "480x640"
# Split the resolution into width and height
width, height = map(int, resolution.split('x'))

capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

ptime,ctime = 0 , 0
de = HandDetector()
aze = [
    'A', 'Z', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P',
    'Q', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M',
    'W', 'X', 'C', 'V', 'B', 'N', ':', ',', '.', '/'
]
xdo = 0
letters = []
backspace_pressed = False
reapted_word = None
cleared = False
show_landmark_12 = True
while True :
    suc , img = capture.read()
    img = de.findHands(img) 
    ls = de.findPosition(img)
    counter , counter1 , counter2 = 40 , 40, 40
    y, y1, y2 = 100, 180, 260
    white  = (255,255,255)
    grey = (132,132,135)#(0,0,0)
    green = (0,255,0)
    sky_blue = (240,255,97)
    black = (0,0,0)
    yellow = (0,255,255)
    voilet = (255,128,149)
    red = (51,51,255)
    sq = 30
    data = []
    if ls:
        hand_pos = de.hand_direction()
        lmx , lmy = ls[8][1:]
        clear_all , clear_all1 = (10,310) , (110,380)
        space_bar_xy , space_bar_xy1 = (120,310) , (490,380)
        Backspace_key, Backspace_key1 = (500,310) , (610,380)

        # space_bar_xy , space_bar_xy1 = (40,310) , (590,380)
        # Backspace key 
        cv2.rectangle(img,Backspace_key,Backspace_key1,grey,cv2.FILLED) 
        cv2.rectangle(img,Backspace_key,Backspace_key1,green,3) 
        cv2.putText(img,"<- DEL",(510, 355),cv2.FONT_HERSHEY_TRIPLEX,0.7,white,2)
        
        # Delete_all
        cv2.rectangle(img,clear_all,clear_all1,grey,cv2.FILLED) 
        cv2.rectangle(img,clear_all,clear_all1,green,3) 
        cv2.putText(img,"Del All",(15, 355),cv2.FONT_HERSHEY_TRIPLEX,0.8,white,2)

        # Space Bar
        cv2.rectangle(img,space_bar_xy,space_bar_xy1,grey,cv2.FILLED) 
        cv2.rectangle(img,space_bar_xy,space_bar_xy1,green,3) 
        cv2.putText(img,"SPACE BAR",(215, 355),cv2.FONT_HERSHEY_TRIPLEX,1,white,2)

        for num , alpha in enumerate(aze):
            if num <= 9:
                cord0 = counter+sq , y +sq
                cord1 = counter-sq , y-sq
                cv2.rectangle(img,(cord0),(cord1),grey,-1)
                cv2.putText(img,alpha,(counter,y),cv2.FONT_HERSHEY_TRIPLEX,1,white)
                cv2.rectangle(img,(cord0),(cord1),green,5)
                cv2.addWeighted(img.copy(), 0.5, img, 1 - 0.5, 0, img)
                counter +=  60
                data.append(["+",alpha,cord1,cord0])

            elif 9<num<=19:
                cord2 = counter1+sq , y1 +sq
                cord3 = counter1-sq , y1-sq
                cv2.rectangle(img,(cord2),(cord3),grey,-1)
                cv2.putText(img,alpha,(counter1,y1),cv2.FONT_HERSHEY_TRIPLEX,1,white)
                cv2.rectangle(img,(cord2),(cord3),green,5)
                counter1 += 60
                data.append(["-",alpha,cord3,cord2])

            elif 19<num:
                cord4 = counter2+sq , y2 +sq
                cord5 = counter2-sq , y2-sq
                cv2.rectangle(img,(cord4),(cord5),grey,-1)
                cv2.putText(img,alpha,(counter2,y2),cv2.FONT_HERSHEY_TRIPLEX,1,white)
                cv2.rectangle(img,(cord4),(cord5),green,5)
                counter2 += 60 
                                    # top left          bottom_right
                data.append(["*",alpha,cord5,cord4])
        for num , alpha in enumerate(data):
            if alpha[2][0] < lmx and alpha[2][1] < lmy and alpha[3][0] > lmx and alpha[3][1] > lmy:
                cv2.rectangle(img,(alpha[2]),(alpha[3]),red,5)
                if ls[11][2] > ls[12][2]:
                    # print(f"{xdo} {alpha[1]}")
                    letters.append(alpha[1])

            elif space_bar_xy[0] < lmx and space_bar_xy[1] < lmy and space_bar_xy1[0] > lmx and space_bar_xy1[1] > lmy :
                cv2.rectangle(img,(space_bar_xy),(space_bar_xy1),red,5)
                if ls[11][2] > ls[12][2]:
                    # print(f"{xdo}space bar")
                    letters.append(" ")

            elif clear_all[0] < lmx and clear_all[1] < lmy and clear_all1[0] > lmx and clear_all1[1] > lmy :
                cv2.rectangle(img,(clear_all),(clear_all1),red,5)
                if ls[11][2] > ls[12][2] and not cleared:
                    cleared = True
                    letters.clear()
                    print("Keyboard IS CLeared")

            elif Backspace_key[0] < lmx and Backspace_key[1] < lmy and Backspace_key1[0] > lmx and Backspace_key1[1] > lmy :
                cv2.rectangle(img,(Backspace_key),(Backspace_key1),red,5)
                if ls[11][2] > ls[12][2] and not backspace_pressed:
                    backspace_pressed = True
                    if letters:
                        letters.pop()
                        print("Backspace")
            else:
                backspace_pressed = False
                cleared = False
        incr = 85
        # cv2.rectangle(img,(space_bar_xy[0],space_bar_xy[1]+incr),(space_bar_xy1[0],space_bar_xy1[1]+incr),white,cv2.FILLED)
        output , output1  = (10,395) , (610,450)
        cv2.rectangle(img,output,output1,white,cv2.FILLED)
        cv2.rectangle(img,output,output1,black,5)

        cv2.circle(img,(lmx,lmy),7,sky_blue,cv2.FILLED)
        if show_landmark_12:
            cv2.circle(img,(ls[12][1],ls[12][2]),7,yellow,cv2.FILLED)
        if hand_pos == "rh":
            cv2.putText(img,"Right Hand",(420,40),cv2.FONT_HERSHEY_TRIPLEX,1,red,2)
        elif hand_pos == "lh":
            cv2.putText(img,"Left Hand",(420,40),cv2.FONT_HERSHEY_TRIPLEX,1,red,2)

        letters = [letter for i, letter in enumerate(letters) if i == 0 or letter != letters[i-1]]
        if letters:
            words  = "".join(letters)
            if words != reapted_word:
                print(f"{xdo} impvr: {words}")
                xdo += 1

            cv2.putText(img,words,(30,435),cv2.FONT_HERSHEY_TRIPLEX,1,(0,0,0),3)
            reapted_word = words
             
        # letters = list(letters)
        # print(data)
    ctime = time.time()
    fps = int(1/(ctime-ptime))
    ptime = ctime
    cv2.putText(img,f"FPS :{fps}",(15,40),cv2.FONT_HERSHEY_TRIPLEX,1,(0,255,0),2)
    cv2.imshow("s",img)
    if cv2.waitKey(1) & 0xFF == 27 :
        break
capture.release()
cv2.destroyAllWindows()

