# Guideline cá nhân — Mã 119: Phân biệt các loại xe

Tài liệu ghi nhận quy tắc phân loại và gán nhãn của thành viên mã 119 ở Pha 1, làm cơ sở đối chiếu khi nhóm thống nhất guideline chung.

| Thông tin | Nội dung |
|---|---|
| Họ và tên | Nguyễn Thanh Phong |
| Mã thành viên | `119` |
| Loại tài liệu | Guideline cá nhân, Pha 1 |
| Ngày cập nhật | 16/11/2026 |
| Phiên bản | Bản cá nhân; chưa phải guideline v1.0 của nhóm |
| Phạm vi | Bounding box (hình chữ nhật) cho đối tượng giao thông đường bộ |
| Tài liệu tham chiếu | Guideline v0 và taxonomy v0 của repo |

## 1. Mục tiêu

Guideline tập trung phân biệt ô tô con, xe bán tải, van, xe tải và xe buýt. Việc chọn lớp dựa trên hình dáng và công dụng có thể nhận biết từ ảnh, nhằm tránh gán hai lớp cho cùng một xe.

## 2. Hệ thống lớp và thuộc tính

| Class dùng trong CVAT | Giải thích đơn giản     | Ví dụ                                            | Dễ nhầm                                 |
| --------------------- | ----------------------- | ------------------------------------------------ | --------------------------------------- |
| `person`              | Người thật              | người đi bộ, người ngồi trên xe                  | Không phải: tượng, ma-nơ-canh           |
| `car`                 | Ô tô con                | sedan, SUV                                       | Không phải: xe bán tải có thùng hàng hở |
| `motorcycle`          | Xe máy, mô tô           | xe tay ga, xe số, xe phân khối lớn               | Không phải: xe đạp                      |
| `truck`               | Xe tải chở hàng         | xe tải thùng, xe tải lớn                         | Không phải: xe van nhỏ, xe bán tải      |
| `van`                 | Xe van kín              | xe giao hàng nhỏ thùng kín liền thân             | Không phải: xe tải thùng rời            |
| `bus`                 | Xe buýt, xe khách       | xe buýt công cộng, xe chở khách lớn              | Không phải: xe van nhỏ                  |
| `bicycle`             | Xe đạp                  | xe đạp thường, xe đạp thể thao                   | Không phải: xe máy                      |
| `pickup_truck`        | Xe bán tải              | ô tô cabin chở người, thùng chở hàng hở phía sau | Không phải: xe tải thùng lớn            |
| `traffic_light`       | Đèn tín hiệu giao thông | cụm đèn đỏ/vàng/xanh điều khiển giao thông       | Không phải: đèn đường                   |
| `traffic_sign`        | Biển báo giao thông     | biển cấm, biển cảnh báo, biển chỉ dẫn            | Không phải: biển quảng cáo              |

`ignore_region` không phải vật giao thông. Lớp này chỉ dùng để khoanh vùng bỏ qua theo quy tắc nhóm, không dùng thay cho nhãn khó đoán. Cây, nhà, mặt đường, đồ chơi, tượng và ma-nơ-canh không thuộc các lớp đối tượng trong guideline cá nhân này.

**Phạm vi áp dụng:** Taxonomy gốc của repo có 5 lớp đối tượng (`person`, `car`, `motorcycle`, `truck`, `van`). Năm lớp bổ sung (`bus`, `bicycle`, `pickup_truck`, `traffic_light`, `traffic_sign`) là quan điểm phân loại cá nhân; chỉ đưa vào taxonomy v1.0 khi cả nhóm thống nhất.

### Thuộc tính

| Thuộc tính       | Giá trị            | Ý nghĩa                                                                                                                                                              |
| ---------------- | ------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `occluded_level` | `0`, `1`, `2`, `3` | Tỷ lệ diện tích vật bị **vật khác che** (ước lượng trên toàn bộ vật): `0` = 0%; `1` = trên 0% đến 25%; `2` = trên 25% đến 75%; `3` = trên 75% nhưng vẫn nhận ra vật. |
| `truncated`      | `no`, `yes`        | Vật bị cắt ở mép ảnh.                                                                                                                                                |
| `can_review`     | tick / không       | Tick khi chưa chắc về nhãn hoặc box để người khác xem lại.                                                                                                           |

Ước lượng phần bị che so với hình dạng đầy đủ của **chính vật đó**. Phần nằm ngoài mép ảnh tính bằng `truncated`, không cộng vào tỷ lệ che. Nếu vật bị che hoàn toàn thì không có phần nhìn thấy để vẽ box; nếu khó phân biệt mức ở ranh giới 25% hoặc 75%, chọn mức ước lượng gần nhất và tick `can_review`.

## 3. Cách vẽ box

1. Chọn đúng class cho **vật thật** trong ảnh; một vật chỉ có một class.
2. Vẽ khung gọn theo phần vật nhìn thấy; không kéo ôm nhiều đối tượng thành một khung.
3. Người trên xe và chiếc xe là hai đối tượng riêng nếu cả hai thuộc taxonomy.
4. Nếu bị che/cắt mép, gán đúng thuộc tính; nếu còn mơ hồ thì đánh dấu cần xem lại.
5. Không vẽ box cho vật ngoài danh sách; không tự đổi tên class trong CVAT.

## 4. Quy tắc xử lý các tình huống dễ nhầm

| Mã quy tắc | Tình huống          | Cách xử lý trong guideline cá nhân                    |
| ------------ | ------------------- | ------------------------------------------------------ |
| `R-01`       | Xe cabin + thùng hở | Chọn pickup_truck, không gán thêm truck cho cùng xe.   |
| `R-02`       | Xe thùng kín nhỏ    | Chọn van nếu thân xe liền khối và đúng quy tắc nhóm.   |
| `R-03`       | Xe chở khách lớn    | Chọn bus, không đổi sang van chỉ vì bị khuất một phần. |
| `R-04`       | Loại xe khó đoán    | Chọn can_review; không tạo class mới khi chưa họp.     |

**Đối chiếu ảnh thật:** Tài liệu hiện chưa ghi mã ảnh `img_0xx` kèm quyết định và lý do cho từng ví dụ. Danh sách ảnh ứng viên từ SAM3 không được xem là bằng chứng xác nhận nhãn trong ảnh.

## 5. QC và lịch sử

- Kiểm lại class, khung, thuộc tính trước khi xuất COCO 1.0.
- Mỗi phương tiện có một nhãn. Trường hợp có thể thuộc hai lớp cần được ghi lại để nhóm thống nhất.
- Ngưỡng kỹ thuật của repo: chiều cao box tối thiểu 20 px; IoU lớn 0.85, nhỏ 0.70. Nhóm không sửa `taxonomy.json` → `rules`.
- Lịch sử phiên bản: guideline cá nhân Pha 1 của mã 119. Ký hiệu `v1.0` dành cho guideline chung sau khi nhóm chốt và khóa.
