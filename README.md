# Image Processing Dashboard – Edge Detection App

## 1. Giới thiệu

Ứng dụng xử lý ảnh phục vụ học phần *Xử lý Ảnh*. 
Đề tài 2: **Phát hiện biên ảnh và ứng dụng**. 
Cài đặt và hiển thị trực quan các thuật toán: **Sobel, Laplacian, Canny**, và ứng dụng *đếm vật* từ ảnh biên.

---

## 2. Chức năng chính

| Nhóm           | Mô tả                                            |
| -------------- | ------------------------------------------------ |
| Tiền xử lý     | Upload ảnh (.jpg, .png) hoặc ma trận CSV    |
| Phát hiện biên | Sobel, Laplacian, Canny (đếm vật)       |
| Hiển thị       | So sánh Original/Processed + 2 biểu đồ Histogram |
| Lưu kết quả    | Xuất ảnh PNG hoặc CSV tự động theo loại input    |
---

## 3. Cấu trúc thư mục

```
image_processing_dashboard/
 ┛ model/
 ┛ controller/
 ┛ view/
 ┛ uploads/
 ┛ main.py
 ┛ requirements.txt
 ┛ README.md
```

---

## 4. Cài đặt & chạy thử

```bash
python -m venv venv
venv\Scripts\activate      # hoặc source venv/bin/activate
pip install -r requirements.txt
streamlit run main.py
```
Truy cập [Here](http://localhost:8501)

---

## 5. Thư viện chính

* `pandas` - xuất ảnh/CSV
* `numpy` - tính toán ma trận
* `streamlit` - xây dựng giao diện, real-time
* `PIL/Image` - Xử lí ảnh RGB
---

## 6. Giao diện mẫu

* **Sidebar**: Upload → Chọn phương pháp → Save
* **Main area**: Hai ảnh + histogram
* **Count Objects**: Hiển thị số vật thể phát hiện

---

## 7. Thông tin

* **Sinh viên:** Vũ Mạnh Hùng (B22DCCN372)
* **Lớp:** D22HTTT06
* **Học viện Công nghệ Bưu chính Viễn thông**

---
