import streamlit as st
import time
import os

st.subheader('📊 Real-time Attendance System')

# Lazy load face_reco module
@st.cache_resource
def load_face_reco():
    """Load face recognition module with caching"""
    try:
        import face_reco
        return face_reco
    except Exception as e:
        st.error(f"❌ Error loading face recognition: {e}")
        return None

# Initialize face_reco with loading indicator
with st.spinner('🔄 Loading face recognition models...'):
    face_reco = load_face_reco()

if face_reco is None:
    st.error("❌ Face recognition not available. Please refresh the page.")
    st.stop()

# Retrieve the data from Redis Database
with st.spinner('📡 Retrieving Data from Redis DB ...'):    
    try:
        redis_face_db = face_reco.retrieve_data(name='academy:register')
        if not redis_face_db.empty:
            st.dataframe(redis_face_db)
            st.success("✅ Data successfully retrieved from Redis")
        else:
            st.warning("⚠️ No registered faces found. Please register faces first.")
            redis_face_db = None
    except Exception as e:
        st.error(f"❌ Redis connection error: {e}")
        st.stop()

# Only proceed if we have data or want to test
if redis_face_db is not None or st.checkbox("🧪 Test mode (no registered faces)"):
    # Import webrtc components only when needed
    try:
        from streamlit_webrtc import webrtc_streamer
        import av
        
        # time 
        waitTime = 10 # time in sec
        setTime = time.time()
        realtimepred = face_reco.RealTimePred() # real time prediction class

        st.info("📱 **Mobile tip:** This works best on desktop. For mobile, use the Registration page first.")

        # Real Time Prediction
        # streamlit webrtc
        # callback function
        def video_frame_callback(frame):
            global setTime
            
            img = frame.to_ndarray(format="bgr24") # 3 dimension numpy array
            # operation that you can perform on the array
            if redis_face_db is not None:
                pred_img = realtimepred.face_prediction(img,redis_face_db,
                                                    'facial_features',['Name','Role'],thresh=0.5)
            else:
                # Test mode - just return original image
                pred_img = img
            
            timenow = time.time()
            difftime = timenow - setTime
            if difftime >= waitTime:
                realtimepred.saveLogs_redis()
                setTime = time.time() # reset time        
                print('Save Data to redis database')
            
            return av.VideoFrame.from_ndarray(pred_img, format="bgr24")

        webrtc_streamer(
            key="realtimePrediction", 
            video_frame_callback=video_frame_callback,
            media_stream_constraints={"video": True, "audio": False}
        )
        
    except ImportError as e:
        st.error(f"❌ WebRTC not available: {e}")
        st.info("📱 This feature requires webcam access and works best on desktop browsers.")
else:
    st.info("👆 Please register some faces first or enable test mode to use real-time prediction.")