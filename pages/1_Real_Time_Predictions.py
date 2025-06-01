import streamlit as st
from Home import face_reco
from streamlit_webrtc import webrtc_streamer
import av
import time

# Removed st.set_page_config to avoid conflict with main page
st.subheader('Real-time Attendance System')

# Retrieve the data from Redis Database
with st.spinner('Retrieving Data from Redis DB ...'):    
    redis_face_db = face_reco.retrieve_data(name='academy:register')
    st.dataframe(redis_face_db)
    
st.success("Data sucessfully retrieved from Redis")

# time 
waitTime = 10 # time in sec
setTime = time.time()
realtimepred = face_reco.RealTimePred() # real time prediction class

# Real Time Prediction
# streamlit webrtc
# callback function
def video_frame_callback(frame):
    global setTime
    
    img = frame.to_ndarray(format="bgr24") # 3 dimension numpy array
    # operation that you can perform on the array
    pred_img = realtimepred.face_prediction(img,redis_face_db,
                                        'facial_features',['Name','Role'],thresh=0.5)
    
    timenow = time.time()
    difftime = timenow - setTime
    if difftime >= waitTime:
        realtimepred.saveLogs_redis()
        setTime = time.time() # reset time        
        print('Save Data to redis database')
    

    return av.VideoFrame.from_ndarray(pred_img, format="bgr24")


webrtc_streamer(key="realtimePrediction", video_frame_callback=video_frame_callback)