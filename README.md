* Giới thiệu
Đây là một ứng dụng web đơn giản sử dụng Python Flask giúp người dùng mã hóa và giải mã file bằng thuật toán AES (Advanced Encryption Standard).
Ứng dụng hỗ trợ upload file, nhập khóa tùy ý và thực hiện mã hóa hoặc giải mã ngay trên trình duyệt với giao diện hiện đại.
+ Chức năng cơ bản
Tải lên file để mã hóa hoặc giải mã.
 Nhập khóa tùy chọn (dạng chuỗi văn bản).
 Mã hóa file với thuật toán AES-128 (chế độ ECB).
 Giải mã file đã mã hóa trước đó.
 Tự động tạo và tải xuống file kết quả.
 Giao diện đẹp, dễ sử dụng và tự động mở trình duyệt khi chạy ứng dụng.
* Kỹ thuật ,công nghệ
Thành phần	Công nghệ sử dụng
Backend	Flask (Python)
Mã hóa	AES (pycryptodome)
Frontend	Bootstrap 5, HTML5, CSS3
UI	Hiệu ứng Glassmorphism (blur + transparency)
Tự động mở trình duyệt	webbrowser + threading.Timer
Thư mục tĩnh	uploads/, results/
* Một số hình ảnh
  ![Uploading image.png…]()
