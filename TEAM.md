# Thông tin nhóm

- Tên nhóm: K5-L2A — Day 07
- Mã thành viên (ba chữ số): 119, 128, 210, 226, 232
- Người điều phối: 210
- Người review bản cuối: 210
- Commit chốt bài (điền ở kênh nộp sau khi commit):

## Kết quả tóm tắt (điền cuối bài)

- Lượt gán hoàn tất / được giao: **120/120** (5 mã thành viên, 24 ảnh/mã, 3 lượt/ảnh).
- IAA trước calibration (kèm mẫu số): IoU TB **1.000**, cùng lớp **100.0%**, trên **2169 cặp box ghép**.
- Số ảnh phải calibration: **0/40** theo candidate tự động; 8 ảnh có sửa QC nguồn được truy vết trong `source_corrections.json` trước khi dựng bản cuối.
- Vòng QC và số ảnh đã duyệt / cả lô: vòng **1**, duyệt **40/40** ảnh.
- Tỉ lệ lỗi: **2.5% theo ảnh (1/40)**, **0.6% theo đối tượng (4/723)**; vật bỏ sót trong phiếu: **0**.
- **Quyết định: Rework (đã chấp nhận làm bản trung gian)** — giữ nguyên toàn bộ kết quả hiện tại để tiếp tục công việc; việc rà `occluded_level` trên toàn lô được chuyển sang vòng sửa tiếp theo trước khi phát hành chính thức.
