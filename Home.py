import streamlit as st

# Mobile-friendly configuration
st.set_page_config(
    page_title='📱 Face Recognition Attendance',
    page_icon='📱',
    layout='wide',
    initial_sidebar_state='expanded'
)

# CSS cho mobile responsive
st.markdown("""
<style>
    .main > div {
        max-width: 100%;
        padding: 1rem;
    }
    .stButton > button {
        width: 100%;
        height: 60px;
        font-size: 18px;
        margin: 10px 0;
    }
    .stSelectbox > div {
        font-size: 16px;
    }
    .stHeader {
        font-size: 24px !important;
        text-align: center;
    }
    /* Mobile viewport */
    @media (max-width: 768px) {
        .main > div {
            padding: 0.5rem;
        }
        .stButton > button {
            height: 50px;
            font-size: 16px;
        }
    }
</style>
""", unsafe_allow_html=True)

st.header('📱 Attendance System using Face Recognition')

with st.spinner("Loading Models and Connectting to Redis DB ..."):
    import face_reco

st.success('✅ Model loaded successfully')
st.success('✅ Redis DB loaded successfully')

# Mobile usage instructions
st.info("""
📱 **Sử dụng trên Mobile:**
- Xoay ngang điện thoại để có trải nghiệm tốt nhất
- Camera sẽ tự động bật khi vào trang Predictions
- Đảm bảo có ánh sáng đủ để nhận diện khuôn mặt
""")