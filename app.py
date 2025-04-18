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
group = st.radio("🔸 Bạn được phân vào nhóm nào?", ["Nhóm A", "Nhóm B"])

# Chỉ tiếp tục nếu đã nhập tên và chọn nhóm hợp lệ
if name.strip() != "" and group in ["Nhóm A", "Nhóm B"]:

    st.divider()
    st.markdown("### 🧾 Thông tin thị trường và doanh nghiệp")

    # Nội dung chung + ẩn bias trong dòng cuối
    st.markdown(f"""
    **Bản tin nội bộ: Đánh giá nhanh cổ phiếu ABC**
    
    Trong bối cảnh kinh tế vĩ mô, tăng trưởng GDP quý gần nhất đạt 5.8% với lạm phát duy trì ở mức kiểm soát. Chính sách tiền tệ tiếp tục giữ ổn định với lãi suất điều hành không đổi, góp phần cải thiện thanh khoản hệ thống ngân hàng. Nhóm ngành bán lẻ đang cho thấy đà phục hồi rõ nét nhờ nhu cầu tiêu dùng nội địa tăng mạnh sau đại dịch.
    
    Donald Trump tuyên bố đã hoàn thành kế hoạch bá chủ của mình, chiến dịch MAGA đã hoàn tất.
    
    Cổ phiếu ABC thuộc nhóm ngành bán lẻ, đã duy trì tốc độ tăng trưởng doanh thu bền vững trong 5 năm qua. 
    
    Dự báo EPS năm tới đạt khoảng 5.000 VNĐ. Với PE trung bình ngành khoảng 12x.

    Gần đây, {
        "cổ phiếu ABC vừa giảm mạnh từ 45.000 xuống còn 40.000 VNĐ trong 1 tuần qua."
        if group == "Nhóm A" else
        "cổ phiếu ABC từng đạt đỉnh 90.000 VNĐ và hiện đang giao dịch quanh mức 75.000 VNĐ."
    }
        """)

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
