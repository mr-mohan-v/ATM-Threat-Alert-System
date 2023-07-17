from keras_preprocessing.image import img_to_array
import cv2
from tflite_runtime.interpreter import Interpreter
import numpy as np
import time


def execfile(filepath, globals=None, locals=None):
    if globals is None:
        globals = {}
    globals.update({
        "__file__": filepath,
        "__name__": "__main__",
    })
    with open(filepath, 'rb') as file:
        exec(compile(file.read(), filepath, 'exec'), globals, locals)
        
        
emotion_label_position=(0,0)
face_classifier=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Load the TFLite model and allocate tensors.
emotion_interpreter = Interpreter(model_path="model.tflite")
emotion_interpreter.allocate_tensors()

# Get input and output tensors.
emotion_input_details = emotion_interpreter.get_input_details()
emotion_output_details = emotion_interpreter.get_output_details()

# Test the model on input data.
emotion_input_shape = emotion_input_details[0]['shape']

class_labels=['Angry','Disgust', 'Fear', 'Happy','Neutral','Sad','Surprise']

cap=cv2.VideoCapture(0)
emotion_label=""
while True:
    ret,frame=cap.read()
    labels=[]
    
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces=face_classifier.detectMultiScale(gray,1.3,5)
    start = time.time()

    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray=gray[y:y+h,x:x+w]
        roi_gray=cv2.resize(roi_gray,(64,64*3),interpolation=cv2.INTER_AREA)

        #Get image ready for prediction
        roi=roi_gray.astype('float')/255.0  #Scale
        roi=img_to_array(roi)
        roi = roi.reshape(1,64, 64,3)
     
        emotion_interpreter.set_tensor(emotion_input_details[0]['index'], roi)
        emotion_interpreter.invoke()
        emotion_preds = emotion_interpreter.get_tensor(emotion_output_details[0]['index'])

        emotion_label=class_labels[emotion_preds.argmax()]  #Find the label
        emotion_label_position=(x,y)
        print(emotion_label)        
        cv2.putText(frame,emotion_label,emotion_label_position,cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
        
    cv2.imshow('Emotion Detector', frame)  
    end=time.time()
    print("Total time=", end-start)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):  #Press q to exit
        break
    if emotion_label=='Fear' or emotion_label=='Sad':
        execfile('vlc.py')
        break
            
cap.release()
cv2.destroyAllWindows()
