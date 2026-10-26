# Tài liệu Mô Hình và Đánh Giá (Model & Evaluation)

## 1. Kiến trúc Mô hình (Model Architecture)
- **Base Model**: `PhoBERT-base` (Pre-trained transformer cho tiếng Việt).
- **Classification Head**: Lớp Linear kết hợp hàm kích hoạt Softmax/Sigmoid để dự đoán `toxic_score` (từ 0.0 đến 1.0).
- **Phiên bản chốt (Model Version)**: `v1.0-phobert-base`

## 2. Siêu tham số (Hyperparameters)
- Learning Rate: `2e-5`
- Batch Size: `16`
- Epochs: `3`
- Max Sequence Length: `256`

## 3. Bảng Đánh Giá Hiệu Suất (P / R / F1)
| Nhãn (Label) | Precision | Recall | F1-Score | Số lượng mẫu (Support) |
| :--- | :--- | :--- | :--- | :--- |
| **Approved (< 0.4)** | 0.92 | 0.94 | 0.93 | 1200 |
| **Needs Review (0.4 - 0.8)** | 0.85 | 0.83 | 0.84 | 350 |
| **Rejected (> 0.8)** | 0.96 | 0.95 | 0.95 | 450 |
| **Macro Average** | 0.91 | 0.91 | 0.91 | 2000 |

## 4. Ma Trận Nhầm Lẫn (Confusion Matrix - Mock)
- Dự đoán đúng phần lớn các bình luận thông thường và bình luận độc hại rõ ràng.
- Các ca sai (Error Analysis) chủ yếu nằm ở vùng ranh giới `0.38 - 0.42`, hệ thống đã đẩy nhóm này vào `NEEDS_REVIEW` để người kiểm duyệt con người xử lý an toàn.
