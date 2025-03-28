import cv2
from cv2.gapi import BGR2RGB
import mediapipe as mp
import time
class Mesh():
    def __init__(self,static_mode=False,max_faces=1):
        self.static_mode = static_mode
        self.max_faces = max_faces

        self.mpdraw = mp.solutions.drawing_utils 
        self.mpfacemesh = mp.solutions.face_mesh
        self.facemesh = self.mpfacemesh.FaceMesh(self.static_mode,self.max_faces)
        self.drawspec = self.mpdraw.DrawingSpec(thickness=1, circle_radius=1)

    def findposition(self, img,draw=True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        res = self.facemesh.process(img_rgb)
        faces = []
        self.lxm = []
        self.lym = []
        if res.multi_face_landmarks:
            face = []
            for facelm in res.multi_face_landmarks:
                if draw:
                    self.mpdraw.draw_landmarks(img,facelm,self.mpfacemesh.FACEMESH_TESSELATION,self.drawspec,self.drawspec)
                for id , lm in enumerate(facelm.landmark):
                    h , w , c= img.shape 
                    x , y = int(lm.x * w) , int(lm.y * h)
                    self.lxm.append(x)
                    self.lym.append(y)
                    # cv2.putText(img,str(id),(x,y),cv2.FONT_HERSHEY_PLAIN,0.7,(0,255,0),1)
                    face.append([id,x,y])
                faces.append(face)
        return  faces

    def get_bbox(self,img,draw=True,incr=0,color=(0,255,0)):
        xmin , ymin = min(self.lxm) , min(self.lym)
        xmax , ymax = max(self.lxm) , max(self.lym)
        bbox =  xmin-incr , ymin-incr , xmax+incr , ymax+incr
        if draw:
            cv2.rectangle(img,(bbox[0],bbox[1]),(bbox[2],bbox[3]),color,cv2.FILLED)
        return bbox

def main():
    cap = cv2.VideoCapture(0)
    ptime = 0 
    ctime = 0 
    detect = Mesh()
    while True :
        suc , img = cap.read()
        img , ls = detect.findposition(img)
        if len(ls) != 0:
            print(len(ls), ls)
        ctime = time.time()
        fps = 1/(ctime-ptime)
        ptime = ctime
        cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 5, (0,255,0), 5)
        cv2.imshow("dd1", img)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
