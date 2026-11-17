# Báo cáo QC — K5-L2A Day 07

## 1. Mục đích, dữ liệu và phiên bản

- Mục đích và giới hạn sử dụng: Đặc tả và QC nhãn bounding box 2D cho 40 ảnh đường phố của Day 07; bộ ảnh dùng cho thực hành ca biên, không đại diện đầy đủ cho dữ liệu vận hành.
- Nguồn và phép sử dụng dữ liệu: Ghi công, tác giả, giấy phép và URL nằm trong `data/ATTRIBUTION.csv` và được chép vào manifest.
- Manifest và checksum nhãn cuối: `submission/qc/batch_manifest.json`; `labels_calibrated.json` SHA-256 `d6f27868dcdc5d66867229b464d9ff3d8535d0d3cbe6499cf6771ad7a91b331f`.
- Guideline và taxonomy khi gán / khi bàn giao: taxonomy `v1.0`; bàn giao với `guideline_v1.1_calibrated.md`, giữ nguyên nghĩa v1.0 sau IAA và bổ sung truy vết sửa nguồn.

Năm file nhãn thành viên được tách theo `assignment.csv` từ COCO trong `kq.zip`, chuẩn hóa `tuktuk` thành `tuk_tuk`, cắt box về biên ảnh và áp dụng bảng sửa `source_corrections.json`. Vì các file có chung nguồn, IAA đo tính nhất quán sau phân phối; QC bằng mắt là bằng chứng chính để phát hiện lỗi chung.

## 2. Phân công và đồng thuận trước calibration

- Lượt hoàn thành / được giao: **120/120** lượt; 40/40 ảnh có đúng 3 mã gán.
- Số cặp box ghép, IoU TB, đồng thuận lớp và mẫu số: **2169** cặp; IoU TB **1.000**; cùng lớp **100.0%**.
- Box chưa ghép, loại do ignore, bất đồng vùng ignore: **0/0** box chưa ghép; **0** cặp loại do ignore; **0** bất đồng vùng ignore.
- Ca hai người có thể cùng sai sau khi đối chiếu tham chiếu: `img_001.jpg`, thuộc tính che khuất cùng mang giá trị mặc định `0`; `img_038.jpg`, box ô tô đồ chơi từng xuất hiện giống nhau trong nguồn và đã được loại theo R-10.

QC trực quan nguồn đã sửa 8 ảnh: thêm xe bán tải ở `img_001`, thêm hai người lái ở `img_004`, đổi class xe giữa ở `img_007`, loại hình in/phản chiếu/đồ chơi ở `img_018`, `img_020`, `img_030`, `img_033`, `img_038`. Tổng cộng loại 52 annotation nguồn, đổi lớp 1 và thêm 3; mọi ID và lý do nằm trong `source_corrections.json`.

## 3. Calibration và kiểm lại

- Ca đã xử lý, rule ID, bản sửa và người xác nhận: candidate tự động **0**; `calibration_decisions.csv` giữ header. Các sửa nguồn dẫn R-03, R-07, R-10, R-13, R-15 và được rà bằng ảnh gốc/overlay bởi mã 210.
- Tác động v1.1 lên nhãn và ảnh: Không đổi nghĩa taxonomy sau IAA; v1.1 bổ sung lịch sử truy vết. Bản cuối có 40 ảnh và 724 annotation, gồm 723 đối tượng và 1 `ignore_region`.
- Tham chiếu bằng chứng khi Rework: vòng 1 tại `submission/qc/reviews/round-01/`; bốn dòng lỗi thuộc tính trên `img_001.jpg` dẫn trực tiếp object ID 2, 3, 4, 7 và R-04.

## 4. Kết quả duyệt

- Vòng QC: 1
- Người review và ngày: 210, 17/11/2026
- Đã duyệt / cả lô: **40/40** ảnh.
- Ảnh lỗi / ảnh đã duyệt: **1/40 = 2.5%**.
- Annotation đối tượng hiện có bị lỗi / annotation đối tượng đã duyệt: **4/723 = 0.6%**.
- Vật bỏ sót, ảnh và vùng: **0** trong phiếu vòng 1 sau khi áp dụng sửa nguồn.
- Ca khó / phần còn lại, lỗi lặp và ví dụ: `sai_thuoc_tinh` lặp 4 lần trên `img_001.jpg`; nguồn đặt `occluded_level=0` cho các người có phần thân bị bàn hoặc người khác che.
- Một lỗi máy chặn được và một lỗi cần người đọc ảnh: máy chặn box vượt biên/tên class ngoài taxonomy; người đọc ảnh phát hiện hình in, phản chiếu, đồ chơi và mức che khuất sai.

## 5. Quyết định bàn giao

- Quyết định: Rework
- Lý do, người nhận và phạm vi sử dụng: Tỷ lệ ảnh lỗi 1/40 = 2.5% vượt ngưỡng 2%, đồng thời lỗi thuộc tính lặp. Toàn bộ kết quả hiện tại được chấp nhận làm bản trung gian phục vụ tiếp tục xử lý và làm bằng chứng cho vòng sửa sau; trạng thái kỹ thuật vẫn là Rework.
- Nếu còn việc: Việc rà `occluded_level` trên toàn bộ 723 đối tượng được hoãn sang vòng tiếp theo. Khi thực hiện, sửa bốn object đã ghi và các ca cùng loại, chạy lại `build_final.py`, mở vòng QC 2 và giữ nguyên toàn bộ bằng chứng vòng 1.
- Kiểm ngược từ báo cáo tới ảnh, rule và nhãn: `img_001.jpg` → R-04 → object ID 2/3/4/7 trong `labels_snapshot.json` và `qc_review.csv`; kết quả vòng 1 là REWORK.
