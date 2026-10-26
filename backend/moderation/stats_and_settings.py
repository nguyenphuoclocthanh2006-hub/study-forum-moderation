# Quản lý Thống kê, Giải thích và Cấu hình động (Ngày 9)

# Giả lập Database lưu trữ Setting động (Ngưỡng duyệt bài)
# Mặc định: APPROVED < 0.4, REJECTED > 0.8
SYSTEM_SETTINGS = {
    "low_threshold": 0.4,
    "high_threshold": 0.8
}

def get_system_settings():
    # Lấy ngưỡng mới nhất từ DB/Redis
    return SYSTEM_SETTINGS

def update_system_settings(new_low, new_high, admin_user):
    # PUT /admin/settings: Thay đổi ngưỡng động không cần restart
    if admin_user.get("role") != "ADMIN":
        return {"error": "Forbidden: Chỉ Admin mới được đổi cấu hình hệ thống", "status_code": 403}
        
    SYSTEM_SETTINGS["low_threshold"] = float(new_low)
    SYSTEM_SETTINGS["high_threshold"] = float(new_high)
    
    print(f"[DYNAMIC CONFIG] Admin {admin_user.get('username')} đã đổi ngưỡng thành: Low={new_low}, High={new_high}")
    return {
        "status": "success",
        "message": "Đã cập nhật ngưỡng thành công! Áp dụng ngay cho các bài mới.",
        "settings": SYSTEM_SETTINGS
    }

def get_admin_stats(user_role):
    # GET /admin/stats: Thống kê tổng quan
    if user_role not in ["ADMIN", "MODERATOR"]:
        return {"error": "Forbidden", "status_code": 403}
        
    # Dữ liệu thống kê mẫu
    return {
        "status": "success",
        "total_posts": 1540,
        "status_breakdown": {
            "APPROVED": 1100,
            "NEEDS_REVIEW": 280,
            "REJECTED": 160
        },
        "daily_stats": [
            {"date": "2026-10-24", "count": 450},
            {"date": "2026-10-25", "count": 520},
            {"date": "2026-10-26", "count": 570}
        ],
        "top_violations": [
            {"keyword": "mua bán", "count": 85},
            {"keyword": "giảm giá", "count": 64},
            {"keyword": "inbox zalo", "count": 42}
        ]
    }

def explain_post_decision(post_id, user_role):
    # GET /admin/queue/<id>/explain: Gọi khi quản trị viên mở xem chi tiết bài
    if user_role not in ["ADMIN", "MODERATOR"]:
        return {"error": "Forbidden", "status_code": 403}
        
    # Giả lập kết quả giải thích cho bài viết
    return {
        "post_id": post_id,
        "ai_explanation": {
            "summary": "Bài viết chứa cụm từ nhạy cảm có trọng số ảnh hưởng lớn tới điểm độc hại.",
            "confidence": 0.89,
            "key_contributors": ["mua bán", "zalo"]
        }
    }
