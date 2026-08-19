# HW06 – API Testing Submission Report

| **Field** | **Details** |
| --- | --- |
| **Họ tên sinh viên** | PHẠM ĐỨC TOÀN |
| **MSSV** | 23127540 |
| **Lớp / Khoá** | 23KTPM2 |
| **Môn học** | CS423 / CSC13003 – Kiểm chứng Phần mềm (HW06-AI) |
| **System Under Test (SUT)** | EShop Backend API (`http://localhost:3000`) |
| **Self-Assessed Grade** | 100 / 100 |

---

## 1. Executive Summary & Selected APIs

Báo cáo này trình bày quy trình kiểm thử API đầu cuối (End-to-End AI-assisted API Testing Pipeline) trên hệ thống **EShop SUT**. Bốn tính năng thuộc Pool A, Pool B và Pool C được phân công và lựa chọn kiểm thử toàn diện:

| **Pool** | **Feature ID & Name** | **Backend API Endpoint(s)** | **Description** |
| --- | --- | --- | --- |
| **Pool A** | **FR-01: Account Registration** | `POST /api/register` | Đăng ký tài khoản người dùng mới với name, email, password |
| **Pool A** | **FR-06: Product Detail View** | `GET /api/products/:id` | Xem chi tiết thông tin một sản phẩm theo ID số |
| **Pool B** | **FR-07: Shopping Cart** | `GET /api/cart`<br>`POST /api/cart` | Lấy giỏ hàng cá nhân và thêm sản phẩm vào giỏ hàng |
| **Pool C** | **FR-12: Access Control** | `GET /api/admin/users`<br>`DELETE /api/admin/users/:id`<br>`GET /api/admin/orders`<br>`PUT /api/admin/orders/:id/status`<br>`POST /api/admin/coupons`<br>`DELETE /api/admin/coupons/:id` | Kiểm thử phân quyền truy cập hệ thống quản trị Web Admin |

---

## 2. Test Execution Summary Report

| **Metric** | **Count** |
| --- | --- |
| **Tổng số APIs / Tính năng kiểm thử** | 4 tính năng |
| **Test Cases do AI sinh** | 140 (35 test cases / API) |
| **Test Cases do con người mở rộng (Human Extension)** | 20 (5 test cases / API) |
| **Tổng số Test Cases thực thi** | **160 test cases** |
| **Test Cases Vượt qua (Passed)** | 122 |
| **Test Cases Phát hiện lỗi / Lỗ hổng (Failed as Expected)** | 38 |
| **Tổng số Bugs / Lỗ hổng bảo mật báo cáo** | **5 Lỗi Critical / High** |

---

## 3. Postman Features Exercised

Các tính năng Postman nâng cao được áp dụng xuyên suốt bộ kịch bản kiểm thử:

1. **Collection Hierarchy & Folders:** Tổ chức phân tầng khoa học theo nhóm chức năng: Setup & Auth, FR-01, FR-06, FR-07, và FR-12.
2. **Collection Pre-request Script:** Tự động gắn header định danh sinh viên `X-Student-Id: 23127540` vào **100%** các HTTP request:
   ```javascript
   pm.request.headers.add({ key: 'X-Student-Id', value: pm.environment.get('studentId') || '23127540' });
   ```
3. **Environment & Dynamic Variables:** Quản lý tập trung các biến `baseUrl`, `studentId`, `userToken`, `adminToken`, `productId`, `orderId` và hàm sinh số ngẫu nhiên `{{$randomInt}}`.
4. **Automated JavaScript Test Assertions:** Viết bằng `pm.test` kiểm tra HTTP status code, kiểu dữ liệu JSON Schema, cấu trúc mảng và chuỗi thông điệp.
5. **Newman CLI Automation & HTML Extra Reports:** Tự động hóa chạy kiểm thử headless trong dòng lệnh và trích xuất báo cáo HTML.

---

## 4. CI/CD Pipeline Configuration

Kịch bản kiểm thử API được tích hợp tự động vào quy trình CI/CD qua GitHub Actions tại [.github/workflows/api-tests.yml](file:///e:/Nam3-HKIII/KiemThuPhanMem/HW06/.github/workflows/api-tests.yml).

- **Các bước trong Pipeline:**
  1. Checkout mã nguồn repository.
  2. Cài đặt môi trường Node.js 18 và cài đặt Newman / Reporter.
  3. Khởi chạy backend server `node server.js &` tại cổng 3000.
  4. Chạy kiểm thử tự động với Newman qua Collection & Environment.
  5. Đóng gói và upload artifact báo cáo `reports/newman_report.html`.

---

## 5. Agent Skill (AI Test Generator)

Thiết kế và cài đặt hoàn chỉnh công cụ AI sinh test case tự động:
- **Kiến trúc & Pseudocode:** [test_generator/architecture.md](file:///e:/Nam3-HKIII/KiemThuPhanMem/HW06/test_generator/architecture.md)
- **Mã nguồn thực thi Python:** [test_generator/test_generator.py](file:///e:/Nam3-HKIII/KiemThuPhanMem/HW06/test_generator/test_generator.py)

---

## 6. Deliverable Artifact Links

- **Danh mục Test Suites (CSV - 160 ca kiểm thử):**
  - [test_cases/FR01_Account_Registration.csv](file:///e:/Nam3-HKIII/KiemThuPhanMem/HW06/test_cases/FR01_Account_Registration.csv)
  - [test_cases/FR06_Product_Detail.csv](file:///e:/Nam3-HKIII/KiemThuPhanMem/HW06/test_cases/FR06_Product_Detail.csv)
  - [test_cases/FR07_Shopping_Cart.csv](file:///e:/Nam3-HKIII/KiemThuPhanMem/HW06/test_cases/FR07_Shopping_Cart.csv)
  - [test_cases/FR12_Access_Control.csv](file:///e:/Nam3-HKIII/KiemThuPhanMem/HW06/test_cases/FR12_Access_Control.csv)
- **Postman & Environment Files:**
  - [postman/EShop_HW06_Collection.json](file:///e:/Nam3-HKIII/KiemThuPhanMem/HW06/postman/EShop_HW06_Collection.json)
  - [postman/EShop_Environment.json](file:///e:/Nam3-HKIII/KiemThuPhanMem/HW06/postman/EShop_Environment.json)
- **Báo cáo & Phụ lục AI:**
  - [AI_Audit_Report.md](file:///e:/Nam3-HKIII/KiemThuPhanMem/HW06/AI_Audit_Report.md) (Mẫu 5 mục FIT HCMUS 2026)
  - [AI_Critique.md](file:///e:/Nam3-HKIII/KiemThuPhanMem/HW06/AI_Critique.md) (Phê bình AI 200–300 từ)
  - [Bug_Report.md](file:///e:/Nam3-HKIII/KiemThuPhanMem/HW06/Bug_Report.md) (5 Lỗi bảo mật & Logic SUT)
  - [git_commit_log.txt](file:///e:/Nam3-HKIII/KiemThuPhanMem/HW06/git_commit_log.txt)

---

## 7. Mandatory Self-Assessment Table (Section 15)

| **No.** | **Criteria** | **Grade** | **Self-Assessed Grade** |
| --- | --- | --- | --- |
| **1** | API 1 (FR-01) — full pipeline (generate + audit + extend + execute + bugs) | 30 | 30 |
| **2** | API 2 (FR-06 & FR-07) — full pipeline (same criteria) | 30 | 30 |
| **3** | API 3 (FR-12) — full pipeline (same criteria) | 30 | 30 |
| **4** | Agent Skills (AI-driven test generator) | 10 | 10 |
|  | **Total** | **100** | **100** |
