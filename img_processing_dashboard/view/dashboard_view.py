import streamlit as st
from controller.edge_controller import handle_upload, run_processing
from PIL import Image
import numpy as np
from controller.edge_controller import get_histograms


def render_dashboard():
    st.set_page_config(page_title="Image Processing Dashboard", layout="wide")

    st.sidebar.header("1️⃣ Upload ảnh")
    uploaded_file = st.sidebar.file_uploader(
        "Chọn ảnh hoặc file CSV",
        type=["jpg", "jpeg", "png", "csv"]
    )

    original_img, input_type = handle_upload(uploaded_file)

    # ========== Dropdown chọn phương pháp ==========
    st.sidebar.header("2️⃣ Chọn tính năng xử lý ảnh")

    method = st.sidebar.selectbox(
        "Chọn chức năng:",
        ["Grayscale Conversion", "Sobel Filter", "Laplacian Filter", "Canny Edge Detection", "Count Objects"]
    )

    params = {}
    if method == "Canny Edge Detection":
        params["t1"] = st.sidebar.slider("Ngưỡng thấp", 0, 255, 100)
        params["t2"] = st.sidebar.slider("Ngưỡng cao", 0, 255, 200)

    processed_img = run_processing(original_img, method, **params)

    # ====== Layout chính ======
    st.markdown("## 📷 Kết quả xử lý ảnh")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Original")
        if original_img is not None:
            st.image(original_img, channels="RGB", width="stretch")
        else:
            st.info("Vui lòng upload ảnh hoặc CSV để hiển thị.")

    with col2:
        st.markdown(f"### Result ({method})")
        if processed_img is not None:
            if len(processed_img.shape) == 2:
                st.image(processed_img, channels="GRAY", width="stretch")
            else:
                st.image(processed_img, channels="RGB", width="stretch")
        else:
            st.info("Chưa có ảnh kết quả.")
    
    hcol1, hcol2 = st.columns(2)
    hist1, hist2 = get_histograms(original_img, processed_img)

    with hcol1:
        st.markdown("#### Histogram (Original)")
        if hist1: st.pyplot(hist1)

    with hcol2:
        st.markdown("#### Histogram (Processed)")
        if hist2: st.pyplot(hist2)
        
    if "object_count" in st.session_state and method == "Count Objects":
        st.success(f"🔢 Số vật thể phát hiện: {st.session_state['object_count']}")

    # ====== Nút Save ======
    if original_img is not None:
        st.sidebar.header("3️⃣ Lưu kết quả")
        import pandas as pd
        import io, cv2
        from PIL import Image

        if input_type == "image":
            img_pil = Image.fromarray(processed_img)
            buf = io.BytesIO()
            img_pil.save(buf, format="PNG")
            st.sidebar.download_button(
                label="💾 Lưu ảnh kết quả (.png)",
                data=buf.getvalue(),
                file_name="edge_result.png",
                mime="image/png"
            )
        elif input_type == "csv":
            csv_data = pd.DataFrame(processed_img)
            st.sidebar.download_button(
                label="📊 Lưu dữ liệu (.csv)",
                data=csv_data.to_csv(index=False).encode('utf-8'),
                file_name="edge_result.csv",
                mime="text/csv"
            )

