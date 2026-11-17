# Guideline cá nhân 232 — Vẽ box rõ và nhất quán

- Phiên bản: cá nhân 232 — lần 1
- Mã thành viên: 232
- Phạm vi: bounding box cho đối tượng giao thông đường bộ

## 1. Mục tiêu

Tôi sử dụng guideline này để chọn class, vẽ box và ghi thuộc tính nhất quán. Box bám sát phần vật nhìn thấy. Tôi xác định class theo hình dạng và chức năng của vật, không dựa riêng vào màu sắc.

## 2. Class và thuộc tính

### Class

| Class | Định nghĩa | Ví dụ | Không thuộc class |
|---|---|---|---|
| `person` | Người thật, gồm người đi bộ và người ngồi trên xe | Người đi bộ, người lái xe máy | Tượng, ma-nơ-canh, hình in |
| `car` | Ô tô con chở người | Sedan, SUV | Xe bán tải có thùng hàng hở |
| `motorcycle` | Xe máy, mô tô | Xe tay ga, xe số | Xe đạp |
| `truck` | Xe tải chở hàng có thùng hàng riêng | Xe tải thùng, xe tải lớn | Xe van nhỏ, xe bán tải |
| `van` | Xe van nhỏ, khoang hàng kín liền thân | Xe giao hàng nhỏ | Xe tải thùng rời |
| `bus` | Xe buýt, xe khách cỡ lớn | Xe buýt công cộng | Xe van nhỏ |
| `bicycle` | Xe đạp | Xe đạp thường, xe đạp thể thao | Xe máy |
| `pickup_truck` | Xe bán tải có cabin và thùng chở hàng hở phía sau | Xe bán tải | Xe tải thùng lớn |
| `traffic_light` | Đèn tín hiệu điều khiển giao thông | Cụm đèn đỏ, vàng, xanh | Đèn đường |
| `traffic_sign` | Biển báo điều khiển hoặc hướng dẫn giao thông | Biển cấm, cảnh báo, chỉ dẫn | Biển quảng cáo |

Tôi không gán class đối tượng cho cây, nhà, mặt đường, đồ chơi, tượng và ma-nơ-canh. `ignore_region` là vùng bỏ qua, không phải class vật thể và không dùng thay cho class chưa xác định.

Báo cáo cá nhân sử dụng bộ 10 class ở bảng trên. Task CVAT hiện có 5 class đối tượng của repo gốc: `person`, `car`, `motorcycle`, `truck`, `van`. Việc thống nhất taxonomy và guideline chung được thực hiện riêng cùng nhóm; tài liệu này không thay đổi cấu hình Task hiện tại.

### Thuộc tính `occluded_level`

| Giá trị | Ý nghĩa | Quy tắc xác định |
|---|---|---|
| `0` | Thấy rõ | Không bị vật khác che. |
| `1` | Bị che ít | Phần bị che trên 0% đến 25% diện tích hình dáng đầy đủ ước lượng của đối tượng. |
| `2` | Bị che nhiều | Phần bị che trên 25%; vẫn đủ bằng chứng xác định mức che và nhận diện class. |
| `3` | Không rõ | Không đủ bằng chứng để xác định mức che; đặt thêm `can_review=true`. |

Tôi dùng mốc 25% để phân biệt che ít và che nhiều. Đúng 25% ghi mức `1`; trên 25% ghi mức `2`. Mức `3` thể hiện không rõ mức che, không đồng nghĩa với che trên 75%.

Tỷ lệ che được ước lượng theo phần hình dáng bị vật khác chắn so với hình dáng đầy đủ của chính đối tượng. Không dùng số px cố định hoặc tỷ lệ diện tích box. Với người, xét tổng thể đầu, thân, tay và chân; không dùng tỷ lệ chiều cao thay cho tỷ lệ diện tích.

Phần nằm ngoài khung ảnh không tính vào mức che. Người ngồi trên xe có chân bị xe chắn được tính là che khuất; chân co lại do tư thế không tự động tính là bị che. Không vẽ thêm phần khuất để tính tỷ lệ.

### Thuộc tính `truncated`

- `yes`: đối tượng bị cắt ở mép ảnh.
- `no`: đối tượng không bị cắt ở mép ảnh.

Đối tượng bị cắt mép nhưng phần còn trong ảnh không bị vật khác chắn được ghi `truncated=yes`, `occluded_level=0`.

### Thuộc tính `can_review`

- `true`: chưa chắc class, ranh giới box hoặc mức che.
- `false`: xác định được class, box và mức che theo guideline.

Nếu chưa thể vẽ box, tôi ghi vấn đề cấp ảnh gồm tên ảnh, mã thành viên, vùng ảnh và lý do. Cờ occluded mặc định của CVAT không thay thế `occluded_level`.

## 3. Quy tắc vẽ box

1. Một vật có một class và một box; không gộp nhiều vật vào một box.
2. Vẽ hình chữ nhật nhỏ nhất bao toàn bộ các phần còn nhìn thấy của cùng một vật. Không mở rộng box để bao phần bị khuất.
3. Người ngồi trên xe và chiếc xe được gán riêng nếu cả hai thuộc bộ class.
4. Box nằm trong giới hạn ảnh. Vật bị cắt mép ghi `truncated=yes`.
5. Box đối tượng có chiều cao tối thiểu 20 px. Vật thấp hơn 20 px không được phóng box để đạt ngưỡng; không gán box đối tượng đó. Chiều cao đúng 20 px đạt điều kiện kích thước.
6. Không tự đổi class hoặc sửa taxonomy của Task trong quá trình gán theo cấu hình đã khóa.

## 4. Xử lý tình huống

| Mã quy tắc | Tình huống | Cách xử lý |
|---|---|---|
| `R-01` | Box sát vật | Đặt cạnh box sát các điểm ngoài cùng của phần vật còn nhìn thấy, hạn chế nền thừa. |
| `R-02` | Vật đi ra mép ảnh | Chỉ vẽ trong ảnh, ghi `truncated=yes`. |
| `R-03` | Vật bị che | Bao các phần còn nhìn thấy của cùng một vật; ghi mức che theo bảng thuộc tính. |
| `R-04` | Vật rất nhỏ | Không gán box đối tượng cao dưới 20 px; không tự phóng box. |
| `R-05` | Người trên xe | Gán người và xe thành hai đối tượng riêng; xác định mức che của từng đối tượng. |
| `R-06` | Tượng, ma-nơ-canh, đồ chơi, hình in hoặc phản chiếu | Không gán như người hoặc phương tiện thật trong cảnh. |
| `R-07` | Không xác định được mức che | Ghi `occluded_level=3`, đặt `can_review=true`. |
| `R-08` | Xe chở xe | Xét từng xe thật như một đối tượng riêng nếu thuộc class và đạt ngưỡng kích thước. |
| `R-09` | Vật ngoài bộ class | Không ép vào class gần giống; ghi vấn đề cấp ảnh nếu cần làm rõ. |

**Đối chiếu ảnh thật:** `img_002.jpg` gán riêng xe tải chở xe và từng ô tô thật trên sàn; `img_020.jpg` không gán xe trong phản chiếu; `img_038.jpg` không gán các mô hình ô tô đồ chơi trong tủ kính.

## 5. Kiểm tra chất lượng và phiên bản

Trước khi xuất COCO 1.0, tôi kiểm tra class, độ sát của box, đối tượng bị bỏ sót, box trùng và ba thuộc tính `occluded_level`, `truncated`, `can_review`. Ảnh không có đối tượng vẫn phải có trong danh sách ảnh của COCO.

Giữ nguyên các ngưỡng `rules` trong taxonomy: chiều cao box tối thiểu 20 px, IoU lớn 0.85 và IoU nhỏ 0.70. Ngưỡng che 25% là quy tắc của guideline cá nhân này.

Danh sách phát hiện SAM3 chỉ là tài liệu tham khảo tên class, không xác nhận box hoặc class đúng. Tài liệu có sử dụng AI hỗ trợ diễn đạt; cách đối chiếu ảnh và kết quả kiểm tra được ghi trong ghi chú cá nhân khi thực hiện.

Phiên bản cá nhân 232 — lần 1 quy định bộ class, cách vẽ box và thuộc tính che khuất. Guideline chung được duyệt riêng cùng nhóm.
