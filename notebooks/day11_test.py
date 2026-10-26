# Kiểm thử tính năng Ngày 11: Bảo mật, Từ cấm động, Rate limit và SQLi
from moderation.security_and_banned_words import (
    manage_banned_word, 
    get_cached_banned_words, 
    validate_and_sanitize_input, 
    check_rate_limit
)

def run_day11_tests():
    print("🛡️ BẮT ĐẦU KIỂM THỬ BẢO MẬT & TỪ CẤM (NGÀY 11)...")
    
    # 1. Test Phân quyền Admin endpoint (Guest gọi -> 401/403)
    print("\n--- 1. Kiểm tra phân quyền Admin (Guest vs Admin) ---")
    guest_res = manage_banned_word("add", word="hacker_word", user_role="GUEST")
    print("Guest gọi API quản lý từ cấm:", guest_res)
    assert guest_res.get("status_code") == 403, "Phải trả về 403 Forbidden!"
    print("✅ Phân quyền Admin hoạt động chuẩn xác!")
    
    # 2. Test thêm từ cấm mới và chặn ngay lập tức (Tiêu chí Ngày 11)
    print("\n--- 2. Thêm từ cấm mới qua API và kiểm tra chặn ngay ---")
    print("Danh sách từ cấm trước khi thêm:", get_cached_banned_words())
    
    # Admin thêm từ cấm mới "casino_online"
    manage_banned_word("add", word="casino_online", user_role="ADMIN")
    print("Danh sách từ cấm sau khi thêm:", get_cached_banned_words())
    
    # Thử kiểm tra văn bản chứa từ cấm vừa thêm
    test_content = "Tham gia ngay casino_online nhận thưởng lớn"
    validation = validate_and_sanitize_input(test_content)
    print("Kết quả kiểm tra văn bản chứa từ cấm:", validation)
    if validation.get("blocked"):
        print("✅ THÀNH CÔNG: Từ cấm mới được áp dụng và chặn ngay lập tức!")
        
    # 3. Test bảo mật chống SQL Injection trong ô nhập liệu
    print("\n--- 3. Kiểm tra chống SQL Injection ---")
    sqli_input = "admin' OR 1=1 --"
    sqli_res = validate_and_sanitize_input(sqli_input)
    print("Kết quả kiểm tra SQLi:", sqli_res)
    if sqli_res.get("security_alert"):
        print("✅ THÀNH CÔNG: Đã phát hiện và ngăn chặn mã độc SQL Injection!")
        
    # 4. Test Rate Limiting (Vượt quá giới hạn trả về 429)
    print("\n--- 4. Kiểm tra Rate Limiting (5 bài/phút) ---")
    user_token = "anon_token_xyz"
    for i in range(6):
        is_limited = check_rate_limit(user_token, max_calls=5, window_seconds=60)
        if is_limited:
            print(f"✅ THÀNH CÔNG: Vượt giới hạn ở lần gọi thứ {i+1}, hệ thống trả về mã lỗi 429 Too Many Requests!")
            break

if __name__ == "__main__":
    run_day11_tests()
