# Kịch bản kiểm thử End-to-End cho Ngày 7 (Mốc chốt)
# Sử dụng script này sau khi chạy 'docker-compose up --build'

import requests
import time

BACKEND_URL = "http://localhost:8000/api/posts" # (Điều chỉnh lại endpoint theo code của bạn bạn sau)
AI_SERVICE_URL = "http://localhost:8001/predict"

def test_scenario():
    print("🚀 BẮT ĐẦU KIỂM THỬ END-TO-END HỆ THỐNG KIỂM DUYỆT...")
    
    # 1. Test bài sạch -> Phải APPROVED
    clean_post = {"title": "Học tập", "content": "Hôm nay mình học môn cấu trúc dữ liệu rất hay."}
    print(f"-> Gửi bài sạch: {clean_post['content']}")
    
    # 2. Test bài có từ cấm / vi phạm prefilter -> Phải bị chặn hoặc NEEDS_REVIEW / FLAG
    spam_post = {"title": "Quảng cáo", "content": "MUA BÁN acc game giảm giá 50% liên hệ zalo 0912345678"}
    print(f"-> Gửi bài spam/chứa từ cấm: {spam_post['content']}")
    
    # 3. Test bài ranh giới (Neutral/Ambiguous) -> NEEDS_REVIEW
    neutral_post = {"title": "Thắc mắc", "content": "Không biết bài tập này làm thế nào nhỉ."}
    print(f"-> Gửi bài ranh giới: {neutral_post['content']}")
    
    print("💡 Hướng dẫn kiểm tra thủ công (Mốc chốt):")
    print(" - Bật docker-compose lên.")
    print(" - Thử tắt dịch vụ AI (docker stop <ai_service_container>) và đăng bài xem trạng thái có tự chuyển về NEEDS_REVIEW không.")
    print(" - Kiểm tra Redis Cache bằng cách đăng lại chính xác một bài viết và quan sát thời gian phản hồi.")

if __name__ == "__main__":
    test_scenario()
