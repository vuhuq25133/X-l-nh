import numpy as np
from PIL import Image

def load_image(uploaded_file):
    if uploaded_file is None:
        return None, None

    filename = uploaded_file.name.lower()

    if filename.endswith(('.jpg', '.jpeg', '.png')):
        img = Image.open(uploaded_file).convert('RGB')  # convert to grayscale
        return np.array(img).astype(np.uint8), "image"

    elif filename.endswith('.csv'):
        import pandas as pd
        df = pd.read_csv(uploaded_file, header=None)
        img = df.to_numpy().astype(np.uint8)
        return img, "csv"

    return None, None
