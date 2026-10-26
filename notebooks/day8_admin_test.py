# Kiểm thử phân quyền và tính năng quản trị Ngày 8
from moderation.admin_views import get_needs_review_queue, moderate_post_action, ban_user_action

def run_day8_tests():
    print("🛡️ BẮT ĐẦU KIỂM THỬ QUẢN TRỊ VÀ PHÂN QUYỀN (NGÀY 8)...")
    
    mod_user = {"username": "mod_thanh", "role": "MODERATOR"}
    admin_user = {"username": "admin_boss", "role": "ADMIN"}
    
    # 1. Test Moderator xem hàng đợi (Phải thành công)
    print("\n--- Test 1: Moderator xem danh sách cần duyệt ---")
    res = get_needs_review_queue(mod_user["role"])
    print("Kết quả:", res)
    
    # 2. Test Moderator duyệt bài (Phải thành công)
    print("\n--- Test 2: Moderator duyệt bài viết #101 ---")
    res = moderate_post_action(mod_user, 101, "APPROVED", "Bài viết hợp lệ sau khi xem xét")
    print("Kết quả:", res)
    
    # 3. Test Moderator CỐ TÌNH gọi lệnh BAN (Phải bị từ chối 403)
    print("\n--- Test 3: Moderator gọi lệnh BAN (Mong đợi bị từ chối 403) ---")
    res = ban_user_action(mod_user, "ip_192.168.1.50")
    print("Kết quả:", res)
    
    # 4. Test ADMIN gọi lệnh BAN (Phải thành công)
    print("\n--- Test 4: Admin thực hiện lệnh BAN ---")
    res = ban_user_action(admin_user, "ip_192.168.1.50")
    print("Kết quả:", res)

if __name__ == "__main__":
    run_day8_tests()
