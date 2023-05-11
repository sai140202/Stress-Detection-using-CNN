from flask import Flask, render_template, request
from flask import Flask, render_template,request,jsonify
from flask_socketio import SocketIO, emit 
import threading,random
import time
# import numpy as np
import time
import datetime
import cv2
from keras.models import load_model, model_from_json
from time import sleep
from keras.preprocessing.image import img_to_array
from keras.preprocessing import image
import cv2
import numpy as np
from flask import Flask
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

process_thread = None
stop_process_flag = False

#testing start
eight_hours = datetime.timedelta(minutes=1)
now = datetime.datetime.now()
later = now + eight_hours

# load json and create model
json_file = open('Model\emotion_model1.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
emotion_model = model_from_json(loaded_model_json)

# load weights into new model
emotion_model.load_weights("Model\emotion_model1.h5")
print("Loaded model from disk")

emotion_dict = {0: "neutral", 1: "stress"}
#testing end
def process_function():
    global stop_process_flag
    while not stop_process_flag:
       # Flag to indicate if a face has been detected
        face_detected = False
        
        # Find haar cascade to draw bounding box around face
        cap = cv2.VideoCapture(0)
        # cap = cv2.VideoCapture(r'C:\Users\shadow\OneDrive\Desktop\python\Final Year Project\istockphoto-1383478824-640_adpp_is.mp4')

        ret, frame = cap.read()
        # frame = cv2.resize(frame, (1240, 720))
        if not ret:
            break
        face_detector = cv2.CascadeClassifier('haarcascode\haarcascade_frontalface_default.xml')
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # detect faces available on camera9
        faces = face_detector.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5)

        #     # take each face available on the camera and Preprocess it
        # for (x, y, w, h) in num_faces:
        #     cv2.rectangle(frame, (x, y-50), (x+w, y+h+10), (0, 255, 0), 4)
        #     roi_gray_frame = gray_frame[y:y + h, x:x + w]
        #     cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray_frame, (48, 48)), -1), 0)

        #     # predict the emotions
        #     emotion_prediction = emotion_model.predict(cropped_img)
            
        #     maxindex = int(np.argmax(emotion_prediction))
        #     value = emotion_dict[maxindex]
        #     print(value)

        #     #sending values
        #     socketio.emit('data', {'value': value})
            # cv2.putText(frame, emotion_dict[maxindex], (x+5, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
   
        if len(faces) > 0 and not face_detected:
            (x, y, w, h) = faces[0]
            cv2.rectangle(frame, (x, y-50), (x+w, y+h+10), (0, 255, 0), 4)
            roi_gray_frame = gray_frame[y:y + h, x:x + w]
            cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray_frame, (48, 48)), -1), 0)

            # predict the emotions
            emotion_prediction = emotion_model.predict(cropped_img)
            
            maxindex = int(np.argmax(emotion_prediction))
            value = emotion_dict[maxindex]
            print(value)

            #sending values
            socketio.emit('data', {'value': value})
                                
            cv2.putText(frame, emotion_dict[maxindex], (x+5, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
        # # cv2.putText(frame,'No Faces',(30,80),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
        cv2.imshow('Emotion Detector',frame)
        # Exit the loop if the end time has been reached
        if now >= later:
            break
        
        # Wait for 1 second before running the loop again
        # time.sleep(1)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()   


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/userpage')
def page():
    return render_template('userpage.html')


@app.route('/dashboard')
def adminpage():
    return render_template('dashboard.html')

@app.route("/start_process")
def start_process():
    global process_thread
    global stop_process_flag
    if not process_thread or not process_thread.is_alive():
        stop_process_flag = False
        process_thread = threading.Thread(target=process_function)
        # process_thread.setDaemon(True)
        process_thread.start()
    
    return ""

@app.route("/stop_process")
def stop_process():
    global process_thread
    global stop_process_flag
    stop_process_flag = True
    return ""


if __name__ == '__main__':
    app.run(debug= True)