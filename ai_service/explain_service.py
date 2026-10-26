# Bổ sung tính năng /explain cho AI Service (FastAPI)
# Đoạn code này tích hợp vào ai_service/app.py khi ráp nối thực tế.

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app_explain = FastAPI()

class ExplainRequest(BaseModel):
    text: str
    toxic_score: float

@app_explain.post("/explain")
def explain_decision(payload: ExplainRequest):
    ""
    Phân tích và trả về lý do/đặc trưng giải thích vì sao AI gán mức điểm toxic_score này.
    ""
    text = payload.text
    score = payload.toxic_score
    
    # Giả lập phân tích trọng số từ khóa (hoặc attention weights của PhoBERT)
    risk_factors = []
    words = text.split()
    for w in words:
        if w.lower() in ["mua", "bán", "giảm giá", "inbox", "zalo", "hotline"]:
            risk_factors.append({"word": w, "weight": 0.85})
            
    return {
        "text": text,
        "toxic_score": score,
        "explanation": {
            "summary": "Điểm độc hại dựa trên mức độ xuất hiện từ khóa thương mại/nhạy cảm.",
            "risk_factors": risk_factors if risk_factors else [{"word": "văn bản chung", "weight": score}]
        }
    }
