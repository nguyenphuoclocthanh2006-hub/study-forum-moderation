# Tài liệu Đặc tả API Hệ thống Kiểm duyệt (Ngày 12)

## 1. API Kiểm tra trước (Precheck)
- **Endpoint**: `POST /moderation/precheck`
- **Mô tả**: Quét nhanh từ cấm bằng regex/cache, không lưu DB, tốc độ phản hồi dưới 100ms.
- **Request Body**:
  ```json
  {
    "text": "Mua bán acc game giảm giá qua zalo 0912345678",
    "user_id": "user_123"
  }
  ```
- **Response mẫu**:
  ```json
  {
    "verdict": "FLAG",
    "words": ["mua bán", "giảm giá"],
    "score": 0.95,
    "latency_ms": 0.35
  }
  ```

## 2. API Quản lý Từ cấm (Admin CRUD)
- **Endpoint**: `POST /admin/banned-words`
- **Mô tả**: Thêm/xóa từ cấm và tự động kích hoạt `cache_clear()` để áp dụng ngay lập tức.
- **Request Body**:
  ```json
  {
    "action": "add",
    "word": "vi_pham_moi"
  }
  ```
- **Response mẫu**:
  ```json
  {
    "status": "success",
    "action": "add",
    "current_banned_words": ["tục_tỉu_1", "lừa_đảo", "spam_ads", "vi_pham_moi"]
  }
  ```

## 3. API Thống kê & Cấu hình Ngưỡng (Admin Settings)
- **Endpoint**: `POST /admin/settings`
- **Mô tả**: Thay đổi ngưỡng `low_threshold` và `high_threshold` áp dụng tức thì.
- **Request Body**:
  ```json
  {
    "low_threshold": 0.35,
    "high_threshold": 0.75
  }
  ```
- **Response mẫu**:
  ```json
  {
    "status": "success",
    "message": "Đã cập nhật ngưỡng thành công!",
    "settings": {
        "low_threshold": 0.35,
        "high_threshold": 0.75
    }
  }
  ```