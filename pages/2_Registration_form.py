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

# Detect if we're on Streamlit Cloud (file system restrictions)
def is_streamlit_cloud():
    try:
        # Try to create a test file
        with open('test_write_permission.tmp', 'w') as f:
            f.write('test')
        os.remove('test_write_permission.tmp')
        return False  # Local environment - file system works
    except:
        return True   # Streamlit Cloud - file system restricted

USE_SESSION_STATE = is_streamlit_cloud()

# Initialize session state for face embeddings (both local and cloud for consistency)
if 'face_embeddings' not in st.session_state:
    st.session_state.face_embeddings = []

if USE_SESSION_STATE:
    st.info("🌐 Running on Streamlit Cloud - using memory-based storage")
else:
    st.info("🏠 Running locally - using hybrid storage (file + session backup)")
    # Initialize face embedding file if not exists
    if not os.path.exists('face_embedding.txt'):
        # Create empty file to ensure it exists
        with open('face_embedding.txt', 'w') as f:
            pass

#step 2: Collect facial embedding of the person
def video_callback_func(frame):
    img = frame.to_ndarray(format= 'bgr24') #3d array bgr
    reg_img, embedding = registration_form.get_embedding(img)
    
    # Save embeddings in session state (works for both local and cloud)
    if embedding is not None:
        # Always save to session state for reliability
        st.session_state.face_embeddings.append(embedding)
        
        # Also save to file if local environment (backup method)
        if not USE_SESSION_STATE:
            try:
                with open('face_embedding.txt', mode='ab') as f:
                    np.savetxt(f, embedding)
            except:
                pass  # File method failed, but session state is main method now
    
    return av.VideoFrame.from_ndarray(reg_img, format= 'bgr24')

webrtc_streamer(key='registration', video_frame_callback=video_callback_func,
                rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})

# Display status - Always check session state first
num_samples = len(st.session_state.face_embeddings) if 'face_embeddings' in st.session_state else 0

if num_samples > 0:
    st.success("✅ Face data captured successfully!")
    st.info(f"📊 Number of samples collected: {num_samples}")
    
    # Debug info for cloud
    if USE_SESSION_STATE:
        st.info(f"🔍 Session state embeddings shape: {np.array(st.session_state.face_embeddings).shape}")
else:
    st.warning("⚠️ No face data captured yet. Please look at the camera to capture your face.")
    
    # Additional check for local file as backup
    if not USE_SESSION_STATE and os.path.exists('face_embedding.txt') and os.path.getsize('face_embedding.txt') > 0:
        st.info("📁 File-based data detected as backup")

# Debug information
with st.expander("🔍 Debug Information"):
    st.write(f"Environment: {'Streamlit Cloud' if USE_SESSION_STATE else 'Local'}")
    st.write(f"Session state exists: {'face_embeddings' in st.session_state}")
    st.write(f"Session state length: {len(st.session_state.face_embeddings) if 'face_embeddings' in st.session_state else 0}")
    if not USE_SESSION_STATE:
        st.write(f"File exists: {os.path.exists('face_embedding.txt')}")
        st.write(f"File size: {os.path.getsize('face_embedding.txt') if os.path.exists('face_embedding.txt') else 0}")

#step 3: Save the data in redis database

if st.button('Submit'):
    return_val = registration_form.save_data_in_redis_db(person_name, role)
    if return_val == True:
        st.success(f"{person_name} registered successfully")
    elif return_val == 'name_false':
        st.error('Please enter the name: Name cannot be empty or spaces')
    elif return_val == 'file_false':
        st.error('No face data found. Please refresh the page and capture your face again.')

# Reset button
if st.button('Reset Samples'):
    # Clear session state
    st.session_state.face_embeddings = []
    
    # Clear file if local
    if not USE_SESSION_STATE and os.path.exists('face_embedding.txt'):
        os.remove('face_embedding.txt')
    
    registration_form.reset()
    st.rerun()

