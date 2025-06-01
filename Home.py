import streamlit as st
import os

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

st.header('📱 Face Recognition Attendance System')

# Check if running on Streamlit Cloud
if "STREAMLIT_SHARING" in os.environ or "STREAMLIT_CLOUD" in os.environ:
    st.info("🚀 **Running on Streamlit Cloud** - Models will be downloaded automatically on first use.")
    
    st.success('✅ App deployed successfully!')
    st.success('✅ Environment configured!')
    
    # Show app navigation without loading heavy models yet
    st.markdown("""
    ### 🎯 **How to use:**
    
    1. **📊 Real-time Predictions**: Go to sidebar → Real Time Prediction
    2. **👤 Registration**: Go to sidebar → Registration Form  
    3. **📈 Reports**: Go to sidebar → Reporting
    
    ⚡ **Models will load automatically when you use the features!**
    """)
    
    # Mobile usage instructions
    st.info("""
    📱 **Mobile Usage:**
    - Rotate phone to landscape for best experience
    - Camera will activate automatically in Predictions page
    - Ensure good lighting for face recognition
    """)

else:
    # Local development - load models immediately
    with st.spinner("Loading Models and Connecting to Redis DB ..."):
        try:
            import face_reco
            st.success('✅ Model loaded successfully')
            st.success('✅ Redis DB loaded successfully')
        except Exception as e:
            st.error(f"❌ Error loading models: {e}")
            st.info("Some features may not work. Please check your setup.")

    # Mobile usage instructions
    st.info("""
    📱 **Sử dụng trên Mobile:**
    - Xoay ngang điện thoại để có trải nghiệm tốt nhất
    - Camera sẽ tự động bật khi vào trang Predictions
    - Đảm bảo có ánh sáng đủ để nhận diện khuôn mặt
    """)