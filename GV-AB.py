import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Xem kết quả phản hồi", layout="centered")

st.title("📋 Tổng hợp phản hồi từ sinh viên")

# Nhập mật khẩu đơn giản để hạn chế truy cập
password = st.text_input("🔑 Nhập mã truy cập:", type="password")

if password != "ftu123":
    st.warning("Vui lòng nhập mã truy cập hợp lệ để xem dữ liệu.")
    st.stop()

# Đọc file responses.csv
if not os.path.exists("responses.csv"):
    st.info("📭 Chưa có dữ liệu phản hồi nào được ghi nhận.")
    st.stop()

# Load dữ liệu
try:
    df = pd.read_csv("responses.csv")
except Exception as e:
    st.error("Lỗi khi đọc dữ liệu: " + str(e))
    st.stop()

# Hiển thị bảng dữ liệu
st.subheader("📄 Danh sách phản hồi")
st.dataframe(df, use_container_width=True)

# Thống kê nhanh
st.subheader("📊 Thống kê theo nhóm")
grouped = df.groupby("group")["estimated_price"].agg(["count", "mean", "min", "max"])
st.table(grouped.style.format("{:.0f}"))

# Tải file CSV
csv = df.to_csv(index=False).encode('utf-8')
st.download_button("⬇️ Tải toàn bộ kết quả (.csv)", csv, "responses.csv", "text/csv")
