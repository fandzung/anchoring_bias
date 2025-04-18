import streamlit as st
import pandas as pd
import datetime
import os

st.set_page_config(page_title="Anchoring Bias Game", layout="centered")

CSV_FILE = "responses.csv"

# Giao diện chọn chế độ
mode = st.sidebar.radio("🔑 Chọn chế độ sử dụng:", ["Sinh viên", "Giảng viên"])

# ==============================
# CHẾ ĐỘ SINH VIÊN
# ==============================
if mode == "Sinh viên":
    st.title("\U0001F4CA Trải nghiệm Anchoring Bias trong định giá cổ phiếu")

    if "submitted" not in st.session_state:
        st.session_state.submitted = False
    if "name" not in st.session_state:
        st.session_state.name = ""
    if "group" not in st.session_state:
        st.session_state.group = ""

    def save_response(name, group, estimated_price):
        try:
            df = pd.read_csv(CSV_FILE)
        except:
            df = pd.DataFrame(columns=["timestamp", "name", "group", "estimated_price"])

        new_row = pd.DataFrame([{
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "name": name,
            "group": group,
            "estimated_price": estimated_price
        }])
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(CSV_FILE, index=False)

    if not st.session_state.submitted:
        st.markdown("### \U0001F4DD Vui lòng nhập thông tin để bắt đầu:")
        name = st.text_input("\U0001F539 Họ tên hoặc mã sinh viên", key="name_input")
        group = st.radio("\U0001F538 Nhóm bạn được phân công", ["Nhóm A", "Nhóm B"], key="group_input")

        def submit_info():
            if st.session_state.name_input.strip() == "" or st.session_state.group_input == "Chưa chọn":
                st.warning("⚠️ Vui lòng nhập đầy đủ thông tin.")
            else:
                st.session_state.name = st.session_state.name_input
                st.session_state.group = st.session_state.group_input
                st.session_state.submitted = True

        st.button("🔓 Xác nhận thông tin", on_click=submit_info)

    else:
        name = st.session_state.name
        group = st.session_state.group

        st.markdown(f"""
**Bản tin nội bộ – Đánh giá nhanh cổ phiếu ABC**

Trong bối cảnh kinh tế vĩ mô, tăng trưởng GDP quý gần nhất đạt **5.8%** với lạm phát duy trì ở mức kiểm soát. 

**Lãi suất** điều hành được giữ ổn định, tạo điều kiện cho thanh khoản ngân hàng cải thiện. 

Donald Trump tuyên bố đã hoàn tất sứ mệnh MAGA vĩ đại của mình!

Nhóm ngành bán lẻ ghi nhận sức bật rõ rệt nhờ sự **phục hồi** tiêu dùng nội địa.

Công ty ABC hoạt động trong ngành bán lẻ, có kết quả kinh doanh ổn định và tăng trưởng doanh thu đều đặn trong 5 năm qua. 

EPS dự báo năm tới đạt khoảng **5.000 VNĐ**. Mức P/E trung bình ngành là **12x**.

Tin mới cập nhật: {
    "Cổ phiếu ABC vừa giảm từ **45.000 xuống còn 40.000 VNĐ** trong 1 tuần qua."
    if group == "Nhóm A" else
    "Cổ phiếu ABC từng **đạt đỉnh 90.000 VNĐ** và hiện đang giao dịch quanh mức **75.000 VNĐ**."
}
        """)

        st.markdown("---")
        st.markdown("### \U0001F4AC Theo bạn, **giá hợp lý** hiện tại của cổ phiếu ABC là bao nhiêu?")

        estimated_price = st.number_input("\U0001F4B5 Nhập mức giá bạn định giá (VNĐ):", min_value=0)

        if st.button("✅ Gửi phản hồi"):
            save_response(name, group, estimated_price)
            st.success("✅ Phản hồi của bạn đã được ghi nhận! Cảm ơn bạn.")

# ==============================
# CHẾ ĐỘ GIẢNG VIÊN
# ==============================
elif mode == "Giảng viên":
    st.title("📋 Xem kết quả phản hồi từ sinh viên")
    password = st.text_input("🔐 Nhập mật khẩu truy cập:", type="password")

    if password != "ftu123":
        st.warning("Vui lòng nhập đúng mật khẩu.")
        st.stop()

    if not os.path.exists(CSV_FILE):
        st.info("📭 Chưa có phản hồi nào được ghi nhận.")
        st.stop()

    df = pd.read_csv(CSV_FILE)

    st.subheader("📄 Danh sách phản hồi")
    st.dataframe(df, use_container_width=True)

    st.markdown("### 🕒 Phản hồi gần nhất")
    st.write(df.tail(1))

    st.subheader("📊 Thống kê theo nhóm")
    grouped = df.groupby("group")["estimated_price"].agg(["count", "mean", "min", "max"])
    st.table(grouped.style.format("{:.0f}"))

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Tải toàn bộ kết quả (CSV)", csv, "responses.csv", "text/csv")
