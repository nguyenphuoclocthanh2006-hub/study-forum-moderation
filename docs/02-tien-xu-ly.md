# Tài liệu Tiền Xử Lý Dữ Liệu (Preprocessing)

## 1. Các bước tiền xử lý văn bản
- **Chuẩn hóa Unicode**: Đưa toàn bộ về chuẩn NFC.
- **Chuyển chữ thường (Lowercase)**: Đồng nhất chữ hoa và chữ thường.
- **Loại bỏ khoảng trắng thừa**: Gom nhiều khoảng trắng liên tiếp thành 1 khoảng trắng duy nhất.
- **Tiền lọc luật (Prefilter)**: Phát hiện nhanh số điện thoại, đường link độc hại hoặc từ khóa quảng cáo cấm.

## 2. Ví dụ Trước và Sau khi tiền xử lý
| Trước khi xử lý (Raw Text) | Sau khi tiền xử lý (Normalized Text) | Ghi chú |
| :--- | :--- | :--- |
| `  MUA BÁN Acc game LÊN ĐỜI GIẢM GIÁ 50% tại https://example.com !!! ` | `mua bán acc game lên đời giảm giá 50% tại https://example.com` | Bị lọc bởi Prefilter (FLAG) |
| `Hôm nay học môn Cấu trúc dữ liệu rất hay.  ` | `hôm nay học môn cấu trúc dữ liệu rất hay.` | Văn bản chuẩn, đưa vào AI model |
