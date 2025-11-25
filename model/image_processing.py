import numpy as np

# Convolution 2D 
# ======================================
def conv2d(img, kernel):
    kh, kw = kernel.shape
    pad_h, pad_w = kh // 2, kw // 2

    padded = np.pad(img, ((pad_h, pad_h), (pad_w, pad_w)), mode='edge')
    H, W = img.shape
    out = np.zeros((H, W), dtype=float)

    for i in range(H):
        for j in range(W):
            region = padded[i:i+kh, j:j+kw]
            out[i, j] = np.sum(region * kernel)

    return out


# ======================================
# Connected Components Counting
# ======================================
def count_components(binary_img):
    H, W = binary_img.shape
    visited = np.zeros((H, W), dtype=bool)

    def dfs(x, y):
        stack = [(x, y)]
        while stack:
            i, j = stack.pop()
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    ni, nj = i + dx, j + dy
                    if 0 <= ni < H and 0 <= nj < W:
                        if binary_img[ni, nj] > 0 and not visited[ni, nj]:
                            visited[ni, nj] = True
                            stack.append((ni, nj))

    count = 0
    for i in range(H):
        for j in range(W):
            if binary_img[i, j] > 0 and not visited[i, j]:
                visited[i, j] = True
                dfs(i, j)
                count += 1

    return count


# ======================================
# 1. Sobel Edge + Count
# ======================================
def sobel_edge_with_count(img):
    if img.ndim == 3:   # RGB → Grayscale
        img = np.dot(img[...,:3], [0.2989, 0.5870, 0.1140]).astype(np.uint8)
    Gx = np.array([[-1, 0, 1],
                   [-2, 0, 2],
                   [-1, 0, 1]])

    Gy = np.array([[-1,-2,-1],
                   [ 0, 0, 0],
                   [ 1, 2, 1]])

    sx = conv2d(img, Gx)
    sy = conv2d(img, Gy)

    mag = np.sqrt(sx**2 + sy**2)
    mag = (mag / np.max(mag)) * 255
    edge = mag.astype(np.uint8)

    binary = (edge > 50).astype(np.uint8) * 255
    count = count_components(binary)
    return edge, count


# ======================================
# 2. Laplacian Edge + Count
# ======================================
def laplacian_edge_with_count(img):
    if img.ndim == 3:   # RGB → Grayscale
        img = np.dot(img[...,:3], [0.2989, 0.5870, 0.1140]).astype(np.uint8)
    L = np.array([[0,1,0],
                  [1,-4,1],
                  [0,1,0]])

    lap = conv2d(img, L)
    lap = np.abs(lap)
    lap = (lap / np.max(lap)) * 255
    edge = lap.astype(np.uint8)

    binary = (edge > 50).astype(np.uint8) * 255
    count = count_components(binary)
    return edge, count


# ======================================
# Gaussian Blur
# ======================================
def gaussian_blur(img, size=5, sigma=1.4):
    ax = np.linspace(-(size - 1) / 2., (size - 1) / 2., size)
    gauss = np.exp(-0.5 * (ax**2) / sigma**2)
    kernel = np.outer(gauss, gauss)
    kernel /= kernel.sum()
    return conv2d(img, kernel)


# ======================================
# NMS
# ======================================
def nms(mag, theta):
    H, W = mag.shape
    Z = np.zeros((H, W), dtype=np.uint8)
    angle = (np.rad2deg(theta) + 180) % 180

    for i in range(1, H - 1):
        for j in range(1, W - 1):
            q = 255
            r = 255

            # 0 deg
            if (0 <= angle[i,j] < 22.5) or (157.5 <= angle[i,j] <= 180):
                q = mag[i, j+1]
                r = mag[i, j-1]

            # 45 deg
            elif 22.5 <= angle[i,j] < 67.5:
                q = mag[i+1, j-1]
                r = mag[i-1, j+1]

            # 90 deg
            elif 67.5 <= angle[i,j] < 112.5:
                q = mag[i+1, j]
                r = mag[i-1, j]

            # 135 deg
            elif 112.5 <= angle[i,j] < 157.5:
                q = mag[i-1, j-1]
                r = mag[i+1, j+1]

            if mag[i,j] >= q and mag[i,j] >= r:
                Z[i,j] = mag[i,j]
            else:
                Z[i,j] = 0

    return Z


# ======================================
# Hysteresis Threshold
# ======================================
def hysteresis(img, t_low, t_high):
    strong = 255
    weak = 50

    H, W = img.shape
    res = np.zeros((H, W), dtype=np.uint8)

    strong_i, strong_j = np.where(img >= t_high)
    weak_i, weak_j     = np.where((img < t_high) & (img >= t_low))

    res[strong_i, strong_j] = strong
    res[weak_i, weak_j]     = weak

    changed = True
    while changed:
        changed = False
        for i in range(1, H-1):
            for j in range(1, W-1):
                if res[i,j] == weak:
                    if np.any(res[i-1:i+2, j-1:j+2] == strong):
                        res[i,j] = strong
                        changed = True

    res[res != strong] = 0
    return res


# ======================================
# 3. Canny + Count
# ======================================
def canny_edge_with_count(img, t_low=50, t_high=100):
    if img.ndim == 3:   # RGB → Grayscale
        img = np.dot(img[...,:3], [0.2989, 0.5870, 0.1140]).astype(np.uint8)
    blur = gaussian_blur(img)

    # Sobel
    Gx = np.array([[-1,0,1],[-2,0,2],[-1,0,1]])
    Gy = np.array([[-1,-2,-1],[0,0,0],[1,2,1]])

    sx = conv2d(blur, Gx)
    sy = conv2d(blur, Gy)

    mag = np.sqrt(sx**2 + sy**2)
    mag = (mag / np.max(mag)) * 255
    theta = np.arctan2(sy, sx)

    # NMS
    nms_img = nms(mag, theta)

    # Hysteresis Threshold
    edges = hysteresis(nms_img, t_low, t_high)

    # Count
    count = count_components(edges)

    return edges, count


# ======================================
# Histogram
# ======================================
def compute_histogram(img):
    hist, _ = np.histogram(img.flatten(), bins=256, range=(0,256))
    return hist