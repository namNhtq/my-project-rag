# RAG 

## Giới thiệu
Đề tài này là một bài thực hành trong môn học của tôi nhằm hiểu được RAG là gì? Xây dựng hệ thống, cấu trúc trong RAG ra sao. Tuy nhiên, đây là chỉ là một phần của Project cuối kỳ cho môn học này nên tôi sẽ update các cải thiện dần theo thời gian.

Đề tài này xây dựng một hệ thống chatbot dựa trên mô hình **Retrieval-Augmented Generation (RAG)**. Chatbot có khả năng tìm kiếm và tổng hợp thông tin từ tập dữ liệu có sẵn, sau đó tạo ra câu trả lời thông minh và chính xác.

- Lưu ý: Hiện chatbot này đang đọc được dữ liệu từ file PDF nhưng là PDF thuần chữ, PDF dạng bảng. Ở đây tôi sử dụng data từ file PDF về môn Tư tưởng Hồ Chí Minh và file PDF dạng bảng trong tài chính.

Hệ thống bao gồm các thành phần chính:
- **Backend**: Xử lý dữ liệu, truy vấn và tích hợp với mô hình AI.
- **Frontend**: Giao diện web để người dùng tương tác với chatbot.
- **Data Storage**: Lưu trữ dữ liệu văn bản để phục vụ tìm kiếm thông tin.
- **Docker & Deployment**: Đóng gói và triển khai dễ dàng với Docker.

---

## Cấu trúc thư mục
```
Lab2_RAG/
│── backend/            # Xử lý dữ liệu và API
│   ├── config.py       # Cấu hình hệ thống
│   ├── database.py     # Quản lý cơ sở dữ liệu
│   ├── embedding.py    # Xử lý embedding
│   ├── main.py         # API chính
│   ├── process_pdf.py  # Xử lý file PDF
│   ├── query.py        # Truy vấn dữ liệu
│── data/documents/     # Lưu trữ tài liệu PDF
│── frontend/           # Giao diện người dùng
│   ├── app.py          # Chạy frontend
│── notebooks/          # Chứa các notebook xử lý dữ liệu
│── docker-compose.yaml # Cấu hình Docker
│── .gitignore          # Danh sách file bị ignore
│── README.md           # Hướng dẫn sử dụng
```

---

## Cài đặt và chạy hệ thống
### 1. Yêu cầu hệ thống
- Python 3.10
- Docker & Docker Compose
- Các thư viện trong `requirements.txt`

### 2. Cài đặt môi trường
Chạy lệnh sau để cài đặt các thư viện cần thiết:
```sh
pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt
```

### 3. Chạy hệ thống bằng Docker
Khởi chạy toàn bộ hệ thống bằng Docker:
```sh
docker-compose up --build
```

## 4. Sử dụng chatbot
- Truy cập giao diện web tại `localhost:8501`
- Nhập câu hỏi vào chatbot và nhận câu trả lời từ hệ thống.
---

(...)


