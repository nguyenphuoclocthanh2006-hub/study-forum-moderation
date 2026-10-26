# Tài liệu Thống kê, Giải thích AI và Cấu hình Động (Ngày 9)

## 1. Giải thích quyết định AI (`/admin/queue/<id>/explain`)
- Khi quản trị viên bấm vào xem chi tiết một bài viết cần xem xét, hệ thống gọi API `/explain` để trả về các yếu tố, từ khóa chính có trọng số cao khiến AI đưa ra mức điểm `toxic_score` tương ứng.

## 2. Thống kê hệ thống (`/admin/stats`)
- Cung cấp số liệu tổng quan về lượng bài viết theo ngày, tỷ lệ phân bố các trạng thái (`APPROVED`, `NEEDS_REVIEW`, `REJECTED`), và top các từ khóa vi phạm nhiều nhất.

## 3. Cấu hình ngưỡng động (`/admin/settings`)
- Cho phép quản trị viên cấp cao (Admin) thay đổi linh hoạt các ngưỡng phân loại (`low_threshold`, `high_threshold`) trực tiếp qua API.
- Celery Worker sẽ đọc giá trị ngưỡng mới từ DB/Redis ngay khi xử lý bài viết tiếp theo mà **không cần khởi động lại (restart) dịch vụ**.