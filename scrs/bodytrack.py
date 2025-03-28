import cv2 
import mediapipe as mp 
import time
import math 
class BodyDetector():
    def __init__(self, model_complexity=1, static_image_mode=False, smooth_landmarks=True, enable_segmentation=False, smooth_segmentation=True,min_detection_confidence=0.5, min_tracking_confidence=0.5):

                self.static_image_mode = static_image_mode
                self.model_complexity = model_complexity
                self.smooth_landmarks = smooth_landmarks
                self.enable_segmentation = enable_segmentation
                self.smooth_segmentation = smooth_segmentation
                self.min_detection_confidence = min_detection_confidence
                self.min_tracking_confidence = min_tracking_confidence

                self.mpd  = mp.solutions.drawing_utils
                self.mpPose = mp.solutions.pose 
                self.pose = self.mpPose.Pose(self.model_complexity, self.smooth_landmarks, self.enable_segmentation, self.smooth_segmentation, self.min_detection_confidence, self.min_tracking_confidence)

    def drawit(self, img, draw=True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.res = self.pose.process(img_rgb)
        gre_con = self.mpd.DrawingSpec(color=(0,255,0), thickness=2, circle_radius=2)
        if self.res.pose_landmarks :
            if draw:
                self.mpd.draw_landmarks(img, self.res.pose_landmarks, self.mpPose.POSE_CONNECTIONS, connection_drawing_spec=gre_con)

        return img
    
    def getposition(self,img,landmark=None,draw=True):
        self.lm_ls = []
        if self.res.pose_landmarks:
            for id , lm in enumerate(self.res.pose_landmarks.landmark):
                h ,w ,c = img.shape
                cx = int(lm.x * w)
                cy = int(lm.y * h)
                self.lm_ls.append([id , cx , cy])
                if draw :
                    if landmark == id :
                        cv2.circle(img , (cx , cy) , 7 , (255,255,0), cv2.FILLED)



        return self.lm_ls
    def findAngle(self,img,p1,p2,p3,draw=True,draw_connection_p1_p3=False):

        x1,y1 = self.lm_ls[p1][1:]
        x2,y2 = self.lm_ls[p2][1:]
        x3,y3 = self.lm_ls[p3][1:]
        angle1 = math.atan2(y3-y2, x3-x2)
        angle2 = math.atan2(y1-y2, x1-x2)

        angle = math.degrees(angle1 - angle2) 
        print(angle)

        if draw:
            cv2.circle(img , (x1 , y1) , 5 , (255,255,0), cv2.FILLED)
            cv2.line(img,(x1,y1),(x2,y2),(255,255,255),2)
            cv2.circle(img , (x2 , y2) , 5 , (255,255,0), cv2.FILLED)
            cv2.line(img,(x2,y2),(x3,y3),(255,255,255),2)
            cv2.circle(img , (x3 , y3) , 5 , (255,255,0), cv2.FILLED)
            if draw_connection_p1_p3:
                cv2.line(img,(x3,y3),(x1,y1),(255,255,255),2)

        
def main(landmark=None):
    if landmark is not None:
        try:
            landmark = int(landmark)
        except ValueError:
            print("Error: Landmark must be an integer.")
            quit()
    # vd = "vd/th.mp4"
    cap = cv2.VideoCapture(0)
    ptime = 0
    ctime = 0
    detector = BodyDetector()  # Create an instance of the BodyDetector class
    while True:
        suc , img = cap.read()
        if not suc:
            break
        img = detector.drawit(img)
        ls = detector.getposition(img,landmark)
        if len(ls) != 0 :
            if landmark is None:
                print(ls)

            else:
                print(ls[landmark])

        ctime = time.time()
        fps = 1/(ctime-ptime)
        ptime = ctime
        cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 5, (0,255,0), 5)
        cv2.imshow("dd", img)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main(20)
    

