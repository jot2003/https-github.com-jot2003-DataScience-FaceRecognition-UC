import streamlit as st
from Home import face_reco
import pandas as pd

st.subheader('👥 User Management - Quản lý người dùng')

# Lấy danh sách user hiện tại
users = face_reco.get_all_registered_users()

if users:
    st.write(f"**Tổng số user đã đăng ký: {len(users)}**")
    
    # Hiển thị bảng user
    df = pd.DataFrame(users)
    st.dataframe(df[['Name', 'Role']], use_container_width=True)
    
    st.write("---")
    
    # Xóa user cụ thể
    st.subheader("🗑️ Xóa user cụ thể")
    
    col1, col2 = st.columns(2)
    with col1:
        selected_user = st.selectbox(
            "Chọn user để xóa:",
            options=[f"{user['Name']} ({user['Role']})" for user in users],
            key="delete_select"
        )
    
    with col2:
        if st.button("❌ Xóa user đã chọn", type="secondary"):
            if selected_user:
                # Parse name và role
                name_role = selected_user.split(" (")
                name = name_role[0]
                role = name_role[1][:-1]  # Remove closing parenthesis
                
                if face_reco.delete_user_from_redis(name, role):
                    st.success(f"✅ Đã xóa user: {name} ({role})")
                    st.rerun()
                else:
                    st.error(f"❌ Không thể xóa user: {name} ({role})")
    
    st.write("---")
    
    # Xóa tất cả user
    st.subheader("🚨 Xóa tất cả user")
    st.warning("⚠️ Thao tác này sẽ xóa TẤT CẢ user đã đăng ký và KHÔNG THỂ HOÀN TÁC!")
    
    col1, col2 = st.columns(2)
    with col1:
        confirm_delete_all = st.checkbox("Tôi hiểu rủi ro và muốn xóa tất cả")
    
    with col2:
        if st.button("🗑️ XÓA TẤT CẢ USER", type="primary", disabled=not confirm_delete_all):
            if face_reco.delete_all_users_from_redis():
                st.success("✅ Đã xóa tất cả user!")
                st.rerun()
            else:
                st.error("❌ Không thể xóa user!")

else:
    st.info("📭 Chưa có user nào được đăng ký.")
    st.write("Hãy vào trang **Registration Form** để đăng ký user mới!")

# Refresh button
if st.button("🔄 Làm mới danh sách"):
    st.rerun() 