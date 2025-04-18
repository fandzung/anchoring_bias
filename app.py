import streamlit as st
import pandas as pd
import datetime
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="Anchoring Bias Game", layout="centered")

# Google Sheets setup
SHEET_NAME = "AB_Responses"
SCOPE = ["https://www.googleapis.com/auth/spreadsheets"]
CREDS = Credentials.from_service_account_file("credentials.json", scopes=SCOPE)
client = gspread.authorize(CREDS)
sheet = client.open(SHEET_NAME).sheet1

# ----------- Session State mặc định ------------
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "name" not in st.session_state:
    st.session_state.name = ""
if "group" not in st.session_state:
    st.session_state.group = ""

# ----------- Hàm lưu dữ liệu -------------
def save_to_google_sheets(name, group, estimated_price):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([timestamp, name, group, estimated_price])

# ----------- Giao diện ----------------

st.title("\U0001F4CA Trải nghiệm Anchoring Bias trong định giá cổ phiếu")

# BƯỚC 1: NHẬP THÔNG TIN
if not st.session_state.submitted:
    st.markdown("### \U0001F4DD Vui lòng nhập thông tin để bắt đầu:")

    name = st.text_input("\U0001F539 Họ tên hoặc mã sinh viên", key="name_input")
    group = st.radio("\U0001F538 Nhóm bạn được phân công", ["Chưa chọn", "Nhóm A", "Nhóm B"], key="group_input")

    def submit_info():
        if st.session_state.name_input.strip() == "" or st.session_state.group_input == "Chưa chọn":
            st.warning("⚠️ Vui lòng nhập đầy đủ thông tin.")
        else:
            st.session_state.name = st.session_state.name_input
            st.session_state.group = st.session_state.group_input
            st.session_state.submitted = True

    st.button("\U0001F513 Xác nhận thông tin", on_click=submit_info)

# BƯỚC 2: HIỂN THỊ THÔNG TIN PHÂN TÍCH + Ô NHẬP GIÁ
else:
    name = st.session_state.name
    group = st.session_state.group

    st.markdown(f"""
**Bản tin nội bộ – Đánh giá nhanh cổ phiếu ABC**

Trong bối cảnh kinh tế vĩ mô, tăng trưởng GDP quý gần nhất đạt 5.8% với lạm phát duy trì ở mức kiểm soát. Lãi suất điều hành được giữ ổn định, tạo điều kiện cho thanh khoản ngân hàng cải thiện. Nhóm ngành bán lẻ ghi nhận sức bật rõ rệt nhờ sự phục hồi tiêu dùng nội địa.

Công ty ABC hoạt động trong ngành bán lẻ, có kết quả kinh doanh ổn định và tăng trưởng doanh thu đều đặn trong 5 năm qua. EPS dự báo năm tới đạt khoảng 5.000 VNĐ. Với mức P/E trung bình ngành là 12x, mức giá tham chiếu có thể quanh 60.000 VNĐ.

Ghi nhận gần đây: {
    "Cổ phiếu ABC vừa giảm từ 45.000 xuống còn 40.000 VNĐ trong 1 tuần qua."
    if group == "Nhóm A" else
    "Cổ phiếu ABC từng đạt đỉnh 90.000 VNĐ và hiện đang giao dịch quanh mức 75.000 VNĐ."
}
    """)

    st.markdown("---")
    st.markdown("### \U0001F4AC Bạn đánh giá giá hợp lý hiện tại của cổ phiếu ABC là bao nhiêu?")

    estimated_price = st.number_input("\U0001F4B5 Nhập mức giá bạn định giá (VNĐ):", min_value=0)

    if st.button("✅ Gửi phản hồi"):
        save_to_google_sheets(name, group, estimated_price)
        st.success("✅ Phản hồi của bạn đã được ghi nhận. Cảm ơn bạn!")
