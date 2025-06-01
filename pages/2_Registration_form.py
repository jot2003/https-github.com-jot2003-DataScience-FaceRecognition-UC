import streamlit as st
from Home import face_reco
import cv2
import numpy as np
from streamlit_webrtc import webrtc_streamer
import av
import os

# st.set_page_config(page_title='Registration Form')
st.subheader('Registration Form')

##init registration form
registration_form = face_reco.RegistrationForm()

#Step 1: Collect person name and role
#form
person_name = st.text_input(label='Name',placeholder='First & Last Name')
role = st.selectbox(label='Select your role', options=('Student',
                                                        'Teacher'))

# Detect Streamlit Cloud environment
is_streamlit_cloud = (
    'STREAMLIT_SHARING_MODE' in os.environ or 
    'STREAMLIT_SERVER_HEADLESS' in os.environ or
    os.path.exists('/mount/src') or  # Streamlit Cloud file structure
    'streamlit.app' in os.environ.get('HOSTNAME', '')
)

if is_streamlit_cloud:
    st.info("🌐 Cloud Mode: Face recognition is simulated for demo purposes")
    st.warning("⚠️ In production, you would use actual face capture here")
else:
    st.info("💾 Local Mode: Using real face recognition")
    # Initialize face embedding file for local mode
    if not os.path.exists('face_embedding.txt'):
        with open('face_embedding.txt', 'w') as f:
            pass

#step 2: Collect facial embedding of the person
def video_callback_func(frame):
    img = frame.to_ndarray(format= 'bgr24') #3d array bgr
    reg_img, embedding = registration_form.get_embedding(img)
    
    # Only save to file in local mode
    if embedding is not None and not is_streamlit_cloud:
        try:
            with open('face_embedding.txt', mode='ab') as f:
                np.savetxt(f, embedding)
        except:
            pass  # File operations might fail, but that's ok
    
    return av.VideoFrame.from_ndarray(reg_img, format= 'bgr24')

webrtc_streamer(key='registration', video_frame_callback=video_callback_func,
                rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})

# Status display
if is_streamlit_cloud:
    st.success("✅ Ready to register (Cloud Demo Mode)")
else:
    # Check file for local mode only
    if os.path.exists('face_embedding.txt') and os.path.getsize('face_embedding.txt') > 0:
        st.success("✅ Face data captured successfully!")
        try:
            embeddings = np.loadtxt('face_embedding.txt')
            num_samples = 1 if embeddings.ndim == 1 else embeddings.shape[0]
            st.info(f"📊 Number of samples collected: {num_samples}")
        except:
            pass
    else:
        st.warning("⚠️ No face data captured yet. Please look at the camera to capture your face.")

#step 3: Save the data in redis database
if st.button('Submit'):
    return_val = registration_form.save_data_in_redis_db(person_name, role)
    if return_val == True:
        st.success(f"{person_name} registered successfully")
        # Clean up for local mode
        if not is_streamlit_cloud and os.path.exists('face_embedding.txt'):
            try:
                os.remove('face_embedding.txt')
            except:
                pass
    elif return_val == 'name_false':
        st.error('Please enter the name: Name cannot be empty or spaces')
    elif return_val == 'file_false':
        st.error('face_embedding.txt is not found. Please refresh the page and execute again.')

# Reset button (local mode only)
if not is_streamlit_cloud and st.button('Reset Samples'):
    if os.path.exists('face_embedding.txt'):
        try:
            os.remove('face_embedding.txt')
        except:
            pass
    registration_form.reset()
    st.rerun()

