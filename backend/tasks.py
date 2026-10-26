import time
import requests
from celery import Celery

celery_app = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')
AI_SERVICE_URL = "http://localhost:8001/predict"

@celery_app.task(bind=True, max_retries=2, default_retry_delay=5)
def moderate_post(self, post_id: int, post_content: str):
    try:
        # Gọi AI service với timeout 5 giây
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
            
        print(f"[DB SAVE] Post ID {post_id} -> Score: {toxic_score} -> Status: {status}")
        return {"post_id": post_id, "toxic_score": toxic_score, "status": status}

    except (requests.exceptions.RequestException, Exception) as exc:
        print(f"[WARNING] Lỗi mạng hoặc timeout khi kiểm duyệt bài {post_id}: {exc}")
        try:
            raise self.retry(exc=exc)
        except self.MaxRetriesExceededError:
            print(f"[ERROR] Thử lại 2 lần thất bại. Chuyển bài viết {post_id} sang NEEDS_REVIEW.")
            return {"post_id": post_id, "toxic_score": None, "status": "NEEDS_REVIEW", "error": "AI Service unavailable"}
