# MinRide
# HỆ THỐNG QUẢN LÝ VÀ TỰ ĐỘNG GHÉP CẶP CHUYẾN ĐI (RIDE MANAGEMENT SYSTEM)

## Giới thiệu

Dự án mô phỏng **hệ thống quản lý tài xế, khách hàng, chuyến đi và tự động ghép cặp** như các ứng dụng **Grab, Be hoặc Gojek**.

Hệ thống được viết bằng **Python**, có thể chạy bằng **Streamlit** để tạo giao diện trực quan, bao gồm đầy đủ các module từ quản lý dữ liệu, tìm kiếm tài xế, đặt chuyến, lưu lịch sử, đến tự động ghép cặp.

## Cấu trúc dự án

├── driver_manager.py # Quản lý danh sách tài xế (DriverManagementSystem)
├── customer_manager.py # Quản lý danh sách khách hàng (CustomerManagementSystem)
├── find_driver_system.py # Tìm tài xế trong bán kính với các tiêu chí lọc/sắp xếp
├── ride.py # Lớp Ride và RideManagementSystem (quản lý chuyến đi)
├── booking_system.py # Hệ thống đặt chuyến (BookingSystem)
├── auto_matching.py # Tự động ghép cặp tài xế - khách hàng (AutoMatchingSystem)
├── undo_stack.py # Cấu trúc lưu lịch sử thao tác (UndoStack)
├── main.py # Giao diện Streamlit hoặc hàm chạy chính
├── rides.csv # File dữ liệu chuyến đi
└── README.md # Tài liệu mô tả dự án

## Chức năng chính

### Quản lý tài xế (`DriverManagementSystem`)
- Thêm, xóa, sửa, tìm kiếm tài xế.  
- Lưu danh sách tài xế trong:
  - `list`: lưu trữ tuần tự.
  - `dict (id_index)`: tra cứu nhanh theo ID – **O(1)**.
- Sắp xếp, lọc tài xế theo rating, số chuyến, kinh nghiệm.

---

### Quản lý khách hàng (`CustomerManagementSystem`)
- Quản lý thông tin khách hàng (ID, tên, tọa độ).  
- Lưu trữ trong `dict` để tra cứu nhanh.

---

### Tìm tài xế (`FindDriverSystem`)
- Tìm các tài xế **trong bán kính xác định** từ vị trí khách hàng.
- Có thể lọc theo:
  - Điểm đánh giá (`rating`)
  - Số chuyến (`trips`)
  - Kinh nghiệm (`experience`)
- Hỗ trợ **sắp xếp ưu tiên đa tiêu chí**, ví dụ:
  ```python
  sort_priority=['distance', '-rating', 'trips', '-experience']

### Quản lý chuyến đi (Ride & RideManagementSystem)

Lưu thông tin chi tiết từng chuyến đi (khách, tài xế, khoảng cách, giá, thời gian).

Đọc/ghi dữ liệu từ file CSV.

Cung cấp các hàm:

get_driver_trips() → lấy chuyến theo tài xế.

filter_trips_by_time() → lọc chuyến theo khoảng thời gian.

get_recent_trips() → lấy n chuyến gần nhất.

get_all_rides() → xuất toàn bộ chuyến.

### Đặt chuyến (BookingSystem)

Tạo đơn đặt chuyến (booking) giữa tài xế và khách hàng.

Tính toán:

Khoảng cách đón khách (pickup distance)

Tổng quãng đường

Giá tiền = tổng_km × FARE_RATE

Hỗ trợ:

confirm_all() → xác nhận tất cả đơn và tạo đối tượng Ride.

cancel_all() → hủy các đơn đang chờ.

get_pending() → lấy danh sách đơn chưa xác nhận.

### Tự động ghép cặp (AutoMatchingSystem)

Nhận yêu cầu của khách hàng (create_request).

Tìm tài xế rảnh gần nhất (find_best_driver).

Ghép tự động và tạo booking tương ứng (auto_match_all).

Cấu trúc dữ liệu:

Biến	Kiểu	Mục đích
requests	list	Hàng chờ yêu cầu gọi xe
busy	set	Lưu các ID tài xế đang bận
### Lịch sử thao tác (UndoStack)

Lưu lại các hành động người dùng (thêm, xóa, cập nhật...).

Cấu trúc stack (ngăn xếp) giới hạn dung lượng.

Hỗ trợ:

push(action)

pop()

history() để xem danh sách hành động.


## Luồng hoạt động

Khách hàng gửi yêu cầu gọi xe → AutoMatchingSystem.create_request()

Hệ thống tìm tài xế rảnh gần nhất → find_best_driver()

Tạo đơn đặt → BookingSystem.create_booking()

Xác nhận chuyến → sinh Ride mới

Dữ liệu chuyến đi lưu trong RideManagementSystem

| Thành phần               | Cấu trúc        | Vai trò                       |
| ------------------------ | --------------- | ----------------------------- |
| Danh sách tài xế         | `list` + `dict` | Lưu và tra cứu nhanh          |
| Danh sách khách hàng     | `dict`          | Quản lý khách hàng            |
| Danh sách chuyến đi      | `list`          | Lưu thông tin từng chuyến     |
| Lịch sử thao tác         | `stack (list)`  | Undo/Redo                     |
| Danh sách yêu cầu gọi xe | `list`          | Hàng chờ yêu cầu              |
| Tài xế đang bận          | `set`           | Quản lý tài xế đang hoạt động |

## Công thức và logic
### Tính khoảng cách Euclidean:
distance = sqrt((x2 - x1)**2 + (y2 - y1)**2)

### Tính giá tiền:
fare = (pickup_distance + trip_distance) * FARE_RATE
Mặc định FARE_RATE = 12000VND/km

## Cách chạy trương trình
### Chạy bằng terminal:
python main.py

### Chạy bằng Streamlit:
streamlit run main.py

## Ví dụ minh họa:
  from auto_matching import AutoMatchingSystem
  from booking_system import BookingSystem
  from ride import RideManagementSystem
  from driver_manager import DriverManagementSystem
  from customer_manager import CustomerManagementSystem
  
  drivers = DriverManagementSystem().load_from_file()
  customers = CustomerManagementSystem().load_from_file()
  rides = RideManagementSystem().load_from_file()
  
  booking_sys = BookingSystem(drivers, customers, rides)
  auto_match = AutoMatchingSystem(drivers, customers, booking_sys)
  
  # Tạo yêu cầu mới
  req, _ = auto_match.create_request("C5", 10.0)
  
  # Tự động ghép tài xế
  matches = auto_match.auto_match_all()
  
  print(matches)

## Tính năng nổi bật
Quản lý tài xế, khách hàng, chuyến đi
Tìm tài xế theo khoảng cách và bộ lọc
Tự động ghép cặp tài xế gần nhất
Tạo, xác nhận, hủy đơn đặt
Ghi/đọc dữ liệu CSV
Lưu lịch sử thao tác (UndoStack)
Giao diện dễ sử dụng trên Streamlit

## Hướng phát triển
Bổ sung bản đồ thực tế (Google Maps API).
Dự đoán thời gian di chuyển theo lưu lượng xe.
Mở rộng thuật toán tìm kiếm tài xế (KD-Tree / R-Tree).
Thêm biểu đồ thống kê và dashboard hiển thị.
