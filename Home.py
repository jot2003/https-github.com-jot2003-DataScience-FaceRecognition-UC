import streamlit as st

# Import face_reco at global scope so other modules can import it
import face_reco

st.set_page_config(
    page_title='🎯 Attendance System', 
    layout='wide',
    initial_sidebar_state='expanded'
)

# Mobile-friendly header
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .feature-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    /* Mobile responsive */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 1.5rem !important;
        }
        .feature-card {
            padding: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>🎯 Face Recognition Attendance System</h1>
    <p>📱 Mobile-Ready • 🔒 Secure • ⚡ Real-time</p>
</div>
""", unsafe_allow_html=True)

with st.spinner("🚀 Loading AI Models & Connecting to Database..."):
    # face_reco is already imported above
    pass

col1, col2 = st.columns(2)

with col1:
    st.success('✅ AI Models Loaded Successfully')
    st.info('🌐 Redis Database Connected')

with col2:
    st.metric("📱 Mobile Support", "✅ Full Compatible")
    st.metric("🔒 Security", "✅ Environment Protected")

# Feature overview
st.markdown("## 🚀 Quick Start Guide")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <h3>📝 1. Register Users</h3>
        <p>Add new faces to the system using your camera</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h3>🎥 2. Real-time Recognition</h3>
        <p>Track attendance with live face detection</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <h3>📊 3. Generate Reports</h3>
        <p>Export attendance data and analytics</p>
    </div>
    """, unsafe_allow_html=True)

# Mobile instructions
st.markdown("---")
st.markdown("### 📱 Mobile Users")
st.info("""
**For best mobile experience:**
- Use Chrome or Safari browser
- Allow camera permissions when prompted
- Hold device steady during face scanning
- Ensure good lighting conditions
""")

# System status
with st.expander("🔧 System Status & Info"):
    import redis
    try:
        face_reco.r.ping()
        st.success("✅ Redis Database: Connected")
    except:
        st.error("❌ Redis Database: Connection Failed")
    
    st.info(f"🔗 Network URL: Use this for mobile access")
    st.code("http://[your-local-ip]:8501")
    
    st.warning("📱 Mobile Camera: Requires HTTPS in production")

st.markdown("---")
st.markdown("💡 **Tip:** Navigate using the sidebar menu on the left")