# Tài liệu Precheck Tốc độ cao và Quản lý Feedback Dataset (Ngày 10)

## 1. API Kiểm tra trước (`POST /moderation/precheck`)
- Quét nhanh nội dung bằng Regex và từ điển từ khóa trước khi đưa vào hàng đợi AI chính thức.
- **Đặc điểm**: Không lưu bài viết vào database ở bước này, thời gian phản hồi cực nhanh **dưới 100 ms**, giúp người dùng nhận được cảnh báo ngay lập tức trên giao diện trình duyệt.

## 2. Giới hạn tần suất (`Rate Limiting`)
- Áp dụng cơ chế đếm số lượng request qua Redis (`10 requests / phút / user`) để chống lạm dụng API precheck.

## 3. Thu thập Feedback & Huấn luyện lại mô hình (Retraining)
- Khi quản trị viên thực hiện đảo quyết định so với kết quả ban đầu của AI, hệ thống lưu lại đồng thời `ai_decision` và `admin_decision` kèm theo lý do.
- Hỗ trợ lệnh quản trị Django (`python manage.py export_feedback`) để xuất toàn bộ dữ liệu này ra định dạng CSV phục vụ cho việc fine-tune lại mô hình PhoBERT trong tương lai.