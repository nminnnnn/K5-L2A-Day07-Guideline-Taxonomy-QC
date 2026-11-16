# Guideline cá nhân 04 — Chú ý biển báo và đèn đường

Người điền: Lương Văn Quyến Mã sinh viên: 2A202603226

- Phiên bản: nháp đề xuất (chưa phải v1.0 nhóm)
- Người duyệt: 232
- Phạm vi: bounding box (hình chữ nhật) cho đối tượng giao thông đường bộ

## 1. Mục tiêu

Chỉ chọn các vật liên quan điều khiển và hướng dẫn giao thông. Hai nhãn dễ nhầm nhất là traffic_light và traffic_sign.

## 2. Các class đề xuất

| Class dùng trong CVAT | Giải thích đơn giản | Ví dụ | Dễ nhầm |
|---|---|---|---|
| `person` | Người thật | người đi bộ, người ngồi trên xe | Không phải: tượng, ma-nơ-canh |
| `car` | Ô tô con | sedan, SUV | Không phải: xe bán tải có thùng hàng hở |
| `motorcycle` | Xe máy, mô tô | xe tay ga, xe số, xe phân khối lớn | Không phải: xe đạp |
| `truck` | Xe tải chở hàng | xe tải thùng, xe tải lớn | Không phải: xe van nhỏ, xe bán tải |
| `van` | Xe van kín | xe giao hàng nhỏ thùng kín liền thân | Không phải: xe tải thùng rời |
| `bus` | Xe buýt, xe khách | xe buýt công cộng, xe chở khách lớn | Không phải: xe van nhỏ |
| `bicycle` | Xe đạp | xe đạp thường, xe đạp thể thao | Không phải: xe máy |
| `pickup_truck` | Xe bán tải | ô tô cabin chở người, thùng chở hàng hở phía sau | Không phải: xe tải thùng lớn |
| `traffic_light` | Đèn tín hiệu giao thông | cụm đèn đỏ/vàng/xanh điều khiển giao thông | Không phải: đèn đường |
| `traffic_sign` | Biển báo giao thông | biển cấm, biển cảnh báo, biển chỉ dẫn | Không phải: biển quảng cáo |

`ignore_region` không phải vật giao thông: chỉ sử dụng theo quy tắc nhóm để khoanh vùng bỏ qua; đừng dùng thay cho nhãn khó đoán. Các vật như cây, nhà, mặt đường, đồ chơi, tượng, ma-nơ-canh không nằm trong bộ class đề xuất.

**Chú ý:** Repo gốc chỉ có 5 class đối tượng (`person`, `car`, `motorcycle`, `truck`, `van`). Năm class bổ sung (`bus`, `bicycle`, `pickup_truck`, `traffic_light`, `traffic_sign`) chỉ dùng khi cả nhóm phê duyệt taxonomy v1.0.

### Thuộc tính

- `occluded_level`: `0` = thấy rõ, `1` = bị che ít(< 20%), `2` = bị che nhiều(trong khoảng >40%), `3` = khó nhận ra do che(>70%). **Các mức phần trăm che cụ thể phải được nhóm chốt; chưa có ngưỡng % trong nguồn.**
- `truncated`: `yes` nếu vật bị cắt ở mép ảnh, còn lại `no`.
- `can_review`: đánh dấu khi chưa chắc nhãn hoặc box, sau đó báo nhóm.

## 3. Cách vẽ box

1. Chọn đúng class cho **vật thật** trong ảnh; một vật chỉ có một class.
2. Vẽ khung gọn theo phần vật nhìn thấy; không kéo ôm nhiều đối tượng thành một khung.
3. Người trên xe và chiếc xe là hai đối tượng riêng nếu cả hai thuộc taxonomy.
4. Nếu bị che/cắt mép, gán đúng thuộc tính; nếu còn mơ hồ thì đánh dấu cần xem lại.
5. Không vẽ box cho vật ngoài danh sách; không tự đổi tên class trong CVAT.

## 4. Các tình huống cần xem kỹ

| Quy tắc nháp | Tình huống | Cách xử lý đề xuất (cần nhóm duyệt) |
|---|---|---|
| `R-01` | Đèn giao thông | Đánh cả cụm đèn tín hiệu, không tách 3 màu thành 3 box. |
| `R-02` | Biển báo giao thông | Đánh phần mặt biển báo; không gộp cả cột đỡ nếu nhóm không quy định. |
| `R-03` | Đèn chiếu sáng đường | Không gán traffic_light cho đèn đường. |
| `R-04` | Biển quảng cáo cạnh đường | Không gán traffic_sign nếu không phải biển giao thông. |

**Ví dụ từ ảnh thật:** [thành viên tự điền ít nhất 2 mã `img_0xx` đã mở xem, quyết định và lý do]. File SAM3 chỉ liệt kê ảnh ứng viên, **không chứng minh nhãn trong ảnh là đúng**.

## 5. QC và lịch sử

- Kiểm lại class, khung, thuộc tính trước khi xuất COCO 1.0.
- Kiểm lại nhãn công trình ven đường — Không thêm road/sidewalk vì bài này dùng box cho đối tượng phổ biến.
- Ngưỡng kỹ thuật của repo: chiều cao box tối thiểu 20 px; IoU lớn 0.85, nhỏ 0.70. Nhóm không sửa `taxonomy.json` → `rules`.
- Lịch sử: bản nháp 04; chỉ ghi `v1.0` khi cả nhóm đã chốt và khóa.
