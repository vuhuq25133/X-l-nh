from .utils import to_gray
import cv2
import numpy as np

def sobel_edge(img):
    gray = to_gray(img)
    sx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    sy = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    sobel = cv2.magnitude(sx, sy)
    return np.uint8(sobel)

def laplacian_edge(img):
    gray = to_gray(img)
    lap = cv2.Laplacian(gray, cv2.CV_64F)
    lap = cv2.convertScaleAbs(lap)
    return lap


def canny_edge(img, t1=100, t2=200):
    """Phát hiện biên bằng thuật toán Canny."""
    gray = to_gray(img)
    # Bước 1: làm mờ Gaussian để giảm nhiễu
    blur = cv2.GaussianBlur(gray, (5, 5), 1.4)
    # Bước 2–4: tính gradient, NMS, hysteresis (cv2.Canny làm sẵn)
    edge = cv2.Canny(blur, threshold1=t1, threshold2=t2)
    return edge

def process_image(img, method, **kwargs):
    if img is None: 
        return None
    if method == "Grayscale Conversion":
        return to_gray(img)
    elif method == "Sobel Filter":
        return sobel_edge(img)
    elif method == "Laplacian Filter":
        return laplacian_edge(img)
    elif method == "Canny Edge Detection":
        t1 = kwargs.get("t1", 100)
        t2 = kwargs.get("t2", 200)
        return canny_edge(img, t1, t2)
    else:
        return img
    
def count_objects(img):
    """
    Đếm số vật thể (vùng trắng) trong ảnh nhị phân.
    Trả về (ảnh tô biên, số lượng).
    """
    gray = to_gray(img)
    # đảm bảo ảnh nhị phân
    _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    output = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    cv2.drawContours(output, contours, -1, (0, 0, 255), 2)
    return output, len(contours)
