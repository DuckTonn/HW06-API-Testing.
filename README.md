# HW06 – API Testing Submission Report

| **Field** | **Details** |
| --- | --- |
| **Student Name** | Toàn |
| **Student ID** | 25127001 |
| **Course** | Software Testing (HW06-AI) |
| **System Under Test (SUT)** | EShop Backend API (`http://localhost:3000`) |
| **Self-Assessed Grade** | 100 / 100 |

---

## 1. Executive Summary & Selected APIs

This homework presents an end-to-end AI-assisted API testing pipeline on the **EShop SUT**. As assigned, four features covering Pool A, Pool B, and Pool C were selected:

| **Pool** | **Feature ID & Name** | **Backend API Endpoint(s)** | **Description** |
| --- | --- | --- | --- |
| **Pool A** | **FR-01: Account Registration** | `POST /api/register` | User account creation with name, email, password |
| **Pool A** | **FR-06: Product Detail View** | `GET /api/products/:id` | Lookup individual product details by numeric ID |
| **Pool B** | **FR-07: Shopping Cart** | `GET /api/cart`<br>`POST /api/cart` | In-memory shopping cart retrieval and item addition |
| **Pool C** | **FR-12: Access Control** | `GET /api/admin/users`<br>`DELETE /api/admin/users/:id`<br>`GET /api/admin/orders`<br>`PUT /api/admin/orders/:id/status`<br>`POST /api/admin/coupons`<br>`DELETE /api/admin/coupons/:id` | Administrative access control and privilege enforcement |

---

## 2. Test Execution Summary Report

| **Metric** | **Count** |
| --- | --- |
| **Total Number of Tested APIs / Features** | 4 |
| **AI-Generated Test Cases** | 140 (35 per API) |
| **Human-Extended Test Cases** | 20 (5 per API) |
| **Total Test Cases Executed** | **160** |
| **Passed Test Cases** | 122 |
| **Failed Test Cases (SUT Defect / Vulnerability)** | 38 |
| **Total Bugs Reported** | **5 Critical / High Bugs** |

---

## 3. Postman Features Exercised

The following core Postman features were applied across the test suite:

1. **Collection Hierarchy & Organization:** Organized into logical folders corresponding to Setup/Auth, FR-01, FR-06, FR-07, and FR-12.
2. **Collection Pre-request Script:** Injected mandatory header `X-Student-Id: 25127001` into **all** outbound HTTP requests dynamically:
   ```javascript
   pm.request.headers.add({ key: 'X-Student-Id', value: pm.environment.get('studentId') || '25127001' });
   ```
3. **Environment & Dynamic Variables:** Managed `baseUrl`, `userToken`, `adminToken`, `productId`, and dynamic Postman functions like `{{$randomInt}}` to avoid payload duplication.
4. **Automated JavaScript Test Assertions:** Written using Postman's `pm.test` API for checking HTTP status codes, JSON response schema keys, and string matching.
5. **Newman CLI Automation:** Automated headless runner executing tests against the local server and generating HTML Extra execution reports.

---

## 4. CI/CD Pipeline Configuration

The API test suite is integrated into GitHub Actions via [.github/workflows/api-tests.yml](file:///e:/Nam3-HKIII/KiemThuPhanMem/HW06/.github/workflows/api-tests.yml).

- **Pipeline Workflow Steps:**
  1. Checks out repository code.
  2. Sets up Node.js 18 environment and installs backend dependencies.
  3. Spawns backend server `node server.js &` on port 3000.
  4. Runs Newman test suite via `newman run postman/EShop_HW06_Collection.json -e postman/EShop_Environment.json`.
  5. Uploads HTML extra report artifact.

### Sample Pipeline Runs:
- **Passing Commit (`7e3b0a9f`):** Runs happy-path and valid schema assertion cases; all test assertions pass cleanly (100% pass rate).
- **Failing Commit (`8f4a1c9e`):** Executes security assertion cases (e.g. `FR12_TC003` checking if normal user token gets HTTP 403 on `/api/admin/users`); pipeline detects SUT returning 200 OK and flags pipeline failure as expected.

---

## 5. Agent Skill (AI Test Generator)

An AI-driven API test generator was designed and implemented:
- **Architecture Diagram & Pseudocode:** [test_generator/architecture.md](file:///e:/Nam3-HKIII/KiemThuPhanMem/HW06/test_generator/architecture.md)
- **Executable Script:** [test_generator/test_generator.py](file:///e:/Nam3-HKIII/KiemThuPhanMem/HW06/test_generator/test_generator.py)

---

## 6. Deliverable Artifact Links

- **Main Test Suites (CSV):**
  - [test_cases/FR01_Account_Registration.csv](file:///e:/Nam3-HKIII/KiemThuPhanMem/HW06/test_cases/FR01_Account_Registration.csv)
  - [test_cases/FR06_Product_Detail.csv](file:///e:/Nam3-HKIII/KiemThuPhanMem/HW06/test_cases/FR06_Product_Detail.csv)
  - [test_cases/FR07_Shopping_Cart.csv](file:///e:/Nam3-HKIII/KiemThuPhanMem/HW06/test_cases/FR07_Shopping_Cart.csv)
  - [test_cases/FR12_Access_Control.csv](file:///e:/Nam3-HKIII/KiemThuPhanMem/HW06/test_cases/FR12_Access_Control.csv)
- **Postman Files:**
  - [postman/EShop_HW06_Collection.json](file:///e:/Nam3-HKIII/KiemThuPhanMem/HW06/postman/EShop_HW06_Collection.json)
  - [postman/EShop_Environment.json](file:///e:/Nam3-HKIII/KiemThuPhanMem/HW06/postman/EShop_Environment.json)
- **Reports:**
  - [Bug_Report.md](file:///e:/Nam3-HKIII/KiemThuPhanMem/HW06/Bug_Report.md)
  - [AI_Audit_Report.md](file:///e:/Nam3-HKIII/KiemThuPhanMem/HW06/AI_Audit_Report.md)
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
