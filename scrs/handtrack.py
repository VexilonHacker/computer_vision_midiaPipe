import cv2
import mediapipe as mp
import time

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
                    self.gre_con = self.mpd.DrawingSpec(color=(0,255,0), thickness=2, circle_radius=2)
                    self.mpd.draw_landmarks(img, hand, self.mpHands.HAND_CONNECTIONS,connection_drawing_spec=self.gre_con)
        return img

    def findPosition(self, img, handNum=0, draw=True,landmark=None,draw_numbers=False):
        self.lml = [] 
        self.xs = []
        self.ys = []
        if self.res.multi_hand_landmarks: 
            hand = self.res.multi_hand_landmarks[handNum] 
            for id,lm  in enumerate(hand.landmark):
                h , w , c = img.shape
                cx , cy = int(lm.x * w) , int(lm.y * h)
                self.xs.append(cx)
                self.ys.append(cy)
                self.lml.append([id , cx , cy])
                if draw:
                    if id == landmark:
                        cv2.circle(img , (cx , cy) , 7 , (255,255,0), cv2.FILLED)
                    elif landmark is None:
                        self.mpd.draw_landmarks(img, hand, self.mpHands.HAND_CONNECTIONS,connection_drawing_spec=self.gre_con)
                if draw_numbers:                        
                    cv2.putText(img,str(id),(cx,cy),cv2.FONT_HERSHEY_PLAIN,2.5,(255,255,255),3)



        return self.lml

    def get_bounding_box(self,img,draw_bounding_box=False,color=(0,255,0),thickness=3):
        if len(self.xs) != 0 and len(self.ys) != 0 :
            add = 15
            xmin , xmax = min(self.xs) , max(self.xs)
            ymin  , ymax = min(self.ys) , max(self.ys)
            bbox =  xmin-add , ymin-add , xmax+add , ymax+add

            if draw_bounding_box:
                cv2.rectangle(img,(bbox[0],bbox[1]),(bbox[2],bbox[3]),color,thickness)
            return bbox
        else : 
            return None

    def hand_direction(self):
        hand_postion = False
        if self.lml[0][1] > self.lml[4][1]:
            hand_postion = "lh"
        elif self.lml[0][1] < self.lml[4][1]:
                hand_postion = "rh"
        if not hand_postion :
            return None 
        else :
            return hand_postion

def main(landmark=None,activate_box=False):
    cap = cv2.VideoCapture(0)
    ptime = 0
    ctime = 0
    detect = HandDetector()
    x = 0
    while True:
        succ, img = cap.read()
        if not succ:
            print("Cannot read frame")
            break
        img = detect.findHands(img)
        ls = detect.findPosition(img,landmark=landmark,draw_numbers=False)
        if activate_box:
            detect.get_bounding_box(img,True)
        if len(ls) != 0:
            if landmark is None :
                print(ls[:])
                pass
            elif landmark:
                print(ls[landmark])
                pass

        ctime = time.time()
        fps = 1/(ctime-ptime)
        ptime = ctime
        x +=1
        cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(0,255,0),3)
        cv2.imshow('Hand Tracking', img)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main(8,True)

