from model.utils import load_image
from model.image_processing import process_image
from model.utils import compute_histogram
from model.image_processing import count_objects
import streamlit as st

def get_histograms(original_img, processed_img):
    h1 = compute_histogram(original_img) if original_img is not None else None
    h2 = compute_histogram(processed_img) if processed_img is not None else None
    return h1, h2

def handle_upload(uploaded_file):
    """
    Đọc ảnh/CSV được upload.
    Trả về (ảnh numpy, loại input).
    """
    return load_image(uploaded_file)

def run_processing(original_img, method):
    """
    Gọi hàm xử lý ảnh trong Model và trả về ảnh kết quả.
    """
    if original_img is None or method is None:
        return None
    result = process_image(original_img, method)
    return result

def run_processing(original_img, method, **kwargs):
    from model.image_processing import process_image
    if original_img is None:
        return None
    if method == "Count Objects":
        # Nếu chưa có biên, dùng Canny mặc định
        edge = process_image(original_img, "Canny Edge Detection", t1=100, t2=200)
        result_img, num = count_objects(edge)
        st.session_state["object_count"] = num
        return result_img
    else:
        return process_image(original_img, method, **kwargs)