import cv2
import mediapipe as mp
import time
class FaceDetector():
    def __init__(self,mindetection=0.5):
        self.mindetection = mindetection
        self.mpface = mp.solutions.face_detection
        self.mpdraw = mp.solutions.drawing_utils
        self.mpdface = self.mpface.FaceDetection(self.mindetection)

    def findfaces(self,img,draw=True,fancy=False,landmarks_with_detection_value=False,only_landmarks=False,incr=0):
        img_rgb = cv2.cvtColor(img , cv2.COLOR_BGR2RGB)
        res = self.mpdface.process(img_rgb)
        data = []
        if res.detections:
            for id , lm in enumerate(res.detections):
                y ,x , z = img.shape
                bboxC = lm.location_data.relative_bounding_box

                bbox = int(bboxC.xmin* x)-incr , int(bboxC.ymin * y)-incr-incr ,\
                       int(bboxC.width * x)+incr*2 , int(bboxC.height * y)+incr*3
                    
                gre_con = self.mpdraw.DrawingSpec(color=(0,255,0), thickness=2, circle_radius=2)
                if draw:
                    if only_landmarks:
                        self.mpdraw.draw_detection(img,lm,bbox_drawing_spec=gre_con)
                    else:
                        if fancy:
                            img = self.fancy(img,bbox)

                        cv2.rectangle(img,bbox,(0,255,0),2) 

                        # cv2.rectangle(img,(bbox[0],bbox[1]),(bbox[2],bbox[3]),(0,255,0),2) 
                        cv2.putText(img, str(int(lm.score[0]*100)), (bbox[0],bbox[1]-20), cv2.FONT_HERSHEY_PLAIN, 5, (0,255,0), 5)
                        if landmarks_with_detection_value:
                            self.mpdraw.draw_detection(img,lm,bbox_drawing_spec=gre_con)
                data.append([bbox , lm.score[0]])
        return  data

    def fancy(self, img, bbox,l=30,t=10,cc=(0,255,0)):
        x , y , w , h = bbox 
        x1 , y1 = x+w , y+h
        cv2.rectangle(img,bbox,cc,1) 
        # Top left Corner
        cv2.line(img,(x,y),(x+l,y),cc,t)
        cv2.line(img,(x,y),(x,y+l),cc,t)
        # down Right ..
        cv2.line(img,(x1,y1),(x1-l,y1),cc,t)
        cv2.line(img,(x1,y1),(x1,y1-l),cc,t)
        # Down left Corner
        cv2.line(img,(x1,y),(x1-l,y),cc,t)
        cv2.line(img,(x1,y),(x1,y+l),cc,t)

        cv2.line(img,(x,y1),(x+l,y1),cc,t)
        cv2.line(img,(x,y1),(x,y1-l),cc,t)

         

        return img


        

def main():
    cap = cv2.VideoCapture(0)
    ptime = 0 
    ctime = 0 
    detect = FaceDetector()
    while True :
        suc , img = cap.read()
        ls = detect.findfaces(img,draw=True)
        
        if len(ls) != 0:
            print(ls)
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
    main()
