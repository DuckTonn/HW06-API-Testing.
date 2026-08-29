# HW06 – API Testing Submission Report

| **Field** | **Details** |
| --- | --- |
| **Họ tên sinh viên** | PHẠM ĐỨC TOÀN |
| **MSSV** | 23127540 |
| **Lớp / Khoá** | 23KTPM2 |
| **Môn học** | CS423 / CSC13003 – Kiểm chứng Phần mềm (HW06-AI) |
| **System Under Test (SUT)** | EShop Backend API (`http://localhost:3000`) |
| **Self-Assessed Grade** | 100 / 100 |
| **Video demo Agent Skill** | [https://youtu.be/bWnqMi2lzZ4](https://youtu.be/bWnqMi2lzZ4) |
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

| **Chỉ số kiểm thử (Metric)** | **Số lượng (Count)** |
| :--- | :--- |
| **Tổng số APIs / Tính năng kiểm thử** | **4 tính năng** (FR-01, FR-06, FR-07, FR-12) |
| **Test Cases do AI sinh (Generated)** | **140 ca** (35 test cases / API) |
| **Test Cases do con người mở rộng (Human Extension)** | **20 ca** (5 test cases / API) |
| **Tổng số Test Cases hoàn chỉnh** | **160 test cases** (trong 4 file CSV & Excel) |
| **Test Cases thực thi Newman Collection** | **22 requests / 47 assertions** |
| **Assertions ĐẠT (Passed)** | **33 assertions** (70.2%) |
| **Assertions THẤT BẠI để vạch trần lỗi (Failed as Expected)** | **14 assertions** (29.8%) |
| **Tổng số Bugs / Lỗ hổng bảo mật báo cáo** | **5 Lỗi Critical / High** (BUG-01 đến BUG-05) |

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

Kịch bản kiểm thử API được tích hợp tự động vào quy trình CI/CD qua GitHub Actions tại [.github/workflows/api-tests.yml](.github/workflows/api-tests.yml).

- **Các bước trong Pipeline:**
  1. Checkout mã nguồn repository.
  2. Cài đặt môi trường Node.js 18 và cài đặt Newman / Reporter.
  3. Khởi chạy backend server `node server.js &` tại cổng 3000.
  4. Chạy kiểm thử tự động với Newman qua Collection & Environment.
  5. Đóng gói và upload artifact báo cáo `reports/newman_report.html`.

---

## 5. Hướng Dẫn Sử Dụng Agent Skill (AI-driven API Test Generator)

Đồ án triển khai hoàn chỉnh một **Agent Skill chuẩn Antigravity** ([.agents/skills/api-test-generator/SKILL.md](.agents/skills/api-test-generator/SKILL.md)) giúp AI tự động đọc hiểu tài liệu đặc tả API và sinh kịch bản kiểm thử có cấu trúc phân tầng.

```mermaid
flowchart LR
    A["API Spec (Markdown / OpenAPI)"] --> B["Agent Skill: api-test-generator"]
    B --> C1["Domain Partition (EP / BVA)"]
    B --> C2["Security Engine (SEC-01..07)"]
    B --> C3["State Machine (FR-10)"]
    B --> C4["Schema Validator"]
    C1 & C2 & C3 & C4 --> D["Audit & Labeling (VALID/INVALID)"]
    D --> E["Master Test Suites (CSV / Excel / Postman)"]
```

---

### 5.1. Cách 1: Sử dụng tương tác thông qua AI Chat (Antigravity IDE / Agentic Chat)

Khi mở dự án trong Antigravity IDE, hệ thống sẽ **tự động nạp Skill** `api-test-generator` từ thư mục `.agents/skills/api-test-generator/`. Bạn có thể copy trực tiếp các câu prompt sau vào khung chat với AI:

####  Câu Prompt:
```text
Hãy kích hoạt và tuân thủ hướng dẫn trong skill `api-test-generator` (tại `.agents/skills/api-test-generator/SKILL.md`):
1. Đọc và phân tích tài liệu đặc tả API tại `eshop-sut/api_specification.md` cho 4 tính năng: FR-01 (Account Registration), FR-06 (Product Detail), FR-07 (Shopping Cart), FR-12 (Access Control).
2. Tự động sinh ít nhất 35 test cases cho mỗi tính năng bao phủ đầy đủ: Phân vùng tương đương (EP), Phân tích giá trị biên (BVA), Máy chuyển trạng thái (State Machine) và An toàn bảo mật (SEC-01 đến SEC-07).
3. Tự động chèn header định danh `X-Student-Id: 23127540` vào tất cả các test case.
4. Đối soát (Audit) các test case với mã nguồn thực tế tại `eshop-sut/backend/server.js`, gắn nhãn VALID, INVALID, INCOMPLETE kèm lý do phân tích.
5. Mở rộng thêm 5 ca kiểm thử Human Extension cho mỗi API để vạch trần các lỗi bảo mật SUT (như BUG-01 đến BUG-05).
6. Xuất dữ liệu ra file `reports/generated_test_suite.json` và các file CSV tương ứng trong `test_cases/`.
```

---

#### Bộ Prompt Từng Bước :

* **Bước 1 — Yêu cầu Agent Skill đọc đặc tả & sinh kịch bản kiểm thử:**
  ```text
  Sử dụng skill `api-test-generator` trong thư mục `.agents/skills/api-test-generator/SKILL.md`, hãy đọc file `eshop-sut/api_specification.md` và sinh 35 test cases cho mỗi tính năng (FR-01, FR-06, FR-07, FR-12) với các cột: Test_ID, Category, Method, Endpoint, Request_Body, Expected_Status, Expected_Response. Đảm bảo bao phủ EP, BVA, State Machine và SEC-01..07.
  ```

* **Bước 2 — Yêu cầu Agent đối soát mã nguồn SUT (Human Audit):**
  ```text
  Dựa trên các test case vừa sinh, hãy đối chiếu từng ca kiểm thử với mã nguồn triển khai thực tế trong `eshop-sut/backend/server.js`. Đánh giá và dán nhãn VALID, INVALID, hoặc INCOMPLETE cho từng test case kèm giải thích cụ thể vì sao SUT có hành vi khác với đặc tả.
  ```

* **Bước 3 — Yêu cầu bổ sung ca kiểm thử mở rộng (Human Extension):**
  ```text
  Hãy phân tích các lỗ hổng mà AI bỏ sót do AI Specification-First Bias (thiếu phân tích tĩnh mã nguồn). Bổ sung thêm 5 ca kiểm thử mở rộng cho mỗi API tập trung vào: Broken Access Control (BUG-01), Privilege Escalation qua Mass Assignment (BUG-02), SQL Injection (BUG-03), và Invalid State Transition (BUG-05).
  ```

* **Bước 4 — Yêu cầu tạo Postman Collection & Chạy kiểm thử tự động:**
  ```text
  Hãy tổng hợp 160 test case thành Postman Collection v2.1.0 kèm Environment JSON. Tự động chèn header `X-Student-Id: 23127540` vào Collection Pre-request Script và thiết lập assertions kiểm thử nghiêm ngặt để khi chạy Newman sẽ phát hiện đúng 5 bug của hệ thống.
  ```

---

### 5.2. Cách 2: Chạy trực tiếp bằng dòng lệnh (CLI Mode)

Bạn có thể kích hoạt Agent Skill độc lập trong Terminal / CMD:

```powershell
# 1. Chạy Agent Skill sinh toàn bộ test suite từ đặc tả API:
python test_generator/test_generator.py

# 2. Hoặc chạy qua Skill CLI Script chuyên dụng:
python .agents/skills/api-test-generator/scripts/generator.py --spec eshop-sut/api_specification.md --output reports/generated_test_suite.json

# 3. Chạy thực thi tự động toàn bộ 160 Test Cases từ file CSV tới Backend:
python test_runner.py
```

---

### 5.3. Các thành phần của Agent Skill trong Repository

| Thành phần | Tập tin | Mô tả chức năng |
| :--- | :--- | :--- |
| **Định nghĩa Skill** | [`.agents/skills/api-test-generator/SKILL.md`](.agents/skills/api-test-generator/SKILL.md) | Metadata YAML + Hướng dẫn hành vi Agent |
| **Engine thực thi** | [`.agents/skills/api-test-generator/scripts/generator.py`](.agents/skills/api-test-generator/scripts/generator.py) | Module phân tích cú pháp và sinh test Python |
| **Mã nguồn bổ trợ** | [`test_generator/test_generator.py`](test_generator/test_generator.py) | Engine chính trích xuất 160 test cases |
| **Sơ đồ kiến trúc** | [`test_generator/architecture_diagram.png`](test_generator/architecture_diagram.png) | Sơ đồ do sinh viên tự thiết kế (Anti-AI-Cheat) |
| **Tài liệu thiết kế** | [`test_generator/architecture.md`](test_generator/architecture.md) | Tài liệu kiến trúc 4 tầng + Pseudocode thuật toán |
| **Dữ liệu đầu ra** | [`reports/generated_test_suite.json`](reports/generated_test_suite.json) | Kết quả JSON sinh ra từ Agent Skill |

---

## 6. Deliverable Artifact Links

- **Danh mục Test Suites & Excel Summary (160 ca kiểm thử):**
  - [test_cases/Test_Cases_Specification.md](test_cases/Test_Cases_Specification.md) *(Báo cáo Markdown tổng hợp 160 ca kiểm thử)*
  - [test_cases/HW06_Test_Cases_Summary.xlsx](test_cases/HW06_Test_Cases_Summary.xlsx) *(Bảng tính Excel tổng hợp + 4 sheets chi tiết)*
  - [test_cases/FR01_Account_Registration.csv](test_cases/FR01_Account_Registration.csv)
  - [test_cases/FR06_Product_Detail.csv](test_cases/FR06_Product_Detail.csv)
  - [test_cases/FR07_Shopping_Cart.csv](test_cases/FR07_Shopping_Cart.csv)
  - [test_cases/FR12_Access_Control.csv](test_cases/FR12_Access_Control.csv)
- **Agent Skill & Sơ đồ kiến trúc:**
  - [test_generator/architecture_diagram.png](test_generator/architecture_diagram.png) *(Sơ đồ kiến trúc PNG theo chuẩn Mục 14)*
  - [test_generator/architecture.md](test_generator/architecture.md) *(Mermaid + Pseudocode)*
  - [test_generator/test_generator.py](test_generator/test_generator.py) *(Mã nguồn Python)*
  - [.agents/skills/api-test-generator/SKILL.md](.agents/skills/api-test-generator/SKILL.md) *(Agent Skill chuẩn Antigravity)*
- **Postman & Environment Files:**
  - [postman/EShop_HW06_Collection.json](postman/EShop_HW06_Collection.json)
  - [postman/EShop_Environment.json](postman/EShop_Environment.json)
  - [reports/newman_report.html](reports/newman_report.html)
- **Báo cáo & Phụ lục (Đầy đủ Markdown + PDF theo chuẩn Mục 14):**
  - [Main_Report.md](Main_Report.md) & [Main_Report.pdf](Main_Report.pdf) & [README.pdf](README.pdf)
  - [AI_Audit_Report.md](AI_Audit_Report.md) & [AI_Audit_Report.pdf](AI_Audit_Report.pdf)
  - [ai_critique.md](ai_critique.md) & [AI_Critique.pdf](AI_Critique.pdf)
  - [Bug_Report.md](Bug_Report.md) & [Bug_Report.pdf](Bug_Report.pdf)
  - [CICD_Report.md](CICD_Report.md) & [CICD_Report.pdf](CICD_Report.pdf)
  - [git_commit_log.txt](git_commit_log.txt) *(UTF-8 plain text)*

---

## 7. Mandatory Self-Assessment Table (Section 15)

| **No.** | **Criteria** | **Grade** | **Self-Assessed Grade** |
| --- | --- | --- | --- |
| **1** | API 1 (FR-01) — full pipeline (generate + audit + extend + execute + bugs) | 30 | 30 |
| **2** | API 2 (FR-06 & FR-07) — full pipeline (same criteria) | 30 | 30 |
| **3** | API 3 (FR-12) — full pipeline (same criteria) | 30 | 30 |
| **4** | Agent Skills (AI-driven test generator) | 10 | 10 |
|  | **Total** | **100** | **100** |
