import streamlit as st
import pandas as pd
import datetime

# Tạo/đọc file kết quả
def load_data():
    try:
        return pd.read_csv("responses.csv")
    except:
        return pd.DataFrame(columns=["timestamp", "name", "group", "estimated_price"])

# Giao diện người dùng
st.title("📊 Trải nghiệm Anchoring Bias trong đầu tư cổ phiếu")

st.markdown("""
Bạn là chuyên viên phân tích, hãy đọc thông tin và đưa ra mức giá hợp lý cho cổ phiếu ABC.

---  
**Thông tin tài chính giống nhau với mọi người:**

- EPS dự báo: 5.000 VNĐ  
- PE ngành: 12 → Giá hợp lý ước lượng: 60.000 VNĐ  
- Tăng trưởng ổn định, không có tin xấu  
---
""")

group = st.radio("Bạn thuộc nhóm nào?", ["Nhóm A", "Nhóm B"])

if group == "Nhóm A":
    st.warning("Cổ phiếu ABC vừa giảm từ 45.000 xuống 40.000 VNĐ trong 1 tuần qua.")
else:
    st.success("Cổ phiếu ABC đã từng đạt đỉnh 90.000 VNĐ, nay đang ở mức 75.000 VNĐ.")

name = st.text_input("Họ tên (hoặc mã sinh viên)")
estimated_price = st.number_input("Theo bạn, giá hợp lý hiện tại là bao nhiêu (VNĐ)?", min_value=0)

if st.button("✅ Gửi phản hồi"):
    if name == "":
        st.error("Bạn cần nhập họ tên.")
    else:
        df = load_data()
        new_data = pd.DataFrame([{
            "timestamp": datetime.datetime.now(),
            "name": name,
            "group": group,
            "estimated_price": estimated_price
        }])
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv("responses.csv", index=False)
        st.success("Gửi thành công!")

# Hiển thị kết quả nếu giảng viên muốn xem
st.markdown("## 📈 Tổng hợp (dành cho giảng viên)")
if st.checkbox("Hiện kết quả"):
    df = load_data()
    if df.empty:
        st.info("Chưa có phản hồi nào.")
    else:
        st.dataframe(df)
        st.bar_chart(df.groupby("group")["estimated_price"].mean())
