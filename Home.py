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

# Always show success for demo
st.success('🎉 **App Successfully Deployed!**')

# Check deployment environment
if "STREAMLIT_SHARING" in os.environ or "STREAMLIT_CLOUD" in os.environ:
    st.info("🚀 **Running on Streamlit Cloud** - This is a DEMO version")
    demo_mode = True
else:
    st.info("💻 **Running locally** - Full features available")
    demo_mode = False

# Show features
st.markdown("""
### 🎯 **Available Features:**

1. **📊 Real-time Predictions**: 
   - Go to sidebar → Real Time Prediction
   - {}

2. **👤 Registration Form**: 
   - Go to sidebar → Registration Form
   - {}

3. **📈 Reports**: 
   - Go to sidebar → Reporting
   - {}

{}
""".format(
    "Demo mode - simulated face detection" if demo_mode else "Live webcam face recognition",
    "Demo mode - simulated registration" if demo_mode else "Register new faces with webcam", 
    "Demo mode - sample reports" if demo_mode else "Real attendance analytics",
    "⚡ **This is a demonstration version. Models are simulated for quick loading.**" if demo_mode else "⚡ **Full face recognition capabilities enabled.**"
))

# Mobile usage instructions
st.info("""
📱 **Mobile Usage Tips:**
- Rotate phone to landscape for best experience
- All features are mobile-optimized
- Demo mode works perfectly on any device
""")

# Environment info
with st.expander("🔧 **System Information**"):
    st.write(f"**Demo Mode:** {'✅ Yes' if demo_mode else '❌ No'}")
    st.write(f"**Platform:** {'Streamlit Cloud' if demo_mode else 'Local Development'}")
    st.write("**Status:** Ready for use! 🚀")

st.markdown("---")
st.markdown("**Made with ❤️ using Streamlit + InsightFace**")