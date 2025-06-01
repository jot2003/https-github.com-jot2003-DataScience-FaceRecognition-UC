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

## 📱 Mobile Support

✅ **Hoàn toàn tương thích với mobile:**
- Responsive design tự động điều chỉnh
- Camera access qua WebRTC
- Touch-friendly interface
- Optimized cho 3G/4G networks

## 🌐 Truy cập

- **Local:** http://localhost:8501
- **Network:** http://[your-ip]:8501  
- **Mobile:** Truy cập qua network URL

## 📊 Các trang chức năng

1. **🏠 Home** - Dashboard tổng quan
2. **🎥 Real Time Predictions** - Nhận diện trực tiếp
3. **📝 Registration Form** - Đăng ký khuôn mặt mới
4. **👥 User Management** - Quản lý người dùng  
5. **📈 Report** - Báo cáo và thống kê

## 🔧 Troubleshooting

### Lỗi Redis Connection
```bash
# Kiểm tra .env file
cat .env

# Test Redis connection
redis-cli -h your-host -p your-port -a your-password ping
```

### Lỗi Camera trên Mobile
- Đảm bảo HTTPS connection cho production
- Check browser permissions
- Thử các browser khác (Chrome, Safari, Firefox)

## 🛡️ Security

- ✅ Environment variables cho credentials  
- ✅ .gitignore prevents credential leaks
- ✅ Redis password protection
- ✅ No hardcoded secrets

## 🚀 Deployment

### Streamlit Cloud
1. Push code lên GitHub
2. Kết nối Streamlit Cloud
3. Thêm secrets trong dashboard
4. Deploy!

### Local Network
```bash
streamlit run Home.py --server.address 0.0.0.0 --server.port 8501
```

## 📧 Liên hệ

- **Developer:** jot2003
- **GitHub:** https://github.com/jot2003

---

**⭐ Nếu project hữu ích, hãy star repo này!** 