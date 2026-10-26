import time
import hashlib
import json
import requests
from celery import Celery
from moderation.prefilter import prefilter_text
import redis

celery_app = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')
AI_SERVICE_URL = "http://localhost:8001/predict"
redis_client = redis.Redis(host='localhost', port=6379, db=0)

@celery_app.task(bind=True, max_retries=2, default_retry_delay=5)
def moderate_post(self, post_id: int, post_content: str):
    # 1. Chạy tiền lọc luật (Prefilter)
    prefilter_result = prefilter_text(post_content)
    if prefilter_result["status"] == "FLAG":
        print(f"[PREFILTER] Post ID {post_id} bị FLAG: {prefilter_result['reason']}")
        return {
            "post_id": post_id, 
            "toxic_score": None, 
            "status": "NEEDS_REVIEW", 
            "flag_reason": prefilter_result['reason']
        }

    # 2. Tạo mã băm SHA-256 từ nội dung chuẩn hóa làm khóa cache (TTL 24h)
    normalized_content = " ".join(post_content.lower().split())
    cache_key = f"mod_cache:{hashlib.sha256(normalized_content.encode('utf-8')).hexdigest()}"
    
    cached_data = redis_client.get(cache_key)
    if cached_data:
        print(f"[CACHE HIT] Post ID {post_id} lấy kết quả từ Redis Cache!")
        return json.loads(cached_data.decode('utf-8'))

    try:
        # 3. Gọi AI service với timeout 5 giây
        response = requests.post(
            AI_SERVICE_URL, 
            json={"text": post_content}, 
            timeout=5.0
        )
        
        if response.status_code != 200:
            raise Exception(f"AI Service error status: {response.status_code}")
            
        data = response.json()
        toxic_score = data.get("toxic_score", 0.0)
        
        # Áp dụng ngưỡng phân loại
        if toxic_score < 0.4:
            status = "APPROVED"
        elif 0.4 <= toxic_score <= 0.8:
            status = "NEEDS_REVIEW"
        else:
            status = "REJECTED"
            
        result = {"post_id": post_id, "toxic_score": toxic_score, "status": status, "source": "AI_Model"}
        
        # Lưu vào Redis Cache (TTL = 86400 giây = 24 giờ)
        redis_client.setex(cache_key, 86400, json.dumps(result))
        
        print(f"[AI MODEL] Post ID {post_id} -> Score: {toxic_score} -> Status: {status}")
        return result

    except (requests.exceptions.RequestException, Exception) as exc:
        print(f"[WARNING] Lỗi mạng hoặc timeout khi kiểm duyệt bài {post_id}: {exc}")
        try:
            raise self.retry(exc=exc)
        except self.MaxRetriesExceededError:
            print(f"[ERROR] Thử lại 2 lần thất bại. Chuyển bài viết {post_id} sang NEEDS_REVIEW.")
            return {"post_id": post_id, "toxic_score": None, "status": "NEEDS_REVIEW", "error": "AI Service unavailable"}
