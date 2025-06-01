import streamlit as st
from Home import face_reco
import cv2
import numpy as np
from streamlit_webrtc import webrtc_streamer
import av

# st.set_page_config(page_title='Registration Form')
st.subheader('Registration Form')

##init registration form
registration_form = face_reco.RegistrationForm()

# Initialize session state for face embeddings
if 'face_embedding' not in st.session_state:
    st.session_state['face_embedding'] = None

#Step 1: Collect person name and role
#form
person_name = st.text_input(label='Name',placeholder='First & Last Name')
role = st.selectbox(label='Select your role', options=('Student',
                                                        'Teacher'))


#step 2: Collect facial embedding of the person
def video_callback_func(frame):
    img = frame.to_ndarray(format= 'bgr24') #3d array bgr
    reg_img, embedding = registration_form.get_embedding(img)
    
    # Save embedding to session state instead of file
    if embedding is not None:
        st.session_state['face_embedding'] = embedding
        
    return av.VideoFrame.from_ndarray(reg_img, format= 'bgr24')

webrtc_streamer(key='registration', video_frame_callback=video_callback_func)

# Show status
if st.session_state['face_embedding'] is not None:
    st.success(f"✅ Face detected! Samples collected: {registration_form.sample}")
else:
    st.info("📸 Please look at the camera to capture your face")

#step 3: Save the data in redis database
if st.button('Submit'):
    return_val = registration_form.save_data_in_redis_db(person_name, role)
    if return_val == True:
        st.success(f"🎉 {person_name} registered successfully!")
        # Reset for next registration
        st.session_state['face_embedding'] = None
        registration_form.reset()
    elif return_val == 'name_false':
        st.error('❌ Please enter the name: Name cannot be empty or spaces')
    elif return_val == 'file_false':
        st.error('❌ No face data captured. Please look at the camera and try again.')

