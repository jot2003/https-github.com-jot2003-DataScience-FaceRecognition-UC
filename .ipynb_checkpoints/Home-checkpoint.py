import streamlit as st



st.set_page_config(page_title='Attendance System', layout='wide')

st.header('Attendance System using Face Recognition')

with st.spinner("Loading Models and Connectting to Redis DB ..."):
    import face_reco

st.success('Model loaded successfully')
st.success('Redis DB loaded successfully')