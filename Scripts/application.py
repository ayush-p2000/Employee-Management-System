import streamlit as st
import cv2
from keras.models import load_model
import numpy as np
import time



st.set_page_config(page_title="Drowsiness Detection System",page_icon="https://cdn-icons-png.flaticon.com/512/5985/5985970.png")
st.title("DROWSINESS DETECTION SYSTEM")
st.sidebar.image("title_icon.png")
choice=st.sidebar.selectbox("My Menu",("HOME","URL","CAMERA"))



if(choice=="HOME"):
    st.image("main_image.jpeg")
    st.markdown("<h1>WELCOME TO DROWSINESS DETECTION APPLICATION<h1>",unsafe_allow_html=True)
    st.write("This is a Computer Vision Application which can detect whether a person is drowsy or not. This Application access data from Web Camera,IP Camera. It can be used to alert the drivers to avoid accidents.")



elif(choice=="URL"):
    url=st.text_input("Enter Video URL Here")
    btn=st.button("Start Detection")
    window=st.empty()
    if btn:
        facemodel=cv2.CascadeClassifier("face.xml")
        eyemodel=cv2.CascadeClassifier("eye.xml")
        detectionmodel=load_model("mymodel.h5",compile=False)
        vid=cv2.VideoCapture(cam)
        i=1
        btn2=st.button("Stop Detection")
        if btn2:
            vid.release()
            st.experimental_rerun()
            
        while(vid.isOpened()):
            flag,frame=vid.read()            
            if(flag):
                gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
                faces=facemodel.detectMultiScale(gray,1.3,5)
                for(x,y,w,l) in faces:
                    cv2.rectangle(frame,(x,y),(x+w,y+l),(255,0,0),2)
                    face_img=frame[y:y+w,x:x+l]
                    face_img = cv2.resize(face_img, (224, 224), interpolation=cv2.INTER_AREA) 
                    face_img = np.asarray(face_img, dtype=np.float32).reshape(1, 224, 224, 3)
                    face_img = (face_img / 127.5) - 1

                    roi_gray = gray[y:y+l, x:x+w]
                    roi_color = frame[y:y+l, x:x+w]
        
                    eyes = eyemodel.detectMultiScale(roi_gray)
                    for (ex,ey,ew,el) in eyes:
                            eye_img=frame[ey:ey+ew,ex:ex+el]
                            eye_img = cv2.resize(eye_img, (224, 224), interpolation=cv2.INTER_AREA) 
                            eye_img = np.asarray(eye_img, dtype=np.float32).reshape(1, 224, 224, 3)
                            eye_img = (eye_img / 127.5) - 1
                            pred=detectionmodel.predict(eye_img)[0][0]   
                    if pred>0.8:
                        for (ex,ey,ew,el) in eyes:
                            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+el),(0,255,0),2)
                    else:
                        cv2.rectangle(frame,(x,y),(x+w,y+l),(0,0,255),2)
                window.image(frame,channels="BGR")



                
elif(choice=="CAMERA"):
    cam=st.selectbox("Select 0 for Primary Camera and 1 for Secondary Camera",("None",0,1))
    btn=st.button("Start Detection")
    window=st.empty()
    if btn:
        facemodel=cv2.CascadeClassifier("face.xml")
        eyemodel=cv2.CascadeClassifier("eye.xml")
        detectionmodel=load_model("mymodel.h5",compile=False)
        vid=cv2.VideoCapture(cam)
        i=1
        btn2=st.button("Stop Detection")
        if btn2:
            vid.release()
            st.experimental_rerun()
            
        while(vid.isOpened()):
            flag,frame=vid.read()            
            if(flag):
                gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
                faces=facemodel.detectMultiScale(gray,1.3,5)
                for(x,y,w,l) in faces:
                    cv2.rectangle(frame,(x,y),(x+w,y+l),(255,0,0),2)
                    face_img=frame[y:y+w,x:x+l]
                    face_img = cv2.resize(face_img, (224, 224), e)
                    face_img = np.asarray(face_img, dtype=np.float32).reshape(1, 224, 224, 3)
                    face_img = (face_img / 127.5) - 1

                    roi_gray = gray[y:y+l, x:x+w]
                    roi_color = frame[y:y+l, x:x+w]
        
                    eyes = eyemodel.detectMultiScale(roi_gray)
                    for (ex,ey,ew,el) in eyes:
                            eye_img=frame[ey:ey+ew,ex:ex+el]
                            eye_img = cv2.resize(eye_img, (224, 224), interpolation=cv2.INTER_AREA) 
                            eye_img = np.asarray(eye_img, dtype=np.float32).reshape(1, 224, 224, 3)
                            eye_img = (eye_img / 127.5) - 1
                            pred=detectionmodel.predict(eye_img)[0][0]   
                    if pred>0.8:
                        for (ex,ey,ew,el) in eyes:
                            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+el),(0,255,0),2)
                    else:
                        cv2.rectangle(frame,(x,y),(x+w,y+l),(0,0,255),2)
                window.image(frame,channels="BGR")
