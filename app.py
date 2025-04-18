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
    st.success("📈 Cổ phiếu ABC từng đạt đỉnh 90.000 VNĐ, nay đang giao dịch ở mức 75.000 VNĐ.")

# 4. Nhập thông tin phản hồi
st.divider()
st.markdown("### 📝 Mức giá bạn cho là hợp lý")
name = st.text_input("Họ tên hoặc mã sinh viên")
estimated_price = st.number_input("Bạn định giá cổ phiếu ABC là bao nhiêu (VNĐ)?", min_value=0)

if st.button("✅ Gửi phản hồi"):
    if name.strip() == "":
        st.error("❌ Bạn cần nhập họ tên trước khi gửi.")
    else:
        df = load_data()
        new_entry = pd.DataFrame([{
            "timestamp": datetime.datetime.now(),
            "name": name,
            "group": group,
            "estimated_price": estimated_price
        }])
        df = pd.concat([df, new_entry], ignore_index=True)
        df.to_csv("responses.csv", index=False)
        st.success("✅ Đã gửi thành công! Cảm ơn bạn.")

# ❌ Không hiển thị tùy chọn tổng hợp kết quả nữa (ẩn hoàn toàn khỏi sinh viên)
# Nếu bạn cần giao diện thống kê cho giảng viên, mình có thể tạo app riêng (app_giangvien.py)
