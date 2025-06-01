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

# Global variable for WebRTC callback compatibility
if 'global_embeddings' not in globals():
    global_embeddings = []

#Step 1: Collect person name and role
#form
person_name = st.text_input(label='Name',placeholder='First & Last Name')
role = st.selectbox(label='Select your role', options=('Student',
                                                        'Teacher'))

# ULTRA SMART CLOUD DETECTION: Check environment instead of file operations
# Streamlit Cloud can create files but they don't persist across requests

# Detect Streamlit Cloud environment
is_streamlit_cloud = (
    'STREAMLIT_SHARING_MODE' in os.environ or 
    'STREAMLIT_SERVER_HEADLESS' in os.environ or
    os.path.exists('/mount/src') or  # Streamlit Cloud file structure
    'streamlit.app' in os.environ.get('HOSTNAME', '')
)

if is_streamlit_cloud:
    # Force session_state mode on cloud
    st.session_state['use_file'] = False
    if 'embeddings_list' not in st.session_state:
        st.session_state['embeddings_list'] = []
    st.info("🌐 Detected Streamlit Cloud - Using session storage mode")
    # Clear global embeddings for fresh start
    global_embeddings = []
else:
    # Local environment - use file system
    try:
        if not os.path.exists('face_embedding.txt'):
            with open('face_embedding.txt', 'w') as f:
                pass
        # Test write permission
        with open('face_embedding.txt', 'a') as f:
            pass
        st.session_state['use_file'] = True
    except:
        # Fallback to session_state if file operations fail
        st.session_state['use_file'] = False
        if 'embeddings_list' not in st.session_state:
            st.session_state['embeddings_list'] = []

#step 2: Collect facial embedding of the person
def video_callback_func(frame):
    global global_embeddings
    img = frame.to_ndarray(format= 'bgr24') #3d array bgr
    reg_img, embedding = registration_form.get_embedding(img)
    
    if embedding is not None:
        # Always save to global for WebRTC compatibility
        global_embeddings.append(embedding)
        
        # Also try session_state if available
        try:
            if 'embeddings_list' not in st.session_state:
                st.session_state['embeddings_list'] = []
            st.session_state['embeddings_list'].append(embedding)
        except:
            pass  # WebRTC context might not have session_state access
        
        # Try file for local mode
        if st.session_state.get('use_file', True):
            try:
                with open('face_embedding.txt', mode='ab') as f:
                    np.savetxt(f, embedding)
            except:
                pass  # File operations might fail in cloud
    
    return av.VideoFrame.from_ndarray(reg_img, format= 'bgr24')

webrtc_streamer(key='registration', video_frame_callback=video_callback_func,
                rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})

# SMART STATUS: Display status for all sources
has_data = False
num_samples = 0

# Check global embeddings first (most reliable)
if len(global_embeddings) > 0:
    has_data = True
    num_samples = len(global_embeddings)
elif st.session_state.get('use_file', True):
    # Check file
    if os.path.exists('face_embedding.txt') and os.path.getsize('face_embedding.txt') > 0:
        has_data = True
        try:
            embeddings = np.loadtxt('face_embedding.txt')
            num_samples = 1 if embeddings.ndim == 1 else embeddings.shape[0]
        except:
            pass
else:
    # Check session_state
    if 'embeddings_list' in st.session_state and len(st.session_state['embeddings_list']) > 0:
        has_data = True
        num_samples = len(st.session_state['embeddings_list'])

if has_data:
    st.success("✅ Face data captured successfully!")
    st.info(f"📊 Number of samples collected: {num_samples}")
    if not st.session_state.get('use_file', True):
        st.info("🌐 Using cloud-compatible mode (session storage)")
        # Debug info for troubleshooting
        st.info(f"🔍 Debug: Global embeddings: {len(global_embeddings)}")
        if 'embeddings_list' in st.session_state:
            st.info(f"🔍 Debug: Session has {len(st.session_state['embeddings_list'])} embeddings")
    else:
        st.info("💾 Using local file mode")
else:
    st.warning("⚠️ No face data captured yet. Please look at the camera to capture your face.")
    # Debug info
    mode = "Cloud session mode" if not st.session_state.get('use_file', True) else "Local file mode"
    st.info(f"🔧 Mode: {mode}")
    st.info(f"🔍 Debug: Global embeddings: {len(global_embeddings)}")

#step 3: Save the data in redis database
if st.button('Submit'):
    return_val = registration_form.save_data_in_redis_db(person_name, role)
    if return_val == True:
        st.success(f"{person_name} registered successfully")
        # Clear all data after successful submission
        global_embeddings = []
        if 'embeddings_list' in st.session_state:
            st.session_state['embeddings_list'] = []
    elif return_val == 'name_false':
        st.error('Please enter the name: Name cannot be empty or spaces')
    elif return_val == 'file_false':
        st.error('face_embedding.txt is not found. Please refresh the page and execute again.')

# Reset button
if st.button('Reset Samples'):
    global_embeddings = []
    if st.session_state.get('use_file', True) and os.path.exists('face_embedding.txt'):
        os.remove('face_embedding.txt')
    if 'embeddings_list' in st.session_state:
        st.session_state['embeddings_list'] = []
    registration_form.reset()
    st.rerun()

