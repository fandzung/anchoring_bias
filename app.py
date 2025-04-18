import streamlit as st
import pandas as pd
import datetime

# Load dữ liệu nếu có
def load_data():
    try:
        return pd.read_csv("responses.csv")
    except:
        return pd.DataFrame(columns=["timestamp", "name", "group", "estimated_price"])

st.set_page_config(page_title="Anchoring Bias Game", layout="centered")

# Header
st.title("📊 Trải nghiệm AB trong phân tích cổ phiếu")
st.markdown("Hãy nhập thông tin cá nhân và lựa chọn của bạn để bắt đầu:")

# Bước 1: Nhập thông tin cá nhân
name = st.text_input("🔹 Nhập họ tên hoặc mã sinh viên:")

# Bước 2: Chọn nhóm
group = st.radio("🔸 Bạn thuộc nhóm nào (do giảng viên phân)?", ["Chưa chọn", "Nhóm A", "Nhóm B"])

# Chỉ tiếp tục nếu đã nhập tên và chọn nhóm hợp lệ
if name.strip() != "" and group in ["Nhóm A", "Nhóm B"]:

    st.divider()
    st.markdown("### 🧾 Thông tin thị trường và doanh nghiệp")

    # Nội dung chung + ẩn bias trong dòng cuối
    info = """
    Bạn được giao phân tích cổ phiếu ABC trong bối cảnh thị trường hiện tại:

    - Tăng trưởng GDP quý gần nhất đạt 5.8%, lạm phát ở mức kiểm soát.
    - Lãi suất điều hành giữ ổn định, thanh khoản thị trường cải thiện.
    - Nhóm ngành bán lẻ đang được hưởng lợi từ tiêu dùng nội địa phục hồi mạnh.
    - Donald Trump đã hoàn tất thương chiến và đã tuyên bố MAGA thắng lợi!

    Cổ phiếu ABC là doanh nghiệp bán lẻ có:
    - Tăng trưởng doanh thu ổn định trong 5 năm gần nhất.
    - EPS dự báo năm tới: **5.000 VNĐ**
    - PE trung bình ngành: **12x** 

    """

    # Chèn bias theo nhóm
    if group == "Nhóm A":
        info += "\nGhi nhận gần nhất: Cổ phiếu ABC vừa giảm mạnh từ 45.000 xuống còn **40.000 VNĐ** trong 1 tuần qua."
    elif group == "Nhóm B":
        info += "\nGhi nhận gần nhất: Cổ phiếu ABC từng đạt đỉnh **90.000 VNĐ**, hiện giao dịch quanh **75.000 VNĐ**."

    # Hiển thị thông tin đầy đủ
    st.markdown(info)

    st.divider()
    st.markdown("### 💵 Theo bạn, mức giá hợp lý hiện tại của cổ phiếu ABC là bao nhiêu?")

    estimated_price = st.number_input("💬 Nhập giá bạn định giá (VNĐ):", min_value=0)

    if st.button("✅ Gửi phản hồi"):
        df = load_data()
        new_row = pd.DataFrame([{
            "timestamp": datetime.datetime.now(),
            "name": name,
            "group": group,
            "estimated_price": estimated_price
        }])
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv("responses.csv", index=False)
        st.success("✅ Gửi thành công! Cảm ơn bạn đã tham gia.")
else:
    st.info("📝 Vui lòng nhập đầy đủ thông tin trước khi xem thông tin phục vụ phân tích.")
