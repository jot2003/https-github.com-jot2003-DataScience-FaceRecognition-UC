import streamlit as st

# Import face_reco at global scope so other modules can import it
import face_reco

st.set_page_config(page_title='Attendance System', layout='wide')

st.header('Attendance System using Face Recognition')

with st.spinner("Loading Models and Connectting to Redis DB ..."):
    # face_reco is already imported above
    pass

st.success('Model loaded successfully')
st.success('Redis DB loaded successfully')