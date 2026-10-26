# Kiểm thử tính năng Ngày 9: Thống kê, Giải thích và Ngưỡng động
from moderation.stats_and_settings import get_system_settings, update_system_settings, get_admin_stats, explain_post_decision

def run_day9_tests():
    print("🧪 BẮT ĐẦU KIỂM THỬ TÍNH NĂNG NGÀY 9...")
    
    admin = {"username": "admin_boss", "role": "ADMIN"}
    mod = {"username": "mod_thanh", "role": "MODERATOR"}
    
    # 1. Kiểm tra ngưỡng ban đầu
    print("\n--- 1. Kiểm tra ngưỡng cấu hình hiện tại ---")
    print(get_system_settings())
    
    # 2. Thay đổi ngưỡng trực tiếp qua API (Dynamic Config)
    print("\n--- 2. Admin thay đổi ngưỡng thành Low=0.3, High=0.7 ---")
    res = update_system_settings(0.3, 0.7, admin)
    print(res)
    print("Ngưỡng mới sau khi đổi:", get_system_settings())
    
    # 3. Kiểm tra API Thống kê
    print("\n--- 3. Kiểm tra API Thống kê (/admin/stats) ---")
    print(get_admin_stats(mod["role"]))
    
    # 4. Kiểm tra API Giải thích bài viết (/admin/queue/<id>/explain)
    print("\n--- 4. Kiểm tra API Giải thích bài viết #101 ---")
    print(explain_post_decision(101, mod["role"]))

if __name__ == "__main__":
    run_day9_tests()
