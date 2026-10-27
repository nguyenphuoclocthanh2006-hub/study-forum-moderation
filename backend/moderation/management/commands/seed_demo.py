import time
import random

def run_seeding():
    print("🌱 BẮT ĐẦU SEEDING DỮ LIỆU DEMO CHO HỆ THỐNG...")
    
    accounts = [
        {"username": "admin_master", "role": "ADMIN"},
        {"username": "mod_thanh", "role": "MODERATOR"},
        {"username": "student_user1", "role": "USER"},
        {"username": "student_user2", "role": "USER"}
    ]
    print(f"✅ Đã khởi tạo {len(accounts)} tài khoản mẫu (Admin, Mod, User).")
    
    categories = [
        {"status": "CLEAN", "label": "Bài viết học tập sạch", "samples": [
            "Thảo luận về đồ án tốt nghiệp ngành Công nghệ thông tin tại CTUT.",
            "Xin tài liệu ôn tập môn Cấu trúc dữ liệu và giải thuật.",
            "Lịch học phần Lập trình Web nâng cao thay đổi vào thứ Hai tuần sau.",
            "Chia sẻ kinh nghiệm làm đồ án bằng Django và FastAPI.",
            "Có ai tham gia câu lạc bộ IT sắp tới không ạ?"
        ]},
        {"status": "FLAG", "label": "Bài vào hàng chờ (Cần AI/Mod xem xét)", "samples": [
            "Cách kiếm tiền nhanh chóng tại nhà không cần vốn.",
            "Đăng ký khóa học đầu tư tài chính lợi nhuận 50%/tháng.",
            "Review địa chỉ mua bán điện thoại cũ giá rẻ uy tín.",
            "Cần tuyển cộng tác viên đăng tin online lương cao.",
            "Mẹo vượt qua kỳ thi sát hạch mà không cần học nhiều."
        ]},
        {"status": "REJECTED_PREFILTER", "label": "Bài bị chặn ngay lập tức (Pre-filter)", "samples": [
            "Mua bán acc game giảm giá siêu rẻ qua zalo 0912345678",
            "spam_ads dịch vụ tăng tương tác facebook",
            "lừa_đảo chuyển tiền nhận ngay hoa hồng khủng",
            "tục_tỉu_1 nội dung vi phạm tiêu chuẩn cộng đồng",
            "Bán đề thi trúng tủ liên hệ số điện thoại lạ"
        ]},
        {"status": "PENDING_AI", "label": "Bài chờ AI xử lý bất đồng bộ", "samples": [
            "Hệ thống kiểm duyệt này hoạt động như thế nào vậy mọi người?",
            "Đánh giá chất lượng dịch vụ của trường Đại học Kỹ thuật - Công nghệ Cần Thơ.",
            "Tìm bạn cùng nhóm làm đề tài AI nhận diện hình ảnh.",
            "Xin ý kiến về việc sử dụng Redis trong kiến trúc microservices.",
            "Làm sao để tối ưu độ trễ API dưới 100ms?"
        ]}
    ]
    
    total_posts = 0
    demo_database = []
    
    for cat in categories:
        for i in range(10):
            text = random.choice(cat["samples"]) + f" (ID: {total_posts+1})"
            post = {
                "id": total_posts + 1,
                "author": random.choice(accounts)["username"],
                "content": text,
                "expected_status": cat["status"],
                "category_desc": cat["label"]
            }
            demo_database.append(post)
            total_posts += 1
            
    print(f"✅ Đã tạo thành công {total_posts} bài viết mẫu phân bổ đều cho 4 trạng thái!")
    print("--- MẪU TEST DÙNG CHO DEMO TRỰC TIẾP ---")
    print("1. Câu sạch: Thảo luận về đồ án tốt nghiệp ngành Công nghệ thông tin tại CTUT.")
    print("2. Câu có từ cấm: Mua bán acc game giảm giá siêu rẻ qua zalo")
    print("3. Câu xúc phạm không từ cấm: Mấy bạn làm bài kiểu này thì đừng bao giờ đi làm nữa cho rộng đất.")
    print("4. Câu viết né: M.u.a b.á.n a.c.c g.a.m.e giá rẻ kịch sàn")
    
    return demo_database

if __name__ == "__main__":
    run_seeding()
