# Mô phỏng các API Quản trị (Admin/Moderator API Endpoints)
# Sẽ được tích hợp vào Django Views khi có source code chính thức.

class MockAuditLog:
    @staticmethod
    def log_action(admin_user, action_type, target_id, reason=""):
        # Ghi nhật ký hành động kiểm duyệt vào AuditLog
        log_entry = {
            "admin": admin_user.get("username"),
            "role": admin_user.get("role"),
            "action": action_type,
            "target_id": target_id,
            "reason": reason,
            "timestamp": "2026-10-26 15:00:00" # Sẽ dùng timezone.now() trong Django thật
        }
        print(f"[AUDIT LOG] {log_entry}")
        return log_entry

def get_needs_review_queue(user_role):
    # GET /admin/queue
    # Cả Moderator và Admin đều được xem danh sách cần duyệt
    if user_role not in ["ADMIN", "MODERATOR"]:
        return {"error": "Forbidden", "status_code": 403}
        
    # Trả về danh sách mẫu đang chờ duyệt
    return {
        "status": "success",
        "queue": [
            {"post_id": 101, "content": "Bài viết ranh giới 1", "toxic_score": 0.55, "status": "NEEDS_REVIEW"},
            {"post_id": 102, "content": "Bài viết ranh giới 2", "toxic_score": 0.42, "status": "NEEDS_REVIEW"}
        ]
    }

def moderate_post_action(user, post_id, decision, reason=""):
    # POST /admin/moderate/<id>
    # Cả Moderator và Admin đều có quyền duyệt/từ chối bài viết
    if user.get("role") not in ["ADMIN", "MODERATOR"]:
        return {"error": "Forbidden", "status_code": 403}
        
    if decision not in ["APPROVED", "REJECTED", "HIDDEN"]:
        return {"error": "Invalid decision", "status_code": 400}
        
    # Ghi nhật ký vào AuditLog
    MockAuditLog.log_action(user, f"MODERATE_{decision}", post_id, reason)
    
    return {
        "status": "success",
        "message": f"Post {post_id} đã được chuyển trạng thái thành {decision}",
        "decided_by": user.get("username"),
        "reason": reason
    }

def ban_user_action(user, target_identifier):
    # POST /admin/ban
    # PHÂN QUYỀN NGHIÊM NGẶT: Chỉ có ADMIN mới được ban, Moderator gọi sẽ bị từ chối 403
    if user.get("role") != "ADMIN":
        print(f"[SECURITY] Moderator '{user.get('username')}' cố tình gọi lệnh Ban nhưng bị từ chối!")
        return {"error": "Forbidden: Chỉ Admin mới có quyền cấm người dùng", "status_code": 403}
        
    # Ghi nhật ký ban vào AuditLog
    MockAuditLog.log_action(user, "BAN_USER", target_identifier, "Vi phạm nội quy nhiều lần")
    
    return {
        "status": "success",
        "message": f"Đã cấm thành công định danh: {target_identifier}"
    }
