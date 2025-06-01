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

# Initialize face embedding file if not exists
if not os.path.exists('face_embedding.txt'):
    # Create empty file to ensure it exists
    with open('face_embedding.txt', 'w') as f:
        pass

#step 2: Collect facial embedding of the person
def video_callback_func(frame):
    img = frame.to_ndarray(format= 'bgr24') #3d array bgr
    reg_img, embedding = registration_form.get_embedding(img)
    #two step process
    #1st step save data into local computer txt
    if embedding is not None:
        with open('face_embedding.txt', mode='ab') as f:
            np.savetxt(f, embedding)
    return av.VideoFrame.from_ndarray(reg_img, format= 'bgr24')

webrtc_streamer(key='registration', video_frame_callback=video_callback_func,
                rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})

# Display file status
if os.path.exists('face_embedding.txt') and os.path.getsize('face_embedding.txt') > 0:
    st.success("✅ Face data captured successfully!")
    
    # Show number of samples
    try:
        embeddings = np.loadtxt('face_embedding.txt')
        if embeddings.ndim == 1:
            num_samples = 1
        else:
            num_samples = embeddings.shape[0]
        st.info(f"📊 Number of samples collected: {num_samples}")
    except:
        st.warning("⚠️ Face embedding file exists but may be empty. Continue capturing faces.")
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
        st.error('face_embedding.txt is not found. Please refresh the page and execute again.')

# Reset button
if st.button('Reset Samples'):
    if os.path.exists('face_embedding.txt'):
        os.remove('face_embedding.txt')
    registration_form.reset()
    st.rerun()

