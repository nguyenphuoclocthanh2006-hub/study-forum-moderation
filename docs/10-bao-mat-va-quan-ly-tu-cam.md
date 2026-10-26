# Tài liệu Bảo mật, Quản lý Từ cấm Động và Rate Limiting (Ngày 11)

## 1. Quản lý Từ cấm Động (`BannedWord CRUD` & `Cache Clearing`)
- Hỗ trợ thêm/sửa/xóa từ cấm trực tiếp qua API quản trị (chỉ dành cho `ADMIN`).
- Mỗi khi thay đổi danh sách từ cấm, hệ thống tự động kích hoạt `cache_clear()`, giúp từ cấm mới có hiệu lực **ngay lập tức** mà không cần khởi động lại server.

## 2. Giới hạn tần suất (`Rate Limiting & Throttling`)
- Kết hợp giữa Django REST Framework Throttling và Redis để giới hạn thao tác (ví dụ: tối đa 5 bài/phút cho `anon_token`, 3 lần đăng nhập sai/phút). Vượt ngưỡng sẽ nhận mã lỗi chuẩn **429 Too Many Requests**.

## 3. Kiểm tra Đầu vào & Chống Tấn công (`Input Validation & Security`)
- Kiểm tra độ dài, kiểu dữ liệu, và escape ký tự đặc biệt chống tấn công **XSS**.
- Bộ lọc phát hiện và vô hiệu hóa các mẫu câu tấn công **SQL Injection** trong các trường tìm kiếm hoặc nội dung gửi lên.

## 4. Kiểm thử Bảo mật Tự động
- Mọi endpoint quản trị đều được kiểm tra phân quyền nghiêm ngặt (`401 Unauthorized` / `403 Forbidden` đối với khách vãng lai).