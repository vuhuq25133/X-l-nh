import streamlit as st
import pandas as pd
from PIL import Image

from controller.edge_controller import (
    handle_upload,
    run_edge_detection,
    get_histogram_data
)



def render_dashboard():
    st.set_page_config(page_title="Image Processing – Edge Detection", layout="wide")

    # -----------------------------
    # SIDEBAR – UPLOAD
    # -----------------------------
    st.sidebar.header("📁 Upload ảnh hoặc CSV")
    uploaded_file = st.sidebar.file_uploader(
        "Chọn file", type=["jpg", "jpeg", "png", "csv"]
    )

    original_img, input_type = handle_upload(uploaded_file)

    # -----------------------------
    # SIDEBAR – CHỌN THUẬT TOÁN
    # -----------------------------
    st.sidebar.header("⚙️ Thuật toán phát hiện biên")
    method = st.sidebar.selectbox(
        "Chọn phương pháp:",
        ["Sobel Edge", "Laplacian Edge", "Canny Edge Detection"]
    )

    params = {}
    if method == "Canny Edge Detection":
        params["t_low"] = st.sidebar.slider("Ngưỡng thấp", 0, 255, 50)
        params["t_high"] = st.sidebar.slider("Ngưỡng cao", 0, 255, 100)

    # -----------------------------
    # XỬ LÝ ẢNH
    # -----------------------------
    processed_img, count = run_edge_detection(original_img, method, **params)

    # -----------------------------
    # HIỂN THỊ ẢNH
    # -----------------------------
    st.markdown("## 🔍 Kết quả xử lý ảnh (Edge Detection)")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Ảnh gốc")
        if original_img is not None:
            st.image(original_img, width="stretch", caption="Original Image")
        else:
            st.info("Hãy upload ảnh để bắt đầu.")

    with col2:
        st.markdown(f"### Kết quả ({method})")
        if processed_img is not None:
            # Ảnh nhị phân/grayscale vẫn hiển thị chuẩn
            st.image(processed_img, width="stretch", caption="Processed Image")
            st.success(f"🔢 Số vật thể phát hiện: **{count}**")
        else:
            st.info("Chưa có ảnh kết quả.")

    # -----------------------------
    # HISTOGRAM
    # -----------------------------
    st.markdown("---")
    st.markdown("## 📊 Histogram")

    hcol1, hcol2 = st.columns(2)

    with hcol1:
        st.markdown("### Histogram – Original")
        hist1 = get_histogram_data(original_img)
        if hist1 is not None:
            st.bar_chart(hist1)

    with hcol2:
        st.markdown(f"### Histogram – {method}")
        hist2 = get_histogram_data(processed_img)
        if hist2 is not None:
            st.bar_chart(hist2)

    # -----------------------------
    # SAVE RESULT
    # -----------------------------
    # -----------------------------
    # SAVE RESULT (no pre-created files)
    # -----------------------------
    if processed_img is not None:
        st.sidebar.header("💾 Lưu kết quả")

        import datetime
        import io

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        # Nếu file là ảnh
        if input_type == "image":
            filename = f"processed_{timestamp}.png"

            # Lưu vào RAM thay vì lưu ra file
            buf = io.BytesIO()
            Image.fromarray(processed_img).save(buf, format="PNG")
            buf.seek(0)

            st.sidebar.download_button(
                label="Tải ảnh kết quả (.png)",
                data=buf,
                file_name=filename,
                mime="image/png"
            )

        # Nếu file là CSV
        elif input_type == "csv":
            filename = f"processed_{timestamp}.csv"

            # Lưu CSV vào RAM
            buf = io.StringIO()
            df = pd.DataFrame(processed_img)
            df.to_csv(buf, index=False)
            buf.seek(0)

            st.sidebar.download_button(
                label="Tải dữ liệu kết quả (.csv)",
                data=buf.getvalue(),
                file_name=filename,
                mime="text/csv"
            )
