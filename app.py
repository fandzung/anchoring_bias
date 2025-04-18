import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Anchoring Bias Game", layout="centered")

# Load data nếu đã có
def load_data():
    try:
        return pd.read_csv("responses.csv")
    except:
        return pd.DataFrame(columns=["timestamp", "name", "group", "estimated_price"])

# --- Bắt đầu giao diện ---

st.title("📊 Trải nghiệm Anchoring Bias trong phân tích cổ phiếu")

# Dùng session_state để lưu người dùng
if "submitted_info" not in st.session_state:
    st.session_state.submitted_info = False

# Chỉ hiển thị phần nhập nếu chưa submit
if not st.session_state.submitted_info:
    st.markdown("Hãy nhập thông tin cá nhân để bắt đầu:")

    name = st.text_input("🔹 Nhập họ tên hoặc mã sinh viên:", key="name_input")
    group = st.radio("🔸 Bạn thuộc nhóm nào ?", ["Nhóm A", "Nhóm B"], key="group_input")

if "trigger_submit" not in st.session_state:
    st.session_state.trigger_submit = False

def submit_info():
    if st.session_state.name_input.strip() == "" or st.session_state.group_input == "Chưa chọn":
        st.warning("⚠️ Vui lòng nhập đầy đủ thông tin và chọn nhóm trước khi tiếp tục.")
    else:
        st.session_state.name = st.session_state.name_input
        st.session_state.group = st.session_state.group_input
        st.session_state.submitted_info = True
        st.session_state.trigger_submit = True

st.button("🔓 Xác nhận thông tin", on_click=submit_info)

else:
    # Lấy lại thông tin từ session
    name = st.session_state.name
    group = st.session_state.group

    # --- Phần nội dung phân tích ---
    st.markdown(f"""
**Bản tin nội bộ: Đánh giá nhanh cổ phiếu ABC**

Trong bối cảnh kinh tế vĩ mô, tăng trưởng GDP quý gần nhất đạt 5.8% với lạm phát duy trì ở mức kiểm soát. Chính sách tiền tệ tiếp tục giữ ổn định với lãi suất điều hành không đổi, góp phần cải thiện thanh khoản hệ thống ngân hàng. Nhóm ngành bán lẻ đang cho thấy đà phục hồi rõ nét nhờ nhu cầu tiêu dùng nội địa tăng mạnh sau đại dịch.

Cổ phiếu ABC thuộc nhóm ngành bán lẻ, đã duy trì tốc độ tăng trưởng doanh thu bền vững trong 5 năm qua. Dự báo EPS năm tới đạt khoảng 5.000 VNĐ. Với PE trung bình ngành khoảng 12x, mức định giá tham chiếu có thể rơi vào khoảng 60.000 VNĐ.

Ghi nhận gần đây: {
    "Cổ phiếu ABC vừa giảm mạnh từ 45.000 xuống còn 40.000 VNĐ trong 1 tuần qua."
    if group == "Nhóm A" else
    "Cổ phiếu ABC từng đạt đỉnh 90.000 VNĐ và hiện đang giao dịch quanh mức 75.000 VNĐ."
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
