# Thông tin nhóm

- **Tên nhóm:** K5-L2A — Day 07
- **Mã thành viên (ba chữ số):** 119, 128, 210, 226, 232
- **Người điều phối:** 210
- **Người review bản cuối:** 210
- **Commit chốt bài:** [Điền mã commit sau khi hoàn tất]

## Kết quả tóm tắt

- **Lượt phân công hoàn tất / được giao:** **120/120** (5 thành viên, mỗi thành viên phụ trách 24 ảnh). Theo kế hoạch 3 lượt gán/ảnh, tổng số lượt annotation tương ứng là **360**, cần đối chiếu log để xác nhận đã hoàn thành đầy đủ.

- **IAA trước calibration (kèm mẫu số):** IoU trung bình **[cần xác minh]**, tỷ lệ cùng lớp **[cần xác minh]**, trên **2.169 cặp bbox ghép [cần đối chiếu log]**. Các chỉ số cần được tính từ kết quả annotation thực tế trước calibration.

- **Số ảnh phải calibration:** **0/40** theo candidate tự động. Ngoài ra, **8 ảnh** có chỉnh sửa QC nguồn được ghi nhận trong `source_corrections.json` trước khi tổng hợp bản cuối. Các chỉnh sửa này được theo dõi riêng với candidate calibration.

- **Vòng QC và số ảnh đã duyệt / cả lô:** Vòng **1**, đã duyệt **40/40 ảnh (100%)**.

- **Tỷ lệ lỗi theo ảnh:** **2.5% (1/40 ảnh)**.

- **Tỷ lệ lỗi theo đối tượng:** **0.6% (4/723 đối tượng)**.

- **Số vật thể bỏ sót trong phiếu QC:** **0**.

- **Quyết định: REWORK — chấp nhận bản trung gian.** Nhóm giữ lại kết quả hiện tại làm cơ sở cho vòng chỉnh sửa tiếp theo. Thuộc tính `occluded_level` cần được rà soát trên toàn bộ 40 ảnh, cập nhật các lỗi phát hiện và thực hiện QC lại trước khi quyết định phát hành chính thức.