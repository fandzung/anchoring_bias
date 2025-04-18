import streamlit as st
import pandas as pd
import datetime

# Đọc dữ liệu nếu có
def load_data():
    try:
        return pd.read_csv("responses.csv")
    except:
        return pd.DataFrame(columns=["timestamp", "name", "group", "estimated_price"])

# Giao diện
st.title("📊 Trải nghiệm Anchoring Bias trong đầu tư cổ phiếu")

# 1. Chọn nhóm trước
group = st.radio("🔰 Bạn thuộc nhóm nào?", ["Nhóm A", "Nhóm B"])

# 2. Hiện toàn bộ thông tin sau khi chọn nhóm
st.markdown("### 🧾 Thông tin thị trường cổ phiếu ABC")

with st.expander("📂 Bối cảnh thị trường"):
    st.markdown("""
    - Công ty có nền tảng tài chính ổn định.
    - EPS dự báo năm tới: **5.000 VNĐ**
    - Tỷ lệ tăng trưởng duy trì ổn định, không có rủi ro lớn.
    - PE ngành: **12x** → Giá hợp lý ước tính: **60.000 VNĐ**
    """)

# 3. Giá neo (đưa ra sau cùng)
if group == "Nhóm A":
    st.warning("📉 Cổ phiếu ABC vừa giảm từ 45.000 xuống còn 40.000 VNĐ trong tuần qua.")
else:
    st.success("📈 Cổ phiếu ABC từng đạt đỉnh 90
