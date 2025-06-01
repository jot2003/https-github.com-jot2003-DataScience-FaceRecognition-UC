# 📱 Face Recognition Attendance System

Hệ thống điểm danh bằng nhận diện khuôn mặt sử dụng Streamlit và InsightFace.

## 🚀 Features

- ✅ **Real-time face recognition** với webcam
- ✅ **Registration system** để đăng ký khuôn mặt mới  
- ✅ **Attendance logging** với Redis database
- ✅ **Reports dashboard** xem báo cáo điểm danh
- ✅ **Mobile-friendly** responsive design

## 📋 Requirements

- Python 3.7+
- Webcam
- Internet connection (cho Redis Cloud)

## 🛠️ Installation

### 1. Clone repository
```bash
git clone <your-repo-url>
cd 4_attendance_app
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup environment variables
```bash
# Copy template
cp .env.example .env

# Edit .env with your Redis credentials
REDIS_HOST=your-redis-host.com
REDIS_PORT=6379
REDIS_PASSWORD=your-password
```

### 4. Download InsightFace model
Vì model files quá lớn (không thể push lên GitHub), bạn cần:

1. **Tự động download** khi chạy lần đầu (khuyến nghị)
2. **Hoặc download thủ công:**
   - Tạo folder `insightface_model/`
   - Download model `buffalo_sc` từ InsightFace
   - Giải nén vào folder `insightface_model/`

## 🎯 Usage

```bash
streamlit run Home.py
```

Truy cập: http://localhost:8501

## 📱 Mobile Access

Để sử dụng trên mobile:

1. **Local network:** Thay `localhost` bằng IP máy tính
2. **Internet access:** Deploy lên Streamlit Cloud (miễn phí)

## 🌐 Deploy to Streamlit Cloud

1. Push code lên GitHub
2. Vào https://share.streamlit.io/
3. Connect GitHub repo
4. Set secrets trong Settings:
   ```toml
   REDIS_HOST = "your-host"
   REDIS_PORT = "6379"
   REDIS_PASSWORD = "your-password"
   ```

## 🔧 File Structure

```
4_attendance_app/
├── Home.py              # Main Streamlit app
├── face_reco.py         # Face recognition logic
├── requirements.txt     # Dependencies
├── .env.example         # Environment template
├── .gitignore          # Git ignore rules
├── pages/              # Streamlit pages
│   ├── 1_Real_Time_Prediction.py
│   ├── 2_Registration_Form.py
│   └── 3_Reporting.py
└── insightface_model/  # (Download separately)
```

## 🛡️ Security

- ✅ Environment variables cho credentials
- ✅ .gitignore bảo vệ sensitive files
- ✅ .env template cho setup

## 📞 Support

Nếu gặp lỗi:
1. Kiểm tra Python version (3.7+)
2. Kiểm tra webcam permissions
3. Kiểm tra Redis connection
4. Kiểm tra model download

---
Made with ❤️ using Streamlit + InsightFace 