import time
import datetime
import cv2
from keras.models import load_model, model_from_json
from time import sleep
from keras.preprocessing.image import img_to_array
from keras.preprocessing import image
import cv2
import numpy as np
# setting to to app run
eight_hours = datetime.timedelta(minutes=1)
now = datetime.datetime.now()
later = now + eight_hours

# load json and create model
json_file = open('C:\\Users\\shadow\\OneDrive\\Desktop\\python\\Final Year Project\\Model\\emotion_model1.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
emotion_model = model_from_json(loaded_model_json)

# load weights into new model
emotion_model.load_weights("C:\\Users\\shadow\\OneDrive\\Desktop\\python\\Final Year Project\Model\\emotion_model1.h5")
print("Loaded model from disk")

emotion_dict = {0: "neutral", 1: "stress"}




cap = cv2.VideoCapture(0)
while True:
    # Find haar cascade to draw bounding box around face
    ret, frame = cap.read()
    # frame = cv2.resize(frame, (1240, 720))
    if not ret:
        break
    face_detector = cv2.CascadeClassifier('C:\\Users\\shadow\\OneDrive\\Desktop\\python\\Final Year Project\\haarcascode\\haarcascade_frontalface_default.xml')
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # detect faces available on camera9
    num_faces = face_detector.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5)

    # take each face available on the camera and Preprocess it
    for (x, y, w, h) in num_faces:
        cv2.rectangle(frame, (x, y-50), (x+w, y+h+10), (0, 255, 0), 4)
        roi_gray_frame = gray_frame[y:y + h, x:x + w]
        cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray_frame, (48, 48)), -1), 0)

        # predict the emotions
        emotion_prediction = emotion_model.predict(cropped_img)
        
        maxindex = int(np.argmax(emotion_prediction))
        print(emotion_dict[maxindex])
        cv2.putText(frame, emotion_dict[maxindex], (x+5, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(frame,'No Faces',(30,80),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
    cv2.imshow('Emotion Detector',frame)
    # Exit the loop if the end time has been reached
    if now >= later:
        break
    
    # Wait for 1 second before running the loop again
    time.sleep(5)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()