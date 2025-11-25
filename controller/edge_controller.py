from model.utils import load_image
from model.image_processing import (
    sobel_edge_with_count,
    laplacian_edge_with_count,
    canny_edge_with_count,
    compute_histogram
)

# -----------------------------
# HANDLE FILE UPLOAD
# -----------------------------
def handle_upload(uploaded_file):
    """
    Đọc ảnh (jpg/png) hoặc CSV rồi trả về:
    (numpy_img, loại_file)
    """
    return load_image(uploaded_file)


# -----------------------------
# PROCESSING WRAPPER
# -----------------------------
def run_edge_detection(img, method, **params):

    if img is None:
        return None, 0

    if method == "Sobel Edge":
        return sobel_edge_with_count(img)

    elif method == "Laplacian Edge":
        return laplacian_edge_with_count(img)

    elif method == "Canny Edge Detection":
        t_low = params.get("t_low", 50)
        t_high = params.get("t_high", 100)
        return canny_edge_with_count(img, t_low, t_high)

    else:
        return None, 0


# -----------------------------
# HISTOGRAM
# -----------------------------
def get_histogram_data(img):
    """
    Trả về histogram dạng mảng 256 phần tử.
    """
    if img is None:
        return None
    return compute_histogram(img)
