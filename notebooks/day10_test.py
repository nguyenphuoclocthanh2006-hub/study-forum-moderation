# Kiểm thử tính năng Ngày 10: Precheck tốc độ cao (<100ms) và Export Feedback
from moderation.precheck_service import precheck_content, export_feedback_to_csv
import time

def run_day10_tests():
    print("⚡ BẮT ĐẦU KIỂM THỬ TÍNH NĂNG NGÀY 10...")
    
    # 1. Test kiểm tra trước (Precheck) câu có từ khóa cấm
    test_sentence = "MUA BÁN acc game giảm giá liên hệ zalo 0912345678"
    print(f"\n--- 1. Precheck văn bản: '{test_sentence}' ---")
    result = precheck_content(test_sentence, user_id="user_test_01")
    print("Kết quả trả về:", result)
    
    # Kiểm tra điều kiện thời gian < 100ms
    if result["latency_ms"] < 100:
        print(f"✅ ĐẠT YÊU CẦU: Thời gian phản hồi là {result['latency_ms']} ms (< 100 ms).")
    else:
        print(f"⚠️ Cảnh báo: Thời gian phản hồi {result['latency_ms']} ms.")
        
    # 2. Test Rate Limiting (gửi liên tiếp 11 lần)
    print("\n--- 2. Kiểm tra Rate Limiting (10 lần/phút) ---")
    for i in range(11):
        res = precheck_content("Kiểm tra rate limit", user_id="spammer_01")
        if res.get("verdict") == "BLOCKED_RATE_LIMIT":
            print(f"✅ Rate limit hoạt động chính xác ở lần gọi thứ {i+1}: {res['message']}")
            break
            
    # 3. Test xuất file CSV Feedback
    print("\n--- 3. Kiểm tra xuất dataset feedback cho AI retraining ---")
    csv_path = export_feedback_to_csv()
    print(f"File CSV đã lưu tại: {csv_path}")

if __name__ == "__main__":
    run_day10_tests()
