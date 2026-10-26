import re
import time
import redis
from functools import lru_cache

# Kết nối Redis an toàn
try:
    redis_client = redis.Redis(host='localhost', port=6379, db=0, socket_timeout=1)
    redis_client.ping()
except Exception:
    redis_client = None

# Database giả lập danh sách từ cấm
BANNED_WORDS_DB = ["tục_tỉu_1", "lừa_đảo", "spam_ads"]

@lru_cache(maxsize=128)
def get_cached_banned_words():
    # Lấy danh sách từ cấm có sử dụng bộ nhớ đệm (Cache)
    return tuple(BANNED_WORDS_DB)

def manage_banned_word(action: str, word: str = None, user_role: str = "ADMIN"):
    # API CRUD cho BannedWord và xóa cache khi thay đổi
    if user_role != "ADMIN":
        return {"error": "Forbidden: Chỉ Admin mới được quản lý từ cấm", "status_code": 403}
        
    global BANNED_WORDS_DB
    word_cleaned = word.strip().lower() if word else ""
    
    if action == "add" and word_cleaned:
        if word_cleaned not in BANNED_WORDS_DB:
            BANNED_WORDS_DB.append(word_cleaned)
    elif action == "remove" and word_cleaned:
        if word_cleaned in BANNED_WORDS_DB:
            BANNED_WORDS_DB.remove(word_cleaned)
            
    # Xóa cache ngay lập tức để áp dụng từ cấm mới
    get_cached_banned_words.cache_clear()
    
    return {
        "status": "success",
        "action": action,
        "current_banned_words": list(get_cached_banned_words())
    }

def check_rate_limit(key_identifier: str, max_calls: int, window_seconds: int = 60) -> bool:
    # Rate limit (Redis): ví dụ 5 bài/phút. Trả về True nếu vượt quá giới hạn (429).
    if not redis_client:
        return False
        
    try:
        rate_key = f"rate_limit:{key_identifier}"
        current = redis_client.get(rate_key)
        if current and int(current) >= max_calls:
            return True
            
        pipeline = redis_client.pipeline()
        pipeline.incr(rate_key, 1)
        pipeline.expire(rate_key, window_seconds)
        pipeline.execute()
    except Exception:
        pass
    return False

def validate_and_sanitize_input(text: str) -> dict:
    # Validate đầu vào, chống XSS và SQLi cơ bản
    if not isinstance(text, str):
        return {"valid": False, "error": "Kiểu dữ liệu không hợp lệ"}
        
    if len(text) > 5000:
        return {"valid": False, "error": "Nội dung quá dài (tối đa 5000 ký tự)"}
        
    # Phát hiện mẫu SQL Injection cơ bản
    sql_i_patterns = ["--", "or 1=1", "drop table", "union select", "exec("]
    for pattern in sql_i_patterns:
        if pattern in text.lower():
            return {"valid": False, "error": "Phát hiện ký tự hoặc lệnh SQL độc hại tiềm ẩn!", "security_alert": True}
            
    # XSS Escape cơ bản
    sanitized = text.replace("<", "&lt;").replace(">", "&gt;")
    
    # Kiểm tra từ cấm đã cache
    current_banned = get_cached_banned_words()
    matched_banned = [bw for bw in current_banned if bw in sanitized.lower()]
    
    if matched_banned:
        return {"valid": True, "blocked": True, "reason": f"Chứa từ cấm: {matched_banned}", "sanitized_text": sanitized}
        
    return {"valid": True, "blocked": False, "sanitized_text": sanitized}
