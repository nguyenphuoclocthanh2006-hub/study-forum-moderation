# Tài liệu Kiến trúc Hệ thống Kiểm duyệt (Ngày 12)

## 1. Sơ đồ Kiến trúc Microservices
Hệ thống sử dụng mô hình Docker-orchestrated bao gồm các thành phần chính:
- **Django Backend & Admin**: Xử lý logic nghiệp vụ, quản lý người dùng, phân quyền RBAC, và cung cấp API quản trị.
- **FastAPI AI Service**: Chạy mô hình PhoBERT tối ưu trên CPU/GPU để phân loại nội dung độc hại.
- **Redis Cache & Broker**: Lưu trữ cache từ cấm (SHA-256), giới hạn tần suất (Rate Limiting), và làm message broker cho Celery.
- **Celery Worker**: Xử lý hàng đợi bất đồng bộ (Asynchronous task queue) giúp không làm nghẽn luồng HTTP request của người dùng.

## 2. Luồng Kiểm duyệt Bất đồng bộ (Sequence Diagram)

```mermaid
sequenceDiagram
    autonumber
    actor User as Người dùng
    participant Django as Django Backend
    participant Prefilter as Pre-filter (Regex/Cache)
    participant Redis as Redis Queue (Celery)
    participant Worker as Celery Worker
    participant AI as FastAPI AI Service
    participant DB as Database (PostgreSQL)

    User->>Django: Gửi bài viết mới (POST /posts)
    Django->>Prefilter: Kiểm tra nhanh từ cấm / SĐT / Link (<1ms)
    alt Phát hiện từ cấm rõ ràng
        Prefilter-->>Django: Trả về verdict: REJECTED ngay lập tức
        Django-->>User: Từ chối bài viết (Không cần gọi AI)
    else Nội dung hợp lệ qua sơ lọc
        Prefilter-->>Django: Trả về verdict: PASS
        Django->>Redis: Đẩy task vào hàng đợi Celery
        Django-->>User: Phản hồi 'Bài viết đang được xử lý ngầm' (202 Accepted)
        
        Redis->>Worker: Lấy task bất đồng bộ
        Worker->>AI: Gửi nội dung sang FastAPI AI (PhoBERT)
        AI-->>Worker: Trả về kết quả dự đoán (Score, Label)
        Worker->>DB: Lưu trạng thái bài viết & Log kiểm duyệt
    end
```