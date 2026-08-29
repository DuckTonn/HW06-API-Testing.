# Báo Cáo Lỗi Phần Mềm (Bug Report) — Hệ Thống EShop SUT

**Người kiểm thử:** PHẠM ĐỨC TOÀN  
**MSSV:** 23127540 — **Lớp:** 23KTPM2  
**Môn học:** CS423 / CSC13003 – Kiểm chứng Phần mềm (HW06-AI)  
**Kho mã nguồn SUT:** [eshop-sut](eshop-sut)  
**Ngày lập báo cáo:** 19/08/2026  

---

## 1. Tóm Tắt Tổng Quan (Executive Summary)

Trong quá trình thực thi kiểm thử tự động toàn diện qua các phân vùng **Pool A** (FR-01: Đăng ký tài khoản, FR-06: Chi tiết sản phẩm), **Pool B** (FR-07: Giỏ hàng), và **Pool C** (FR-12: Phân quyền Web Admin), chúng tôi đã phát hiện **5 lỗi nghiêm trọng và lỗ hổng bảo mật** trong mã nguồn backend `eshop-sut/backend/server.js`.

Tất cả các lỗi đã được lập trình kịch bản kiểm thử trong Postman Collection và tự động phát hiện (FAIL) trong quy trình CI/CD Newman.

---

## 2. Chi Tiết Danh Mục Lỗi Phát Hiện

### 🐛 BUG-01: Lỗ Hổng Kiểm Soát Truy Cập (Broken Access Control - SEC-01) trên các API Admin
- **Mức độ nghiêm trọng:** **NGHIÊM TRỌNG (CRITICAL)**
- **Phân loại:** An ninh bảo mật / Kiểm soát phân quyền (Authorization)
- **Các Endpoint bị ảnh hưởng:**
  - `GET /api/admin/users` (Lấy danh sách toàn bộ người dùng)
  - `DELETE /api/admin/users/:id` (Xóa tài khoản người dùng bất kỳ)
  - `GET /api/admin/orders` (Xem danh sách đơn hàng toàn hệ thống)
  - `PUT /api/admin/orders/:id/status` (Cập nhật trạng thái đơn hàng)
  - `POST /api/admin/coupons` (Tạo mã giảm giá mới)
  - `DELETE /api/admin/coupons/:id` (Xóa mã giảm giá)
- **Mô tả lỗi:** Middleware `authenticateToken` chỉ kiểm tra tính hợp lệ của chữ ký JWT token nhưng **hoàn toàn không kiểm tra vai trò người dùng** (`req.user.role === 'admin'`). Do đó, bất kỳ tài khoản người dùng thông thường (`role: "user"`) nào sau khi đăng nhập đều có thể gửi request đến tất cả các API quản trị của Admin, đọc/xóa dữ liệu người dùng khác và thay đổi trạng thái đơn hàng.
- **Các bước tái hiện (Steps to Reproduce):**
  1. Đăng ký tài khoản người dùng thông thường qua `POST /api/register`.
  2. Đăng nhập qua `POST /api/login` và nhận chuỗi JWT `userToken`.
  3. Gửi request `GET /api/admin/users` kèm Header `Authorization: Bearer <userToken>`.
- **Kết quả thực tế (Observed Result):** Server trả về mã HTTP `200 OK` kèm theo toàn bộ danh sách người dùng, email và vai trò trong hệ thống.
- **Kết quả kỳ vọng (Expected Result):** Server bắt buộc phải từ chối truy cập và trả về mã lỗi HTTP `403 Forbidden` do tài khoản không có quyền Admin.
- **Đề xuất khắc phục:** Thêm middleware kiểm tra quyền `requireAdmin`:
  ```javascript
  function requireAdmin(req, res, next) {
    if (req.user && req.user.role === 'admin') {
      next();
    } else {
      res.status(403).json({ error: 'Access denied. Admin role required.' });
    }
  }
  ```

---

### 🐛 BUG-02: Lỗ Hổng Leo Thang Đặc Quyền qua Cập Nhật Hồ Sơ (Privilege Escalation - SEC-04)
- **Mức độ nghiêm trọng:** **NGHIÊM TRỌNG (CRITICAL)**
- **Phân loại:** Gán quyền trái phép (Mass Assignment / Role Escalation)
- **Endpoint bị ảnh hưởng:** `PUT /api/users/me`
- **Mô tả lỗi:** Backend cho phép client tùy ý truyền trường `role` trong payload JSON của API cập nhật thông tin cá nhân. Câu lệnh SQL cập nhật trực tiếp trường `users.role` trong cơ sở dữ liệu SQLite mà không có danh sách trắng (whitelist) các trường được phép sửa.
- **Các bước tái hiện (Steps to Reproduce):**
  1. Đăng nhập với tài khoản người dùng thường (`role = "user"`).
  2. Gửi request `PUT /api/users/me` kèm payload JSON:
     ```json
     {
       "name": "Attacker",
       "role": "admin"
     }
     ```
  3. Gọi lại API `GET /api/users/me` để kiểm tra thông tin tài khoản.
- **Kết quả thực tế (Observed Result):** Server trả về `200 OK` thông báo "Profile updated" và cập nhật trường `role` của người dùng thành `admin` trong cơ sở dữ liệu.
- **Kết quả kỳ vọng (Expected Result):** Server phải loại bỏ (strip) hoặc từ chối trường `role` trong payload cập nhật hồ sơ cá nhân và trả về mã lỗi `400 Bad Request`.
- **Đề xuất khắc phục:** Chỉ cho phép cập nhật các trường thông tin cơ bản (`name`, `shipping_address`, `phone`), tuyệt đối không nhận trường `role` từ client.

---

### 🐛 BUG-03: Lỗ Hổng Tiêm Mã Lệnh SQL (SQL Injection - SEC-02) trong Tìm Kiếm Sản Phẩm
- **Mức độ nghiêm trọng:** **CAO (HIGH)**
- **Phân loại:** An ninh bảo mật / SQL Injection
- **Endpoint bị ảnh hưởng:** `GET /api/products?search=...`
- **Mô tả lỗi:** Backend sử dụng phép nối chuỗi trực tiếp (template string) để tạo câu truy vấn SQL: `const query = 'SELECT * FROM products WHERE name LIKE \'%' + searchQuery + '%\'';` thay vì sử dụng tham số hóa (Parameterized Query / Prepared Statement).
- **Các bước tái hiện (Steps to Reproduce):**
  1. Gửi request `GET /api/products?search=' OR '1'='1`
- **Kết quả thực tế (Observed Result):** Câu lệnh SQL bị bẻ gãy cú pháp, trả về toàn bộ dữ liệu hoặc gây lỗi máy chủ `500 Internal Server Error` kèm trang HTML rò rỉ cấu trúc bảng cơ sở dữ liệu (`<h1>Database Error</h1>`).
- **Kết quả kỳ vọng (Expected Result):** Hệ thống phải sử dụng Parameterized Query `WHERE name LIKE ?` và trả về mã `200 OK` (kết quả rỗng) hoặc `400 Bad Request`, không để lộ thông tin cơ sở dữ liệu.

---

### 🐛 BUG-04: Thiếu Kiểm Tra Tính Hợp Lệ Của Email và Mật Khẩu (Input Validation - FR-01)
- **Mức độ nghiêm trọng:** **TRUNG BÌNH (MEDIUM)**
- **Phân loại:** Kiểm tra dữ liệu đầu vào (Input Validation / Boundary Value)
- **Endpoint bị ảnh hưởng:** `POST /api/register`
- **Mô tả lỗi:** API đăng ký tài khoản không kiểm tra định dạng email theo chuẩn RFC 5322, không kiểm tra độ dài tối thiểu hay độ phức tạp của mật khẩu.
- **Các bước tái hiện (Steps to Reproduce):**
  1. Gửi request `POST /api/register` với payload:
     ```json
     {
       "name": "Test User",
       "email": "invalid_email_format",
       "password": "1"
     }
     ```
- **Kết quả thực tế (Observed Result):** Server trả về `200 OK` với thông báo "User registered successfully" và lưu tài khoản không hợp lệ vào hệ thống.
- **Kết quả kỳ vọng (Expected Result):** Server phải từ chối và trả về mã lỗi `400 Bad Request` kèm thông điệp lỗi rõ ràng.

---

### 🐛 BUG-05: Vi Phạm Quy Trình Chuyển Đổi Trạng Thái Đơn Hàng (State Machine Violation - FR-10)
- **Mức độ nghiêm trọng:** **CAO (HIGH)**
- **Phân loại:** Lỗi logic nghiệp vụ / State Transition
- **Endpoint bị ảnh hưởng:** `PUT /api/admin/orders/:id/status`
- **Mô tả lỗi:** Mã nguồn backend có logic cho phép đơn hàng đã bị hủy (`canceled`) được chuyển sang trạng thái đã giao hàng (`delivered`). Điều này vi phạm nghiêm trọng máy trạng thái đơn hàng (đơn hàng đã hủy là trạng thái kết thúc - terminal state, không thể tiếp tục giao).
- **Các bước tái hiện (Steps to Reproduce):**
  1. Lấy một đơn hàng đang ở trạng thái `canceled`.
  2. Gửi request `PUT /api/admin/orders/:id/status` với body `{"status": "delivered"}`.
- **Kết quả thực tế (Observed Result):** Server trả về `200 OK`, cập nhật trạng thái đơn hàng thành `delivered`.
- **Kết quả kỳ vọng (Expected Result):** Server phải chặn giao dịch và trả về mã lỗi `400 Bad Request` với thông điệp `"Invalid state transition from canceled to delivered"`.

---

## 3. Tổng Hợp Mức Độ Nghiêm Trọng

| Mã Lỗi | Tên Lỗi | Endpoint | Mức Độ | Trạng Thái Phát Hiện |
| :---: | :--- | :--- | :---: | :---: |
| **BUG-01** | Broken Access Control trên API Admin | `/api/admin/*` | **CRITICAL** | Đã phát hiện qua Test Suite |
| **BUG-02** | Privilege Escalation qua cập nhật hồ sơ | `PUT /api/users/me` | **CRITICAL** | Đã phát hiện qua Test Suite |
| **BUG-03** | SQL Injection trong tìm kiếm sản phẩm | `GET /api/products` | **HIGH** | Đã phát hiện qua Test Suite |
| **BUG-04** | Thiếu validation email và mật khẩu | `POST /api/register` | **MEDIUM** | Đã phát hiện qua Test Suite |
| **BUG-05** | Cho phép chuyển trạng thái `canceled -> delivered` | `PUT /api/admin/orders/:id/status` | **HIGH** | Đã phát hiện qua Test Suite |
