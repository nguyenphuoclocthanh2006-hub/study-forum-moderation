# Hướng dẫn Vận hành End-to-End (Ngày 7 - Mốc Chốt)

## 1. Chuẩn bị trước khi chạy
- Đảm bảo đã cài đặt Docker và Docker Compose trên máy cá nhân.
- Đã đồng bộ mã nguồn mới nhất từ nhánh main của GitHub.

## 2. Khởi chạy toàn bộ hệ thống
Mở terminal tại thư mục gốc của dự án và chạy lệnh:
```bash
docker-compose up --build -d
```
Lệnh này sẽ khởi động đồng thời 4 services:
1. Redis (Port 6379)
2. AI Service - FastAPI (Port 8001)
3. Backend - Django (Port 8000)
4. Celery Worker (Xử lý hàng đợi bất đồng bộ)

## 3. Checklist Kiểm Thử Luồng (End-to-End)
- [ ] Bài sạch: Đăng bài viết bình thường -> Qua vòng prefilter -> AI phân tích điểm thấp -> Trạng thái APPROVED -> Hiển thị trên Newsfeed.
- [ ] Bài chứa từ cấm / SĐT / Link: Đăng bài chứa từ khóa quảng cáo hoặc SĐT -> Bị phát hiện bởi Prefilter -> Gắn cờ FLAG / NEEDS_REVIEW.
- [ ] Bài ranh giới: Điểm số nằm trong khoảng 0.4 - 0.8 -> Trạng thái NEEDS_REVIEW để kiểm duyệt viên xem xét.
- [ ] Kiểm tra cơ chế Fault-Tolerance (Tắt AI):
  - Chạy lệnh: docker stop <tên_container_ai_service>
  - Đăng bài mới -> Kiểm tra xem sau 2 lần retry, bài viết có tự động chuyển về NEEDS_REVIEW mà không bị sập hệ thống hay không.
- [ ] Kiểm tra Redis Cache: Đăng cùng một nội dung 2 lần liên tiếp, quan sát log của Celery worker để xác nhận lần 2 lấy kết quả từ Cache ([CACHE HIT]).