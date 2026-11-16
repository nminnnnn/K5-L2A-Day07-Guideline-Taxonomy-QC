# HƯỚNG DẪN GÁN NHÃN CHUNG — GUIDELINE v1.0

- **Nhóm:** K5-L2A — Day 07
- **Phiên bản:** v1.0
- **Trạng thái:** ĐÃ THỐNG NHẤT
- **Số thành viên đồng ý:** 5/5
- **Người điều phối:** 210
- **Ngày chốt:** 16/11/2026

Toàn bộ thành viên đã thống nhất 10 class giao thông,
các quy tắc Bounding Box, xử lý che khuất,
đối tượng nhỏ, vật phản chiếu và trường hợp mơ hồ.

Guideline v1.0 được khóa để sử dụng trong quá trình
gán nhãn độc lập bằng CVAT.

## 1. Mục tiêu

Mỗi người nhìn cùng một ảnh cần biết **vật nào phải khoanh, gọi vật đó là gì và vẽ khung ở đâu**. Kết quả của 5 người sẽ được so sánh để kiểm tra mức độ nhất quán.

Cách làm đơn giản: **Nhìn vật thật → chọn đúng class → vẽ một khung ôm sát vật → chọn thuộc tính → kiểm tra lại.** Không dùng mô hình tự động gán nhãn thay cho người làm bài.

## 2. Danh sách class và thuộc tính

### 2.1. Mười class đối tượng giao thông đã thống nhất

| Tên trong CVAT | Tên dễ hiểu | Khi nào chọn | Không chọn nếu là |
|---|---|---|---|
| `person` | Người | Người thật đang đi bộ, đứng, ngồi, lái hoặc ngồi sau xe | Tượng, ma-nơ-canh, búp bê, hình người in trên bảng |
| `car` | Ô tô con | Sedan, hatchback, SUV, ô tô chở người thông thường | Bán tải thùng hở, xe buýt, xe tải |
| `motorcycle` | Xe máy | Xe số, xe tay ga, mô tô | Xe đạp không động cơ |
| `truck` | Xe tải | Xe chủ yếu chở hàng, có thùng chở hàng lớn/rõ ràng | Van thân kín liền khối, bán tải nhỏ |
| `van` | Xe van | Xe thân kín, dạng hộp, chở người hoặc hàng cỡ nhỏ | Xe buýt lớn, xe tải có thùng riêng |
| `bus` | Xe buýt / xe khách | Xe lớn thiết kế chở nhiều hành khách | Van nhỏ, ô tô con |
| `bicycle` | Xe đạp | Xe đạp thường, xe đạp thể thao | Xe máy, mô tô |
| `pickup_truck` | Xe bán tải | Xe có cabin phía trước và thùng hàng hở ở phía sau | Xe tải thùng lớn, SUV |
| `traffic_light` | Đèn tín hiệu | Cụm đèn dùng để điều khiển giao thông (đỏ/vàng/xanh) | Đèn chiếu sáng đường phố |
| `traffic_sign` | Biển báo | Biển chỉ dẫn, cấm, cảnh báo hoặc điều tiết giao thông | Biển quảng cáo, tên cửa hàng |

**`ignore_region`** là nhãn đặc biệt để chỉ **vùng được nhóm quyết định bỏ qua**, không phải một vật giao thông. Không dùng nó chỉ vì không đoán được tên một vật.

**Không gán:** nhà cửa, cây xanh, mặt đường, vỉa hè, bầu trời, ghế, đồ chơi, tượng, ma-nơ-canh, hình in và các vật khác ngoài danh sách trên. Không tự tạo class mới trong CVAT.

**Thống nhất tên class:** Mỗi đối tượng chỉ dùng đúng một tên trong cột “Tên trong CVAT”. Chẳng hạn không đổi `car` thành `automobile` hoặc `pickup_truck` thành `truck` tùy người.

### 2.2. Thuộc tính cần điền

| Thuộc tính | Cách chọn dễ hiểu |
|---|---|
| `occluded_level` | Mức vật bị **vật khác che**, chọn `0`, `1`, `2` hoặc `3` theo bảng dưới |
| `truncated` | Chọn `yes` khi vật bị **mép ảnh cắt mất một phần**; các trường hợp còn lại chọn `no` |
| `can_review` | Chọn `true` khi cần người khác kiểm tra lại class, ranh giới box hoặc quy tắc; nếu chắc chắn chọn `false` |

**Ngưỡng `occluded_level` đã thống nhất cho v1.0:**

| Mức | Quy ước dễ hiểu |
|---|---|
| `0` | Không bị vật khác che hoặc chỉ che không đáng kể |
| `1` | Bị che ít: ước tính **dưới 30%** vật |
| `2` | Bị che vừa/nhiều: ước tính **từ 30% đến dưới 70%** vật |
| `3` | Bị che rất nhiều: ước tính **từ 70% trở lên**, nhưng vẫn nhận diện đủ chắc chắn để gán |

Các ngưỡng phần trăm này là **quy ước của nhóm cho v1.0** để giảm bất đồng. Đây là ngưỡng thao tác khi ước lượng bằng mắt, không yêu cầu đo diện tích chính xác. Mọi thay đổi sau lượt gán độc lập phải được ghi ở guideline v1.1 và nhật ký calibration.

**Ví dụ:** Một người đứng sau xe hơi, thân bị che → `occluded_level` khác `0`. Một xe còn nhìn thấy một nửa vì ra khỏi mép phải ảnh → `truncated=yes` (không tự coi đây là `occluded_level` nếu không bị vật khác che).

## 3. Quy tắc vẽ Bounding Box

**R-01 — Một vật, một box:** Mỗi người, mỗi xe, mỗi biển báo/đèn là một đối tượng riêng. Không gom hai ô tô hoặc nhiều người vào cùng một box.

**R-02 — Khung ôm sát phần nhìn thấy:** Vẽ hình chữ nhật nhỏ nhất đủ bao các phần của vật mà mắt nhìn thấy. Hạn chế lấy thừa nền, người khác hoặc xe khác. Với vật bị che, không tự đoán phần hoàn toàn khuất để kéo box rộng hơn.

**R-03 — Người và xe tách nhau:** Người ngồi trên xe máy được gán `person`, chiếc xe được gán `motorcycle` bằng **hai box riêng** nếu cả hai đủ rõ. Box có thể chồng nhau vì chúng là hai vật khác nhau.

**R-04 — Vật bị che:** Gán box theo phần còn nhìn thấy và chọn `occluded_level`. Nếu không còn đủ đặc điểm để biết vật thuộc class nào, không đoán bừa; ghi vấn đề cấp ảnh và đề nghị review.

**R-05 — Vật bị cắt tại rìa ảnh:** Chỉ vẽ phần nằm trong ảnh, chọn `truncated=yes`. Không kéo box ra ngoài ranh giới ảnh.

**R-06 — Xe đỗ vẫn được gán:** Xe đang chạy hay đứng yên đều gán nếu thuộc danh sách và thấy rõ.

**R-07 — Phân biệt loại xe:** Xe bán tải cabin + thùng hở dùng `pickup_truck`; xe van thân kín liền khối dùng `van`; xe tải có thùng hàng lớn/rõ dùng `truck`; xe chở khách lớn dùng `bus`. Không gán hai class cho một chiếc xe.

**R-08 — Đèn giao thông:** Mỗi cụm đèn tín hiệu là **một box**; không vẽ riêng ô đỏ, vàng, xanh. Không lấy cả cột đèn nếu không cần thiết để bao cụm đèn.

**R-09 — Biển báo:** Vẽ box quanh **mặt biển**; không gộp cả cột đỡ. Không nhầm biển quảng cáo thành `traffic_sign`.

**R-10 — Không gán ảnh in và vật giả:** Xe trên bảng quảng cáo, xe đồ chơi, tượng người, ma-nơ-canh không được coi là xe/người thật trong cảnh.

**R-11 — Vật quá nhỏ:** Theo ngưỡng của repo, chiều cao box tối thiểu là **20 pixel**. Nếu vật thấp hơn 20 px, **không phóng box giả để đủ ngưỡng**; ghi ca để nhóm xử lý theo quy tắc QC.

**R-12 — Ảnh không có đối tượng hợp lệ:** Không vẽ box giả. Vẫn giữ ảnh trong Task và file COCO xuất ra.

**R-13 — Vật phản chiếu và ca chưa chắc:** Không gán người hoặc phương tiện chỉ xuất hiện qua gương, kính hay bề mặt phản chiếu vì đó không phải vật trực tiếp trong cảnh. Nếu chưa xác định được một vùng là vật thật hay phản chiếu, hoặc khó phân biệt van/xe tải hay ranh bị che, đánh dấu `can_review=true` trên box **nếu đã có box hợp lệ**; nếu chưa thể tạo box, ghi rõ mã ảnh, vị trí và lý do trong `submission/qc/image_issues.csv`.

**R-14 — Mỗi người làm độc lập:** Chỉ dùng guideline v1.0 đã chốt và bộ class chung. Không xem box của thành viên khác trước khi khóa bản gán độc lập.

## 4. Các ca khó cần thống nhất

| Tình huống | Quy tắc | Quyết định chung | Vì sao |
|---|---|---|---|
| Người điều khiển xe máy | R-03 | Box cho người và box cho xe riêng | Hai vật khác nhau |
| Người bị ô tô che một phần | R-02, R-04 | Box phần nhìn thấy; điền `occluded_level` | Không tự đoán phần khuất |
| Xe cắt tại mép ảnh | R-05 | Box trong ảnh; `truncated=yes` | Không vẽ ngoài ảnh |
| Xe bán tải và xe tải dễ nhầm | R-07 | Nhìn cabin và thùng hàng, chỉ chọn một class | Tránh nhãn trùng |
| Đèn đỏ-vàng-xanh cùng cụm | R-08 | Một box quanh cả cụm | Đây là một cụm tín hiệu |
| Biển quảng cáo ven đường | R-09 | Không gán `traffic_sign` | Không phải biển điều tiết giao thông |
| Ô tô in trên bảng quảng cáo | R-10 | Không gán `car` | Không phải xe thật |
| Ảnh không có class nào | R-12 | Không tạo box; vẫn giữ ảnh | Tránh box không có thật |
| Xe chỉ xuất hiện trong kính phản chiếu | R-13 | Không gán; nếu chưa chắc có phải phản chiếu thì ghi ca để review | Không phải vật trực tiếp trong cảnh, tránh đếm trùng |
| Nhiều người đứng sát nhau | R-01 | Mỗi người một box nếu phân biệt được | Tránh gộp nhiều người |

### Bằng chứng từ ảnh của bộ dữ liệu

Các ví dụ dưới đây đã được đối chiếu trực tiếp với ảnh gốc. Không lấy kết quả scan hoặc mô hình tự động làm bằng chứng nhãn đúng.

| Mã ảnh thật | Điều thấy trong ảnh | Quy tắc áp dụng | Quyết định sau khi xem | Người xác minh |
|---|---|---|---|---|
| `img_001.jpg` | Một xe bán tải thùng hở và nhiều người, có người bị xe che một phần | R-01, R-04, R-07 | Xe dùng `pickup_truck`; mỗi người nhận diện được dùng một box `person`; người bị che điền `occluded_level` theo tỷ lệ phần bị che | 210 |
| `img_003.jpg` | Người đứng hoặc ngồi gần xe đạp, xe máy; nhiều vật chồng lấn | R-01, R-03, R-04 | Mỗi người một box; xe đạp dùng `bicycle`, xe máy dùng `motorcycle`; người và xe tách box dù box có thể chồng nhau | 210 |
| `img_010.jpg` | Nhiều người ngồi trên xe máy trong khu chợ | R-01, R-03 | Mỗi người dùng một box `person`, mỗi xe dùng một box `motorcycle`; không gộp người với xe | 210 |

## 5. Kiểm tra chất lượng (QC) và quản lý phiên bản

### 5.1. Trước khi bấm lưu hoặc chuyển ảnh

- Đã khoanh đủ các đối tượng thuộc taxonomy? Không có box thừa?
- Mỗi box đúng class và ôm sát phần vật nhìn thấy?
- Đã kiểm `occluded_level`, `truncated`, `can_review`?
- Các trường hợp mơ hồ đã ghi mã ảnh và vị trí để xem lại?
- Ảnh trống vẫn còn trong Task, không thêm nhãn giả?

### 5.2. Trước khi xuất dữ liệu

Dùng **COCO 1.0**; giữ số ảnh đúng danh sách phân công. Mỗi thành viên xuất file cá nhân theo **mã ba chữ số thật**, ví dụ `210.json`, rồi chạy trình kiểm tra nhãn của repo. Không nhập nhãn mô hình tự động vào CVAT thay cho lượt gán độc lập.

Các ngưỡng kỹ thuật hiện có trong `submission/taxonomy.json` của repo: `min_box_height_px=20`, `iou_thr_large=0.85`, `iou_thr_small=0.70`, `large_px=50`, `iaa_iou=0.85`, `iaa_class=0.95`, `error_rate_img_max=0.02`, `match_iou=0.50`. **Không chỉnh mục `rules`**.

### 5.3. Chốt nhóm trước khi gán CVAT

- [x] Tất cả 5 thành viên đã nộp/khóa guideline cá nhân độc lập.
- [x] Nhóm đã đồng ý **10 class** ở Mục 2 và nhãn đặc biệt `ignore_region`.
- [x] Nhóm đã chốt bảng `occluded_level` và cách xử lý vật nhỏ / vật phản chiếu.
- [x] `submission/taxonomy.json` đã được cập nhật trùng khớp với tên class và thuộc tính trong guideline (giữ nguyên `rules`).
- [ ] Mọi người dùng cùng bộ labels được tạo từ taxonomy và cùng guideline v1.0.

### 5.4. Lịch sử thay đổi

| Phiên bản | Thay đổi | Trạng thái |
|---|---|---|
| v0 | Guideline khởi đầu của repo | Tham khảo |
| v1.0 dự thảo | Tổng hợp 5 guideline cá nhân, đề xuất 10 class và 14 quy tắc | Đã kết thúc |
| v1.0 đã chốt | Ngày 16/11/2026; mã duyệt: 119, 128, 210, 226, 232; chốt 10 class, ngưỡng che khuất 30%/70%, vật nhỏ dưới 20 px và không gán vật chỉ xuất hiện qua phản chiếu | **Đã thống nhất** |
| v1.1 | Chỉ cập nhật sau IAA/calibration, kèm lý do và ca cụ thể | Chưa thực hiện |

---

**Đường dẫn nộp:** `submission/guidelines/guideline_v1.0_agreed.md`.

**Lưu ý:** Đổi dòng trạng thái đầu tài liệu thành “ĐÃ THỐNG NHẤT” **chỉ sau khi** cả nhóm đã thật sự rà soát và đồng ý. Nếu nhóm đã bắt đầu gán theo taxonomy khác, không âm thầm thay đổi class; cần thống nhất cách chuyển đổi và ghi nhận thay đổi.
