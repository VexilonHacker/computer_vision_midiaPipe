import pyautogui as pya 
import cv2
import mediapipe as mp
import time
import warnings
warnings.filterwarnings("ignore")
pya.FAILSAFE = False
pya.PAUSE = 0.01

class HandDetector():
    def __init__(self,mode=False,maxHands=2):
        self.mode = mode
        self.maxHands = maxHands

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,self.maxHands)
        self.mpd = mp.solutions.drawing_utils
    
    def findHands(self,img,draw=True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.res = self.hands.process(img_rgb)
        if self.res.multi_hand_landmarks:
            for hand in self.res.multi_hand_landmarks:
                if draw:
                    gre_con = self.mpd.DrawingSpec(color=(0,255,0), thickness=2, circle_radius=2)
                    self.mpd.draw_landmarks(img, hand, self.mpHands.HAND_CONNECTIONS,connection_drawing_spec=gre_con)
        return img

    def findPosition(self, img, handNum=0, draw=True,landmark=None):
        lml = []
        if self.res.multi_hand_landmarks: 
            hand = self.res.multi_hand_landmarks[handNum] 
            for id,lm  in enumerate(hand.landmark):
                h , w , c = img.shape
                cx , cy = int(lm.x * w) , int(lm.y * h)
                w , h = pya.size()
                cx1 , cy1 = int(lm.x*w) , int(lm.y * h)
                lml.append([id ,cx1, cy1, cx , cy])
                if draw:
                    if id == landmark:
                        if landmark == 12:
                            cv2.circle(img , (cx , cy) , 7 , (255,0,255), cv2.FILLED)
                        else:
                            cv2.circle(img , (cx , cy) , 7 , (255,255,0), cv2.FILLED)
                    elif landmark is None:
                        cv2.circle(img , (cx , cy) , 7 , (255,255,0), cv2.FILLED)
        return lml

    def findBoundingBox(self, img, handNum=0):
        x_min, x_max, y_min, y_max = float('inf'), float('-inf'), float('inf'), float('-inf')
        if self.res.multi_hand_landmarks: 
            hand = self.res.multi_hand_landmarks[handNum] 
            for lm in hand.landmark:
                h, w, c = img.shape
                x, y = int(lm.x * w), int(lm.y * h)
                x_min, x_max = min(x_min, x), max(x_max, x)
                y_min, y_max = min(y_min, y), max(y_max, y)
        return (x_min, y_min, x_max, y_max)

def main():
    landmark = 8
    cap = cv2.VideoCapture(0)
    # FPS 10-9
    # w = 1280
    # h = 720
    # FPS 13-12
    w = 1024
    h = 576
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, w)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)

    ptime = 0
    ctime = 0
    detect = HandDetector()
    while True:
        succ, img = cap.read()
        if not succ:
            print("Cannot read frame")
            break

        img = detect.findHands(img)
        ls = detect.findPosition(img,landmark=landmark)
        detect.findPosition(img,landmark=landmark+4)
        if len(ls) != 0:
            bbox = detect.findBoundingBox(img)
            impvr = 15
            cv2.rectangle(img, (bbox[0]-impvr, bbox[1]-impvr), (bbox[2]+impvr, bbox[3]+impvr), (0, 255, 0), 2)

            # first finger // click
            x, y = ls[landmark][1] , ls[landmark][2]
            y1 =  ls[landmark-2][2]
            # Second Finger // right click
            yy =ls[landmark+4][2]
            y2 = ls[landmark+2][2]

            if y1<=y :                                
                pya.click(x ,y)
                print(f"LEFT_CLICK [Screen (x : {x} ,y : {y}) , Camera (x : {ls[landmark][3]} , y : {ls[landmark][4]})]")
            elif y2 <= yy:
                pya.rightClick(x,y)
                print(f"RIGHT_CLICK [Screen (x : {x} ,y : {y}) , Camera (x : {ls[landmark][3]} , y : {ls[landmark][4]})]")
            else:
                pya.moveTo(x,y,duration=0)
                print(f"MOVE [Screen (x : {x} ,y : {y}) , Camera (x : {ls[landmark][3]} , y : {ls[landmark][4]})]")
        ctime = time.time()
        fps = 1/(ctime-ptime)
        ptime = ctime
        cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(0,255,0),3)
        cv2.imshow('Hand Tracking', img)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()



