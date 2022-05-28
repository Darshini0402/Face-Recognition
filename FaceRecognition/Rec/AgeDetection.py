# Import Libraries
import cv2
import os
import filetype
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.join(BASE_DIR,'Weights\\')

# The model architecture
AGE_MODEL = os.path.join(BASE_DIR,'deploy_age.prototxt')
#AGE_MODEL = 'Weights/deploy_age.prototxt'

# The model pre-trained weights
AGE_PROTO = os.path.join(BASE_DIR,'age_net.caffemodel')
#AGE_PROTO = 'Weights/age_net.caffemodel'

# Each Caffe Model impose the shape of the input image also image preprocessing is required like mean
# substraction to eliminate the effect of illunination changes
MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
# Represent the 8 age classes of this CNN probability layer

AGE_INTERVALS = ['(0, 2)', '(4, 6)', '(8, 12)', '(15, 18)', '(20, 32)', '(38, 43)', '(48, 53)', '(60, 100)']

FACE_PROTO = os.path.join(BASE_DIR, 'deploy.prototxt.txt')
#FACE_PROTO = "Weights/deploy.prototxt.txt"

FACE_MODEL = os.path.join(BASE_DIR,'res10_300x300_ssd_iter_140000_fp16.caffemodel')
#FACE_MODEL = "Weights/res10_300x300_ssd_iter_140000_fp16.caffemodel"

# Initialize frame size
frame_width = 1280
frame_height = 720

# load face Caffe model
face_net = cv2.dnn.readNetFromCaffe(FACE_PROTO, FACE_MODEL)
# Load age prediction model
age_net = cv2.dnn.readNetFromCaffe(AGE_MODEL, AGE_PROTO)

def get_faces(frame, confidence_threshold=0.5):
    """Returns the box coordinates of all detected faces"""
    # convert the frame into a blob to be ready for NN input
    blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), (104, 177.0, 123.0))
    # set the image as input to the NN
    face_net.setInput(blob)
    # perform inference and get predictions
    output = np.squeeze(face_net.forward())
    # initialize the result list
    faces = []
    # Loop over the faces detected
    for i in range(output.shape[0]):
        confidence = output[i, 2]
        if confidence > confidence_threshold:
            box = output[i, 3:7] * np.array([frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]])
            # convert to integers
            start_x, start_y, end_x, end_y = box.astype(np.int)
            # widen the box a little
            start_x, start_y, end_x, end_y = start_x - \
                10, start_y - 10, end_x + 10, end_y + 10
            start_x = 0 if start_x < 0 else start_x
            start_y = 0 if start_y < 0 else start_y
            end_x = 0 if end_x < 0 else end_x
            end_y = 0 if end_y < 0 else end_y
            # append to our list
            faces.append((start_x, start_y, end_x, end_y))
    return faces


def get_optimal_font_scale(text, width):
    """Determine the optimal font scale based on the hosting frame width"""
    for scale in reversed(range(0, 60, 1)):
        textSize = cv2.getTextSize(text, fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=scale/10, thickness=1)
        new_width = textSize[0][0]
        if (new_width <= width):
            return scale/10
    return 1

# from: https://stackoverflow.com/questions/44650888/resize-an-image-without-distortion-opencv
def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]
    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image
    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)
    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))
    # resize the image
    return cv2.resize(image, dim, interpolation = inter)

class agedet:

    def predict_age():
        """Predict the age of the faces showing in the image"""
        
        # create a new cam object
        cap = cv2.VideoCapture(0)

        score = 0

        for i in range (100):
            _, img = cap.read()
            # Take a copy of the initial image and resize it
            frame = img.copy()
            if frame.shape[1] > frame_width:
                frame = image_resize(frame, width=frame_width)
            faces = get_faces(frame)
            for i, (start_x, start_y, end_x, end_y) in enumerate(faces):
                face_img = frame[start_y: end_y, start_x: end_x]
                # image --> Input image to preprocess before passing it through our dnn for classification.
                blob = cv2.dnn.blobFromImage(
                    image=face_img, scalefactor=1.0, size=(227, 227), 
                    mean=MODEL_MEAN_VALUES, swapRB=False
                )
                # Predict Age
                age_net.setInput(blob)
                age_preds = age_net.forward()
                #print("="*30, f"Face {i+1} Prediction Probabilities", "="*30)
                # for i in range(age_preds[0].shape[0]):
                #     print(f"{AGE_INTERVALS[i]}: {age_preds[0, i]*100:.2f}%")
                i = age_preds[0].argmax()
                age = AGE_INTERVALS[i]
                age_confidence_score = age_preds[0][i]
                if(score<age_confidence_score):
                    score=age_confidence_score
                    final_age = age
                # Draw the box
                # label = f"Age:{age} - {age_confidence_score*100:.2f}%"
                # print(label)
                # get the position where to put the text
                yPos = start_y - 15
                while yPos < 15:
                    yPos += 15
                # # write the text into the frame
                # cv2.putText(frame, label, (start_x, yPos),
                #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), thickness=2)
                # # draw the rectangle around the face
                cv2.rectangle(frame, (start_x, start_y), (end_x, end_y), color=(255, 0, 0), thickness=2)
            # Display processed image
            cv2.imshow('Age Estimator', frame)
            if cv2.waitKey(1) == ord("q"):
                break
            # save the image if you want
            # cv2.imwrite("predicted_age.jpg", frame)
        cv2.destroyAllWindows()

        return final_age
