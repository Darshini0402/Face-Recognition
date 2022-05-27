import cv2
import os
from .simple_facerec import SimpleFacerec
import face_recognition

class faceload:

    def facesave(username):

        sfr = SimpleFacerec()

        cap = cv2.VideoCapture(0)
        sfr.load_encoding_images("ProfileImages/")
        
        while True:

            ret, frame = cap.read()

            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            MEDIA_ROOT = os.path.join(BASE_DIR,'ProfileImages\\')
            fname = MEDIA_ROOT + username + ".jpg"
            
            cv2.imwrite(fname,frame)

            face_locations, face_names = sfr.detect_known_faces(frame)
            
            for face_loc, name in zip(face_locations, face_names):
                y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0,0,200), 4)
            
            cv2.imshow("Frame", frame)

            key = cv2.waitKey(1)
            if key == 27:
                break

        cap.release()
        cv2.destroyAllWindows()  