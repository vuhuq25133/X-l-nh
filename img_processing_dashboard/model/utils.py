import numpy as np
from PIL import Image

import cv2
import numpy as np
import matplotlib.pyplot as plt

def compute_histogram(img):
    """Trả về figure histogram của ảnh."""
    gray = img if len(img.shape)==2 else cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    hist = cv2.calcHist([gray],[0],None,[256],[0,256])
    fig, ax = plt.subplots()
    ax.plot(hist, color='black')
    ax.set_title("Histogram")
    ax.set_xlabel("Intensity")
    ax.set_ylabel("Frequency")
    plt.tight_layout()
    return fig


def load_image(uploaded_file):
    """Đọc file ảnh hoặc CSV, trả về numpy array và loại input."""
    if uploaded_file is None:
        return None, None

    filename = uploaded_file.name.lower()
    if filename.endswith(('.jpg', '.jpeg', '.png')):
        img = Image.open(uploaded_file).convert('RGB')
        return np.array(img), "image"
    elif filename.endswith('.csv'):
        import pandas as pd
        df = pd.read_csv(uploaded_file, header=None)
        img = df.to_numpy().astype(np.uint8)
        return img, "csv"
    else:
        return None, None

def to_gray(img):
    """Chuyển ảnh RGB sang ảnh xám."""
    if len(img.shape) == 2:
        return img  # đã là ảnh xám
    return np.dot(img[..., :3], [0.2989, 0.5870, 0.1140]).astype(np.uint8)
