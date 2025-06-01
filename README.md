# 🎯 Face Recognition Attendance System

**Hệ thống chấm công nhận diện khuôn mặt sử dụng AI - Hỗ trợ đầy đủ trên Mobile & Desktop**

## ✨ Tính năng chính

- 🔍 **Nhận diện khuôn mặt real-time** với độ chính xác cao
- 📱 **Mobile-friendly** - Hoạt động mượt mà trên điện thoại
- 🖥️ **Cross-platform** - Windows, macOS, Linux  
- ☁️ **Cloud Database** - Redis Cloud storage
- 👥 **Quản lý người dùng** - Thêm, xóa, cập nhật
- 📊 **Báo cáo chi tiết** - Export CSV, thống kê
- 🔒 **Bảo mật cao** - Environment variables

## 🚀 Cài đặt nhanh

### 1. Clone repository
```bash
git clone https://github.com/jot2003/https-github.com-jot2003-DataScience-FaceRecognition-UC.git
cd DataScience-FaceRecognition-UC
```

### 2. Cài đặt dependencies  
```bash
pip install -r requirements.txt
```

### 3. Cấu hình Redis
```bash
# Copy file môi trường
cp .env.example .env

# Chỉnh sửa .env với thông tin Redis của bạn
REDIS_HOST=your-redis-host.com
REDIS_PORT=6379  
REDIS_PASSWORD=your-password
```

### 4. Chạy ứng dụng
```bash
streamlit run Home.py --server.port 8501
```

## ☁️ Deploy lên Streamlit Cloud (Recommended)

### Bước 1: Setup Repository
✅ Code đã được push lên: https://github.com/jot2003/https-github.com-jot2003-DataScience-FaceRecognition-UC

### Bước 2: Deploy trên Streamlit Cloud
1. Truy cập: https://share.streamlit.io/
2. Đăng nhập bằng GitHub account
3. Click **"New app"**
4. Chọn repository: `jot2003/https-github.com-jot2003-DataScience-FaceRecognition-UC`
5. Branch: `master`
6. Main file path: `Home.py`
7. Click **"Deploy!"**

### Bước 3: Cấu hình Secrets
Trong Streamlit Cloud dashboard:
1. Vào **App settings** → **Secrets**
2. Thêm Redis credentials:
```toml
[redis]
REDIS_HOST = "redis-10991.c244.us-east-1-2.ec2.redns.redis-cloud.com"
REDIS_PORT = 10991
REDIS_PASSWORD = "NNGuJHe6l5ZgOQcKGLnvx00LkRBZqq5W"
```
3. Click **"Save"**

### Bước 4: Kiểm tra deployment
- App sẽ tự động deploy trong 2-3 phút
- URL public: `https://your-app-name.streamlit.app`
- 📱 **Mobile accessible:** Works trực tiếp trên mobile browsers!

## 📱 Mobile Support

✅ **Hoàn toàn tương thích với mobile:**
- Responsive design tự động điều chỉnh
- Camera access qua WebRTC (cần HTTPS)
- Touch-friendly interface
- Optimized cho 3G/4G networks

## 🌐 Truy cập

- **Local:** http://localhost:8501
- **Network:** http://[your-ip]:8501  
- **Cloud:** https://your-app-name.streamlit.app
- **Mobile:** All URLs work on mobile!

## 📊 Các trang chức năng

1. **🏠 Home** - Dashboard tổng quan
2. **🎥 Real Time Predictions** - Nhận diện trực tiếp
3. **📝 Registration Form** - Đăng ký khuôn mặt mới
4. **👥 User Management** - Quản lý người dùng  
5. **📈 Report** - Báo cáo và thống kê

## 🔧 Troubleshooting

### Lỗi Redis Connection
```bash
# Kiểm tra .env file (local)
cat .env

# Kiểm tra secrets (cloud)
# Vào Streamlit Cloud dashboard → Secrets

# Test Redis connection
redis-cli -h your-host -p your-port -a your-password ping
```

### Lỗi Camera trên Mobile
- ✅ **Production:** HTTPS được Streamlit Cloud cung cấp tự động
- ✅ **Local:** Sử dụng `https://localhost` với SSL certificate
- Check browser permissions
- Thử các browser khác (Chrome, Safari, Firefox)

### Deployment Issues
```bash
# Check logs trong Streamlit Cloud dashboard
# Xem phần "Manage app" → "Logs"

# Common fixes:
# 1. Ensure secrets are properly configured
# 2. Check requirements.txt versions
# 3. Verify Redis credentials
```

## 🛡️ Security

- ✅ Environment variables cho local development
- ✅ Streamlit secrets cho cloud deployment
- ✅ .gitignore prevents credential leaks
- ✅ Redis password protection
- ✅ HTTPS trên production
- ✅ No hardcoded secrets

## 🚀 Deployment Options

### 🌟 Streamlit Cloud (Recommended)
- ✅ **Free hosting**
- ✅ **Auto HTTPS**
- ✅ **Mobile-ready**
- ✅ **Easy secrets management**
- ✅ **Auto deployment on git push**

### 🖥️ Local Network
```bash
streamlit run Home.py --server.address 0.0.0.0 --server.port 8501
```

### 🔧 Other Platforms
- **Heroku:** Add `setup.sh` and `Procfile`
- **Railway:** Works out of the box
- **Google Cloud Run:** Dockerize with included Dockerfile
- **AWS EC2:** Use `packages.txt` for dependencies

## 📱 Mobile Camera Testing

**Local Development:**
```bash
# Generate self-signed certificate for HTTPS
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes

# Run with HTTPS
streamlit run Home.py --server.sslCertFile cert.pem --server.sslKeyFile key.pem
```

**Production (Streamlit Cloud):**
- ✅ HTTPS được cung cấp tự động
- ✅ Camera access works immediately
- ✅ No additional configuration needed

## 📧 Liên hệ

- **Developer:** jot2003
- **GitHub:** https://github.com/jot2003
- **Live Demo:** https://your-app-name.streamlit.app

---

**⭐ Nếu project hữu ích, hãy star repo này!**

**🚀 Ready for instant cloud deployment!** 