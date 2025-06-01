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

# Initialize session state for embeddings (cloud compatibility)
if 'face_embeddings' not in st.session_state:
    st.session_state['face_embeddings'] = []

# Initialize face embedding file if not exists (local compatibility)
if not os.path.exists('face_embedding.txt'):
    # Create empty file to ensure it exists
    with open('face_embedding.txt', 'w') as f:
        pass

#step 2: Collect facial embedding of the person
def video_callback_func(frame):
    img = frame.to_ndarray(format= 'bgr24') #3d array bgr
    reg_img, embedding = registration_form.get_embedding(img)
    
    if embedding is not None:
        # Method 1: Save to session_state (for Streamlit Cloud)
        st.session_state['face_embeddings'].append(embedding.copy())
        
        # Method 2: Save to file (for local development)
        try:
            with open('face_embedding.txt', mode='ab') as f:
                np.savetxt(f, embedding)
        except Exception as e:
            # File write might fail on cloud, but that's ok
            pass
    
    return av.VideoFrame.from_ndarray(reg_img, format= 'bgr24')

webrtc_streamer(key='registration', video_frame_callback=video_callback_func,
                rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})

# Display status from both sources
session_samples = len(st.session_state.get('face_embeddings', []))
file_samples = 0

try:
    if os.path.exists('face_embedding.txt') and os.path.getsize('face_embedding.txt') > 0:
        embeddings = np.loadtxt('face_embedding.txt')
        if embeddings.ndim == 1:
            file_samples = 1
        else:
            file_samples = embeddings.shape[0]
except:
    file_samples = 0

total_samples = max(session_samples, file_samples)

if total_samples > 0:
    st.success(f"✅ Face data captured successfully!")
    st.info(f"📊 Number of samples collected: {total_samples}")
    if session_samples > 0:
        st.info(f"💾 Session samples: {session_samples} (Cloud compatible)")
    if file_samples > 0:
        st.info(f"📁 File samples: {file_samples} (Local compatible)")
else:
    st.warning("⚠️ No face data captured yet. Please look at the camera to capture your face.")

#step 3: Save the data in redis database

if st.button('Submit'):
    return_val = registration_form.save_data_in_redis_db(person_name, role)
    if return_val == True:
        st.success(f"{person_name} registered successfully")
    elif return_val == 'name_false':
        st.error('Please enter the name: Name cannot be empty or spaces')
    elif return_val == 'file_false':
        st.error('No face data found. Please capture your face first by looking at the camera.')

# Reset button
if st.button('Reset Samples'):
    # Clear session state
    st.session_state['face_embeddings'] = []
    
    # Clear file
    if os.path.exists('face_embedding.txt'):
        os.remove('face_embedding.txt')
    
    # Reset form counter
    registration_form.reset()
    st.rerun()

