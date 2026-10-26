import re
import time
import csv
import redis

# Thử kết nối Redis, nếu không có thì đặt là None để chạy giả lập không bị lỗi
try:
    redis_client = redis.Redis(host='localhost', port=6379, db=0, socket_timeout=1)
    redis_client.ping()
except Exception:
    redis_client = None

def precheck_content(text: str, user_id: str = "default_user") -> dict:
    start_time = time.time()
    
    # 1. Rate Limiting: Tối đa 10 lần / phút / người dùng (chỉ chạy khi có Redis)
    if redis_client:
        try:
            rate_key = f"rate_limit:precheck:{user_id}"
            current_requests = redis_client.get(rate_key)
            if current_requests and int(current_requests) >= 10:
                return {
                    "verdict": "BLOCKED_RATE_LIMIT",
                    "message": "Quá giới hạn 10 lần kiểm tra/phút. Vui lòng thử lại sau.",
                    "latency_ms": round((time.time() - start_time) * 1000, 2)
                }
            pipeline = redis_client.pipeline()
            pipeline.incr(rate_key, 1)
            pipeline.expire(rate_key, 60)
            pipeline.execute()
        except Exception:
            pass # Bỏ qua nếu Redis ngắt kết nối giữa chừng

    if not text:
        return {"verdict": "PASS", "words": [], "score": 0.0, "latency_ms": 1.0}

    text_lower = text.lower()
    
    # 2. Danh sách từ khóa cấm / quảng cáo mẫu
    forbidden_keywords = ["mua bán", "giảm giá", "inbox zalo", "hotline", "khuyến mãi", "tuyển dụng"]
    found_words = [kw for kw in forbidden_keywords if kw in text_lower]
    
    # Kiểm tra SĐT hoặc Link
    phone_pattern = r'(\+84|0[35789])[0-9]{8}'
    url_pattern = r'https?://\S+|www\.\S+'
    
    has_phone = bool(re.search(phone_pattern, text))
    has_link = bool(re.search(url_pattern, text))
    
    if found_words or has_phone or has_link:
        matched_repr = found_words if found_words else ["số điện thoại hoặc đường dẫn ngoài"]
        latency = round((time.time() - start_time) * 1000, 2)
        return {
            "verdict": "FLAG",
            "words": matched_repr,
            "score": 0.95,
            "latency_ms": latency
        }
        
    latency = round((time.time() - start_time) * 1000, 2)
    return {
        "verdict": "PASS",
        "words": [],
        "score": 0.05,
        "latency_ms": latency
    }

# 3. Quản lý Dataset Feedback (AI Decision vs Admin Decision)
FEEDBACK_DATABASE = [
    {"post_id": 1, "content": "Nội dung bình thường", "ai_decision": "APPROVED", "admin_decision": "APPROVED", "reason": "Chính xác"},
    {"post_id": 2, "content": "Bài ranh giới bị AI bắt nhầm", "ai_decision": "REJECTED", "admin_decision": "APPROVED", "reason": "AI nhầm lẫn ngữ cảnh học tập"}
]

def export_feedback_to_csv(filepath="/content/drive/MyDrive/study-forum-moderation/feedback_dataset.csv"):
    keys = ["post_id", "content", "ai_decision", "admin_decision", "reason"]
    
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for row in FEEDBACK_DATABASE:
            writer.writerow(row)
            
    print(f"[EXPORT] Đã xuất thành công {len(FEEDBACK_DATABASE)} dòng dữ liệu feedback ra file: {filepath}")
    return filepath
