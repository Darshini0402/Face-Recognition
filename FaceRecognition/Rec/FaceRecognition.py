import cv2
import os
from .simple_facerec import SimpleFacerec
import face_recognition

class facerec:

    def facecomp(username):

        sfr = SimpleFacerec()

        cap = cv2.VideoCapture(0)
        sfr.load_encoding_images("ProfileImages/")
        cnt = 0
        for i in range (100):
            ret, frame = cap.read()

            face_locations, face_names = sfr.detect_known_faces(frame)

            if(len(face_names)!=0):
                if(face_names[0]==username):
                    return True
                elif(face_names[0]=="Unknown"):
                    cnt+=1
            if cnt==100:
                cap.release()
                cv2.destroyAllWindows()  
                return False

            #print(face_names)

            for face_loc, name in zip(face_locations, face_names):
                y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]

                #cv2.putText(frame, name, (x1, y1-10), cv2.FONT_HERSHEY_DUPLEX, 1, (0,0,0), 2)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0,0,200), 4)
            
            cv2.imshow("Frame", frame)

            key = cv2.waitKey(1)
            if key == 27:
                break

        cap.release()
        cv2.destroyAllWindows()  