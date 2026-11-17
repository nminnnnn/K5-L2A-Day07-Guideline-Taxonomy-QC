
# Guideline cá nhân 128 — Kiểm tra chất lượng trước khi xuất

Người điền: mã `128`

- Phiên bản: v0.1 cá nhân (nháp đề xuất, chưa phải v1.0 nhóm)
- Ngày: 2026-11-16
- Người duyệt: mã `210`
- Phạm vi: bounding box (hình chữ nhật) cho đối tượng giao thông đường bộ

## 1. Mục tiêu

Ưu tiên dễ kiểm tra lại: cùng class, box gọn, thuộc tính đủ. Mọi quyết định chưa chắc phải có dấu vết để reviewer hiểu.

## 2. Các class đề xuất

| Class dùng trong CVAT | Giải thích đơn giản     | Ví dụ                                                                       | Dễ nhầm                                                 |
| ---------------------- | ---------------------------- | ----------------------------------------------------------------------------- | --------------------------------------------------------- |
| `person`             | Người thật                | người đi bộ, người ngồi trên xe (img_005, img_014)                    | Không phải: tượng (img_017), ma-nơ-canh (img_033)    |
| `car`                | Ô tô con                   | sedan, SUV (img_015, SUV đỏ trong img_028)                                  | Không phải: xe bán tải có thùng hàng hở (img_028) |
| `motorcycle`         | Xe máy, mô tô             | xe tay ga, xe số, xe phân khối lớn (img_005)                              | Không phải: xe đạp                                    |
| `truck`              | Xe tải chở hàng           | xe tải thùng, xe tải lớn, xe chở ô tô (img_002)                        | Không phải: xe van nhỏ, xe bán tải                   |
| `van`                | Xe van kín                  | xe giao hàng nhỏ thùng kín liền thân (van trắng trong img_005)         | Không phải: xe tải thùng rời                         |
| `bus`                | Xe buýt, xe khách          | xe buýt công cộng, xe chở khách lớn (nền img_037)                      | Không phải: xe van nhỏ                                 |
| `bicycle`            | Xe đạp                     | xe đạp thường, xe đạp thể thao                                         | Không phải: xe máy                                     |
| `pickup_truck`       | Xe bán tải                 | ô tô cabin chở người, thùng chở hàng hở phía sau (img_028, img_037) | Không phải: xe tải thùng lớn                         |
| `traffic_light`      | Đèn tín hiệu giao thông | cụm đèn đỏ/vàng/xanh điều khiển giao thông                          | Không phải: đèn đường                              |
| `traffic_sign`       | Biển báo giao thông       | biển cấm, biển cảnh báo, biển chỉ dẫn                                 | Không phải: biển quảng cáo                           |

`ignore_region` không phải vật giao thông: chỉ sử dụng theo quy tắc nhóm để khoanh vùng bỏ qua; đừng dùng thay cho nhãn khó đoán. Các vật như cây, nhà, mặt đường, đồ chơi, tượng, ma-nơ-canh không nằm trong bộ class đề xuất.

**Chú ý:** Repo gốc chỉ có 5 class đối tượng (`person`, `car`, `motorcycle`, `truck`, `van`). Năm class bổ sung (`bus`, `bicycle`, `pickup_truck`, `traffic_light`, `traffic_sign`) chỉ dùng khi cả nhóm phê duyệt taxonomy v1.0.

### Thuộc tính

- `occluded_level`: `0` = thấy rõ, `1` = bị che ít, `2` = bị che nhiều, `3` = khó nhận ra do che. **Các mức phần trăm che cụ thể phải được nhóm chốt; chưa có ngưỡng % trong nguồn.**
- `truncated`: `yes` nếu vật bị cắt ở mép ảnh, còn lại `no`.
- `can_review`: đánh dấu khi chưa chắc nhãn hoặc box, sau đó báo nhóm.

## 3. Cách vẽ box

1. Chọn đúng class cho **vật thật** trong ảnh; một vật chỉ có một class.
2. Vẽ khung gọn theo phần vật nhìn thấy; không kéo ôm nhiều đối tượng thành một khung.
3. Người trên xe và chiếc xe là hai đối tượng riêng nếu cả hai thuộc taxonomy.
4. Nếu bị che/cắt mép, gán đúng thuộc tính; nếu còn mơ hồ thì đánh dấu cần xem lại.
5. Không vẽ box cho vật ngoài danh sách; không tự đổi tên class trong CVAT.

## 4. Các tình huống cần xem kỹ

| Quy tắc nháp | Tình huống                     | Cách xử lý đề xuất (cần nhóm duyệt)                     |
| -------------- | -------------------------------- | ---------------------------------------------------------------- |
| `R-01`       | Người/xe dính nhau            | Nếu là hai vật thật, tách hai box theo từng đối tượng. |
| `R-02`       | Đối tượng bị che            | Đánh occluded_level và can_review nếu khó xác định ranh. |
| `R-03`       | Ảnh không có class đã chọn | Không vẽ box giả; vẫn giữ ảnh khi export.                  |
| `R-04`       | Xe phản chiếu qua kính        | Không tự gán; đưa vào danh sách ca cần thống nhất.     |

**Ví dụ từ ảnh thật** (đã mở xem):

| Ảnh    | Quy tắc           | Quyết định                                                                                                                                                                | Lý do                                                                                           |
| ------- | ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| img_005 | `R-01`, `R-02` | Mỗi người trên xe máy một box `person`, mỗi xe máy một box `motorcycle`; van trắng phía sau `van`, occluded_level 2.                                        | Người và xe là hai vật thật; van bị người phía trước che nhiều.                     |
| img_002 | `R-01`, `R-02` | Xe chở ô tô một box `truck`; mỗi ô tô thật trên xe một box `car` (xe tầng dưới occluded_level 1–2); người đứng bên phải `person`.                  | Các ô tô là xe thật, chỉ đang được chở.                                               |
| img_015 | `R-02`           | Xe đỏ bên trái và xe bạc bên phải `car`, truncated = yes.                                                                                                          | Xe bị cắt ở mép ảnh nhưng vẫn nhận ra là ô tô.                                        |
| img_017 | `R-03`           | Không vẽ box.                                                                                                                                                              | Tượng người cưỡi ngựa, không phải người thật.                                        |
| img_038 | `R-03`           | Không vẽ box; vẫn giữ ảnh khi export.                                                                                                                                   | Ô tô đồ chơi trong tủ kính, không phải xe thật.                                        |
| img_027 | `R-03`           | Không vẽ box.                                                                                                                                                              | Tượng đài hình xe bán tải đặt trên bệ đá trong nghĩa trang, không phải xe thật. |
| img_033 | `R-04`           | Không gán ma-nơ-canh và người trên ảnh in; phần xe (gương, cửa) bên phải nghi là phản chiếu → không tự gán, đưa vào danh sách ca cần thống nhất. | Không phải vật thật / chưa chắc là xe thật.                                              |
| img_028 | `R-02`           | Xe bán tải `pickup_truck` (nếu nhóm duyệt class này); SUV đỏ phía sau `car`, occluded_level 1; tượng ngựa không gán.                                       | Xe bán tải có thùng hàng hở, không phải `car` hay `truck` theo bảng class.          |
| img_004 | `R-03`           | Tuk-tuk không gán (ngoài danh sách); người ngồi trong xe nhìn thấy được → `person`, tick can_review nếu khó xác định ranh.                               | Tuk-tuk không thuộc bộ class đề xuất.                                                      |

File SAM3 chỉ liệt kê ảnh ứng viên, **không chứng minh nhãn trong ảnh là đúng**.

## 5. QC và lịch sử

- Kiểm lại class, khung, thuộc tính trước khi xuất COCO 1.0.
- Rà ảnh từng frame trước khi lưu — Kiểm số ảnh xuất COCO bằng danh sách được phân công (`submission/qc/assignments/232.txt`, 24 ảnh).
- Ngưỡng kỹ thuật của repo: chiều cao box tối thiểu 20 px; IoU lớn 0.85, nhỏ 0.70. Nhóm không sửa `taxonomy.json` → `rules`.
- Lịch sử: v0.1 cá nhân của 128, dựa trên bản nháp 05; chỉ ghi `v1.0` khi cả nhóm đã chốt và khóa.
