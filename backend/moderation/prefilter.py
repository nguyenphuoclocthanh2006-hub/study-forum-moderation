import re

def prefilter_text(text: str) -> dict:
    # Tiền lọc bài viết dựa trên luật (Rule-based prefilter):
    # - Phát hiện số điện thoại.
    # - Phát hiện đường dẫn (URL/Link).
    # - Phát hiện từ khóa quảng cáo nhạy cảm.
    # Nếu vi phạm -> Trả về trạng thái FLAG.
    
    if not text:
        return {"status": "PASS"}

    text_lower = text.lower()
    
    # 1. Danh sách từ khóa quảng cáo / spam thường gặp
    ad_keywords = ["liên hệ", "hộp thư đến", "giảm giá", "inbox", "khuyến mãi", "zalo", "hotline", "mua bán", "tuyển dụng"]
    found_keywords = [kw for kw in ad_keywords if kw in text_lower]
    
    # 2. Kiểm tra số điện thoại Việt Nam (03, 05, 07, 08, 09 hoặc +84)
    phone_pattern = r'(\+84|0[35789])[0-9]{8}'
    has_phone = bool(re.search(phone_pattern, text))
    
    # 3. Kiểm tra đường dẫn website / link
    url_pattern = r'https?://\S+|www\.\S+'
    has_link = bool(re.search(url_pattern, text))
    
    # Đánh giá vi phạm
    if found_keywords or has_phone or has_link:
        reasons = []
        if found_keywords: reasons.append(f"Từ khóa quảng cáo: {found_keywords}")
        if has_phone: reasons.append("Chứa số điện thoại")
        if has_link: reasons.append("Chứa đường dẫn ngoài")
        
        return {
            "status": "FLAG",
            "reason": "; ".join(reasons)
        }
        
    return {"status": "PASS"}
