import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Xem kết quả phản hồi", layout="wide")

st.title("📊 Tổng hợp phản hồi từ sinh viên")

CSV_FILE = "responses.csv"

# Kiểm tra file tồn tại
if not os.path.exists(CSV_FILE):
    st.info("📭 Chưa có dữ liệu phản hồi nào được ghi nhận.")
    st.stop()

# Đọc dữ liệu
df = pd.read_csv(CSV_FILE)

# Hiển thị bảng dữ liệu
st.subheader("📋 Danh sách phản hồi")
st.dataframe(df, use_container_width=True)

# Hiển thị phản hồi mới nhất
st.markdown("### 🕒 Phản hồi gần nhất")
st.write(df.tail(1))

# Thống kê nhanh
st.subheader("📈 Thống kê theo nhóm")
grouped = df.groupby("group")["estimated_price"].agg(["count", "mean", "min", "max"])
st.table(grouped.style.format("{:.0f}"))

# Nút tải về
csv = df.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Tải kết quả (CSV)", csv, "responses.csv", "text/csv")
