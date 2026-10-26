from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import time
import random

app = FastAPI(title="AI Moderation Service - PhoBERT", version="1.0")

class TextRequest(BaseModel):
    text: str

class BatchTextRequest(BaseModel):
    texts: List[str]

@app.get("/health")
def health_check():
    return {"status": "healthy", "model_loaded": True}

@app.post("/predict")
def predict(request: TextRequest):
    start_time = time.time()
    
    # --- PHẦN NÀY SAU NÀY SẼ THAY BẰNG MODEL PHOBERT THẬT ---
    time.sleep(0.1) # Giả lập thời gian suy luận trên CPU
    toxic_keywords = ["từ_bậy", "ngu", "dốt", "spam"]
    score = 0.95 if any(word in request.text.lower() for word in toxic_keywords) else round(random.uniform(0.01, 0.3), 2)
    # --------------------------------------------------------
    
    latency_ms = (time.time() - start_time) * 1000
    
    return {
        "text": request.text,
        "toxic_score": score,
        "latency_ms": round(latency_ms, 2)
    }

@app.post("/predict/batch")
def predict_batch(request: BatchTextRequest):
    start_time = time.time()
    results = []
    
    for text in request.texts:
        score = round(random.uniform(0.01, 0.5), 2)
        results.append({"text": text, "toxic_score": score})
        
    latency_ms = (time.time() - start_time) * 1000
    return {
        "results": results,
        "total_latency_ms": round(latency_ms, 2)
    }
