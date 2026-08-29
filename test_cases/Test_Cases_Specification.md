# Tổng Hợp Danh Mục 160 API Test Cases — EShop SUT
**Môn học:** CS423 / CSC13003 – Kiểm chứng Phần mềm (HW06-AI)
**Sinh viên:** PHẠM ĐỨC TOÀN | **MSSV:** 23127540 | **Lớp:** 23KTPM2
**System Under Test (SUT):** EShop Backend API (http://localhost:3000)

---

## 1. Thống Kê Tổng Quan
| Nhóm chức năng | Phân vùng | Endpoint chính | AI Generated | Human Extension | Tổng Test Cases |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **FR-01: Account Registration** | Pool A | POST /api/register | 35 | 5 | **40** |
| **FR-06: Product Detail View** | Pool A | GET /api/products/:id | 35 | 5 | **40** |
| **FR-07: Shopping Cart** | Pool B | GET /api/cart, POST /api/cart | 35 | 5 | **40** |
| **FR-12: Access Control** | Pool C | /api/admin/* | 35 | 5 | **40** |
| **TỔNG CỘNG** | **Pool A, B, C** | **Toàn diện hệ thống** | **140** | **20** | **160** |

---

## 2. FR-01: Account Registration (Pool A — Authentication)
*Tập tin nguồn CSV:* [test_cases/FR01_Account_Registration.csv](test_cases/FR01_Account_Registration.csv)

| Test ID | Nhóm kiểm thử | Mô tả kịch bản | Method & Endpoint | Request Body / Params | Expected Status | Expected Response | Audit Status | Lý do Audit (ISTQB / SUT Analysis) |
| :--- | :--- | :--- | :---: | :--- | :---: | :--- | :---: | :--- |
| FR01_TC001 | Domain Partition | Valid registration with standard name email and password | POST /api/register | {"name": "Nguyen Van A", "email": "user1@test.com", "password": "Password123!"} | 200 | User registered successfully | **VALID** | Valid test case covering standard happy path. |
| FR01_TC002 | Domain Partition | Registration with empty email | POST /api/register | {"name": "Nguyen Van B", "email": "", "password": "Password123!"} | 400 | error | **INVALID** | SUT missing validation; server currently returns 200 or SQLite error. Marked invalid for expected behavior fix. |
| FR01_TC003 | Domain Partition | Registration with invalid email format (no @) | POST /api/register | {"name": "Nguyen Van C", "email": "user3domain.com", "password": "Password123!"} | 400 | error | **INCOMPLETE** | AI did not test sub-domains or special symbols in email address. |
| FR01_TC004 | Domain Partition | Registration with empty password | POST /api/register | {"name": "Nguyen Van D", "email": "user4@test.com", "password": ""} | 400 | error | **INVALID** | Server accepts empty password without validation. AI assumed server had password complexity checks. |
| FR01_TC005 | Domain Partition | Registration with empty name | POST /api/register | {"name": "", "email": "user5@test.com", "password": "Password123!"} | 400 | error | **VALID** | Covers missing required name field. |
| FR01_TC006 | Domain Partition | Registration with missing name field in JSON | POST /api/register | {"email": "user6@test.com", "password": "Password123!"} | 400 | error | **VALID** | Covers missing JSON field payload validation. |
| FR01_TC007 | Domain Partition | Registration with missing email field in JSON | POST /api/register | {"name": "Nguyen Van G", "password": "Password123!"} | 400 | error | **VALID** | Covers payload schema boundary validation. |
| FR01_TC008 | Domain Partition | Registration with missing password field in JSON | POST /api/register | {"name": "Nguyen Van H", "email": "user8@test.com"} | 400 | error | **VALID** | Covers missing password key in payload. |
| FR01_TC009 | Domain Partition | Registration with duplicate email address | POST /api/register | {"name": "Nguyen Van I", "email": "user1@test.com", "password": "Password123!"} | 409 | error | **VALID** | Covers email uniqueness constraint. |
| FR01_TC010 | Domain Partition | Registration with maximum boundary length name (255 chars) | POST /api/register | {"name": "A".repeat(255), "email": "user10@test.com", "password": "Password123!"} | 200 | User registered successfully | **VALID** | Covers upper boundary for name length. |
| FR01_TC011 | Domain Partition | Registration with name exceeding 255 chars (256 chars) | POST /api/register | {"name": "A".repeat(256), "email": "user11@test.com", "password": "Password123!"} | 400 | error | **INCOMPLETE** | AI did not specify exact schema length limits. |
| FR01_TC012 | Domain Partition | Registration with short password (3 chars) | POST /api/register | {"name": "Nguyen Van L", "email": "user12@test.com", "password": "123"} | 400 | error | **INVALID** | SUT accepts 3-character password. Server lacks password policy enforce. |
| FR01_TC013 | Domain Partition | Registration with password containing unicode characters | POST /api/register | {"name": "Nguyen Van M", "email": "user13@test.com", "password": "MậtKhẩu123!"} | 200 | User registered successfully | **VALID** | Tests UTF-8 password handling. |
| FR01_TC014 | Domain Partition | Registration with whitespace-only name | POST /api/register | {"name": "   ", "email": "user14@test.com", "password": "Password123!"} | 400 | error | **VALID** | Tests sanitization of whitespace inputs. |
| FR01_TC015 | Domain Partition | Registration with upper/lowercase mixed email | POST /api/register | {"name": "Nguyen Van O", "email": "USER15@TEST.COM", "password": "Password123!"} | 200 | User registered successfully | **VALID** | Tests email case sensitivity handling. |
| FR01_TC016 | Domain Partition | Registration with email containing leading/trailing whitespace | POST /api/register | {"name": "Nguyen Van P", "email": "  user16@test.com  ", "password": "Password123!"} | 200 | User registered successfully | **VALID** | Tests whitespace trim on email input. |
| FR01_TC017 | Security | SQL Injection payload in email field | POST /api/register | {"name": "Hacker", "email": "' OR '1'='1'--@test.com", "password": "Password123!"} | 400 | error | **VALID** | Tests parameterized query sanitization against SQLi. |
| FR01_TC018 | Security | SQL Injection payload in name field | POST /api/register | {"name": "' DROP TABLE users;--", "email": "user18@test.com", "password": "Password123!"} | 200 | User registered successfully | **VALID** | Tests parameterized INSERT statement safety against SQLi injection. |
| FR01_TC019 | Security | XSS script payload in name field | POST /api/register | {"name": "<script>alert(1)</script>", "email": "user19@test.com", "password": "Password123!"} | 200 | User registered successfully | **VALID** | Tests HTML entity encoding/sanitization. |
| FR01_TC020 | Security | Parameter Pollution / Extra JSON fields (role injection attempt) | POST /api/register | {"name": "Attacker", "email": "user20@test.com", "password": "Password123!", "role": "admin"} | 200 | User registered successfully | **INCOMPLETE** | AI did not verify whether injected 'role' field was stored in DB as admin. |
| FR01_TC021 | Security | Large payload Denial of Service (1MB name payload) | POST /api/register | {"name": "A".repeat(1000000), "email": "user21@test.com", "password": "Password123!"} | 413 | Payload Too Large | **VALID** | Tests body parser size limit defense. |
| FR01_TC022 | Security | JSON syntax error / malformed JSON body | POST /api/register | {name: 'Nguyen Van V', email: 'user22@test.com'} | 400 | error | **VALID** | Tests JSON parsing error handling middleware. |
| FR01_TC023 | Security | Null byte injection in email field | POST /api/register | {"name": "NullUser", "email": "user23\u0000@test.com", "password": "Password123!"} | 400 | error | **VALID** | Tests null byte input filtering. |
| FR01_TC024 | Schema Validation | Response schema structure validation (id and message fields) | POST /api/register | {"name": "Nguyen Van X", "email": "user24@test.com", "password": "Password123!"} | 200 | {"message":"string","id":"number"} | **VALID** | Validates exact response JSON schema structure matching spec. |
| FR01_TC025 | Schema Validation | HTTP Content-Type application/json header missing | POST /api/register | name=Nguyen&email=user25@test.com&password=Password123! | 400 | error | **VALID** | Tests request header validation. |
| FR01_TC026 | Domain Partition | Registration with email containing plus sign (user+tag@domain.com) | POST /api/register | {"name": "Nguyen Van Z", "email": "user+tag26@test.com", "password": "Password123!"} | 200 | User registered successfully | **VALID** | Tests RFC 5322 compliant subaddressing in email. |
| FR01_TC027 | Domain Partition | Registration with numeric password only | POST /api/register | {"name": "Nguyen 27", "email": "user27@test.com", "password": "12345678"} | 200 | User registered successfully | **VALID** | Tests numeric-only password acceptance. |
| FR01_TC028 | Domain Partition | Registration with non-string name (number type in JSON) | POST /api/register | {"name": 12345, "email": "user28@test.com", "password": "Password123!"} | 400 | error | **VALID** | Tests JSON data type type-checking. |
| FR01_TC029 | Domain Partition | Registration with boolean value in email field | POST /api/register | {"name": "User 29", "email": true, "password": "Password123!"} | 400 | error | **VALID** | Tests boolean type validation for string parameters. |
| FR01_TC030 | Domain Partition | Registration with null value for password | POST /api/register | {"name": "User 30", "email": "user30@test.com", "password": null} | 400 | error | **VALID** | Tests null value rejection for mandatory fields. |
| FR01_TC031 | Domain Partition | Registration with empty JSON object `{}` body | POST /api/register | {} | 400 | error | **VALID** | Tests empty payload handling. |
| FR01_TC032 | Domain Partition | Registration with extra array in place of JSON object | POST /api/register | [{"name": "User 32", "email": "user32@test.com", "password": "Password123!"}] | 400 | error | **VALID** | Tests top-level array payload rejection. |
| FR01_TC033 | State Transition | Multiple rapid registration attempts with same email (Race condition) | POST /api/register | {"name": "User 33", "email": "user33@test.com", "password": "Password123!"} | 409 | error | **VALID** | Tests DB unique constraint during concurrent requests. |
| FR01_TC034 | Schema Validation | Verify status code 200 OK for successful registration | POST /api/register | {"name": "User 34", "email": "user34@test.com", "password": "Password123!"} | 200 | User registered successfully | **VALID** | Validates response HTTP status code 200. |
| FR01_TC035 | Schema Validation | Verify HTTP header Content-Type application/json in response | POST /api/register | {"name": "User 35", "email": "user35@test.com", "password": "Password123!"} | 200 | application/json | **VALID** | Validates response Content-Type header. |
| FR01_TC036 | Human Extension | Mass Assignment Attack - attempt to pass role='admin' in POST /api/register | POST /api/register | {"name": "Admin Attacker", "email": "admin_attacker@test.com", "password": "Password123!", "role": "admin"} | 200 | User registered successfully | **VALID** | Human extension: Verifies whether server strips role field or defaults to 'user'. |
| FR01_TC037 | Human Extension | No password hash validation - plaintext password leak check in DB response | POST /api/register | {"name": "Plaintext Test", "email": "plain@test.com", "password": "MySecretPass123"} | 200 | User registered successfully | **VALID** | Human extension: Asserts response does NOT return password field back in JSON body. |
| FR01_TC038 | Human Extension | No Rate Limiting on /api/register (Brute Force Registration / Spam) | POST /api/register | {"name": "Spam Bot", "email": "spam_bot@test.com", "password": "Password123!"} | 429 | Too Many Requests | **INVALID** | SUT has no rate limiting middleware configured on registration endpoint. |
| FR01_TC039 | Human Extension | Unicode Homograph Attack in email domain (e.g. gооgle.com using Cyrillic 'о') | POST /api/register | {"name": "Homograph User", "email": "user@gооgle.com", "password": "Password123!"} | 400 | error | **INCOMPLETE** | Tests IDN homograph vulnerability in registration email validation. |
| FR01_TC040 | Human Extension | No password complexity enforcement check (e.g. single space ' ') | POST /api/register | {"name": "Space Password", "email": "spacepass@test.com", "password": " "} | 400 | error | **INVALID** | SUT permits single space as password due to lack of input validation. |

---

## 3. FR-06: Product Detail View (Pool A — Catalog)
*Tập tin nguồn CSV:* [test_cases/FR06_Product_Detail.csv](test_cases/FR06_Product_Detail.csv)

| Test ID | Nhóm kiểm thử | Mô tả kịch bản | Method & Endpoint | Request Body / Params | Expected Status | Expected Response | Audit Status | Lý do Audit (ISTQB / SUT Analysis) |
| :--- | :--- | :--- | :---: | :--- | :---: | :--- | :---: | :--- |
| FR06_TC001 | Domain Partition | Fetch existing product with valid positive integer ID (id=1) | GET /api/products/1 | *None* | 200 | {"id":1,"name":"string"} | **VALID** | Standard happy path for existing product detail lookup. |
| FR06_TC002 | Domain Partition | Fetch non-existent product ID (id=99999) | GET /api/products/99999 | *None* | 404 | Product not found | **VALID** | Tests handling of missing resource ID. |
| FR06_TC003 | Domain Partition | Fetch product with ID = 0 | GET /api/products/0 | *None* | 404 | Product not found | **VALID** | Boundary value test for zero index ID. |
| FR06_TC004 | Domain Partition | Fetch product with negative integer ID (id=-1) | GET /api/products/-1 | *None* | 404 | Product not found | **VALID** | Boundary value test for negative integer parameter. |
| FR06_TC005 | Domain Partition | Fetch product with non-numeric string ID (id=abc) | GET /api/products/abc | *None* | 400 | Invalid product ID | **INVALID** | SUT returns 404 or sqlite null instead of explicit 400 bad request. |
| FR06_TC006 | Domain Partition | Fetch product with floating point number ID (id=1.5) | GET /api/products/1.5 | *None* | 400 | Invalid product ID | **INCOMPLETE** | AI did not test exact float parsing in backend route handler. |
| FR06_TC007 | Domain Partition | Fetch product with extremely large integer ID (id=9223372036854775807) | GET /api/products/9223372036854775807 | *None* | 404 | Product not found | **VALID** | Tests 64-bit integer boundary overflow handling. |
| FR06_TC008 | Domain Partition | Fetch product with empty ID path parameter (GET /api/products/) | GET /api/products/ | *None* | 200 | Array of products | **VALID** | Re-routed to product list endpoint GET /api/products. |
| FR06_TC009 | Domain Partition | Fetch product with whitespace padded ID (id=%201%20) | GET /api/products/%201%20 | *None* | 404 | Product not found | **VALID** | Tests url decoding and string trim on ID parameter. |
| FR06_TC010 | Domain Partition | Fetch product with special character ID (id=@#$) | GET /api/products/@#$ | *None* | 400 | error | **VALID** | Tests special characters handling in path params. |
| FR06_TC011 | Security | SQL Injection attempt in path parameter (id=1 OR 1=1) | GET /api/products/1%20OR%201=1 | *None* | 404 | Product not found | **VALID** | Tests parameterized SQL query protection against SQLi. |
| FR06_TC012 | Security | SQL Injection attempt with stacked queries (id=1; DROP TABLE products;--) | GET /api/products/1;%20DROP%20TABLE%20products;-- | *None* | 404 | Product not found | **VALID** | Tests sqlite statement isolation against stacked queries. |
| FR06_TC013 | Security | Path Traversal attempt in product ID (id=../../etc/passwd) | GET /api/products/../../etc/passwd | *None* | 404 | error | **VALID** | Tests URL routing security against path traversal. |
| FR06_TC014 | Security | XSS attempt in product ID parameter (id=<script>alert(1)</script>) | GET /api/products/%3Cscript%3Ealert(1)%3C/script%3E | *None* | 404 | Product not found | **VALID** | Tests reflect XSS defense on path parameters. |
| FR06_TC015 | Security | Null Byte Injection in product ID (id=1%00) | GET /api/products/1%00 | *None* | 400 | error | **VALID** | Tests string null byte handling in express route. |
| FR06_TC016 | Schema Validation | Validate response schema fields (id name price description imageUrl category_id) | GET /api/products/1 | *None* | 200 | {"id":1,"price":100000} | **VALID** | Validates JSON object schema fields match specification. |
| FR06_TC017 | Schema Validation | Validate data types of price (number) and description (string) | GET /api/products/1 | *None* | 200 | schema_data_types | **VALID** | Ensures numeric type for price and string type for description. |
| FR06_TC018 | State Transition | Fetch product detail before and after price update | GET /api/products/1 | *None* | 200 | updated_price | **VALID** | Verifies detail view reflects current DB state after updates. |
| FR06_TC019 | State Transition | Fetch product detail for deleted product (ID deleted by admin) | GET /api/products/99 | *None* | 404 | Product not found | **VALID** | Verifies state transition from active to deleted product returns 404. |
| FR06_TC020 | Domain Partition | Fetch product with URL encoded Chinese/Vietnamese characters (id=%E7%94%9F%E9%B1%BC) | GET /api/products/%E7%94%9F%E9%B1%BC | *None* | 404 | Product not found | **VALID** | Tests UTF-8 encoded URL path parameter handling. |
| FR06_TC021 | Domain Partition | Fetch product with hex string ID (id=0x1F) | GET /api/products/0x1F | *None* | 404 | Product not found | **VALID** | Tests hex number format handling. |
| FR06_TC022 | Domain Partition | Fetch product with scientific notation ID (id=1e3) | GET /api/products/1e3 | *None* | 404 | Product not found | **VALID** | Tests scientific exponential number string parsing. |
| FR06_TC023 | Domain Partition | Fetch product with boolean string ID (id=true) | GET /api/products/true | *None* | 404 | Product not found | **VALID** | Tests string literal boolean path handling. |
| FR06_TC024 | Domain Partition | Fetch product with null string ID (id=null) | GET /api/products/null | *None* | 404 | Product not found | **VALID** | Tests 'null' string path parameter handling. |
| FR06_TC025 | Domain Partition | Fetch product with undefined string ID (id=undefined) | GET /api/products/undefined | *None* | 404 | Product not found | **VALID** | Tests 'undefined' string parameter handling. |
| FR06_TC026 | Schema Validation | Verify HTTP Response Status 200 OK for valid product | GET /api/products/1 | *None* | 200 | OK | **VALID** | Verifies HTTP status 200. |
| FR06_TC027 | Schema Validation | Verify Content-Type header is application/json; charset=utf-8 | GET /api/products/1 | *None* | 200 | application/json | **VALID** | Verifies response header Content-Type. |
| FR06_TC028 | Schema Validation | Verify CORS headers present in GET /api/products/1 response | GET /api/products/1 | *None* | 200 | access-control-allow-origin | **VALID** | Verifies CORS access-control headers. |
| FR06_TC029 | Domain Partition | Fetch product with double slash in path (GET /api/products//1) | GET /api/products//1 | *None* | 200 | {"id":1} | **VALID** | Tests URL normalization for duplicate slashes. |
| FR06_TC030 | Domain Partition | Fetch product with trailing slash (GET /api/products/1/) | GET /api/products/1/ | *None* | 200 | {"id":1} | **VALID** | Tests URL normalization for trailing slashes. |
| FR06_TC031 | Domain Partition | HTTP POST request to GET-only endpoint /api/products/1 (without auth) | POST /api/products/1 | {} | 401 | Unauthorized | **VALID** | Verifies method authorization check. |
| FR06_TC032 | Domain Partition | HTTP DELETE request to /api/products/1 without auth token | DELETE /api/products/1 | *None* | 401 | Unauthorized | **VALID** | Verifies DELETE protection without admin token. |
| FR06_TC033 | Domain Partition | HTTP OPTIONS pre-flight request to /api/products/1 | OPTIONS /api/products/1 | *None* | 204 |  | **VALID** | Tests CORS OPTIONS pre-flight response. |
| FR06_TC034 | Domain Partition | Fetch product with Accept application/xml header | GET /api/products/1 | *None* | 200 | json | **VALID** | Verifies server returns JSON despite XML Accept header. |
| FR06_TC035 | Domain Partition | Fetch product with Cache-Control headers check | GET /api/products/1 | *None* | 200 |  | **VALID** | Verifies standard cache response headers. |
| FR06_TC036 | Human Extension | Information Disclosure - error stack trace leak on DB exception (id=NaN) | GET /api/products/NaN | *None* | 404 | Product not found | **VALID** | Human extension: Ensures internal DB errors do not leak stack traces or SQL schemas. |
| FR06_TC037 | Human Extension | Cache Invalidation Verification - modified product details update instantly | GET /api/products/1 | *None* | 200 | {"id":1} | **VALID** | Human extension: Verifies product details update immediately without stale caching. |
| FR06_TC038 | Human Extension | HTTP Head request handling (HEAD /api/products/1) | HEAD /api/products/1 | *None* | 200 |  | **VALID** | Human extension: Verifies HEAD request returns headers without body. |
| FR06_TC039 | Human Extension | Response Time SLA Performance Check (< 200ms response time) | GET /api/products/1 | *None* | 200 | <200ms | **VALID** | Human extension: Verifies response latency for product detail API. |
| FR06_TC040 | Human Extension | Decimal precision leak check on price field (no floating point inaccuracy) | GET /api/products/1 | *None* | 200 | {"price":100000} | **VALID** | Human extension: Checks price formatting is integer/exact decimal without Javascript float bug (e.g. 99999.99999999). |

---

## 4. FR-07: Shopping Cart (Pool B — Cart & Checkout)
*Tập tin nguồn CSV:* [test_cases/FR07_Shopping_Cart.csv](test_cases/FR07_Shopping_Cart.csv)

| Test ID | Nhóm kiểm thử | Mô tả kịch bản | Method & Endpoint | Request Body / Params | Expected Status | Expected Response | Audit Status | Lý do Audit (ISTQB / SUT Analysis) |
| :--- | :--- | :--- | :---: | :--- | :---: | :--- | :---: | :--- |
| FR07_TC001 | Domain Partition | Fetch empty cart for newly logged in user | GET /api/cart | *None* | 200 | [] | **VALID** | Happy path for empty cart retrieval. |
| FR07_TC002 | Domain Partition | Add valid item to cart with quantity 1 | POST /api/cart | {"id":1,"name":"Ao thun", "price":100000,"quantity":1} | 200 | Added to cart | **VALID** | Happy path item addition to cart. |
| FR07_TC003 | Domain Partition | Add valid item to cart with quantity 10 | POST /api/cart | {"id":2,"name":"Quan jean", "price":250000,"quantity":10} | 200 | Added to cart | **VALID** | Covers larger positive quantity addition. |
| FR07_TC004 | Domain Partition | Add item with quantity = 0 | POST /api/cart | {"id":1,"name":"Ao thun", "price":100000,"quantity":0} | 400 | Invalid quantity | **INVALID** | SUT accepts quantity 0 without validation. Server pushes invalid item. |
| FR07_TC005 | Domain Partition | Add item with negative quantity (-5) | POST /api/cart | {"id":1,"name":"Ao thun", "price":100000,"quantity":-5} | 400 | Invalid quantity | **INVALID** | SUT accepts negative quantity without validation. Server allows cart tampering. |
| FR07_TC006 | Domain Partition | Add item with non-numeric string quantity ("two") | POST /api/cart | {"id":1,"name":"Ao thun", "price":100000,"quantity":"two"} | 400 | Invalid quantity | **INCOMPLETE** | AI did not test string type conversion for quantity field. |
| FR07_TC007 | Domain Partition | Add item with float quantity (1.5) | POST /api/cart | {"id":1,"name":"Ao thun", "price":100000,"quantity":1.5} | 400 | Invalid quantity | **INCOMPLETE** | AI did not check integer quantity restriction. |
| FR07_TC008 | Domain Partition | Add item with missing price field | POST /api/cart | {"id":1,"name":"Ao thun", "quantity":1} | 400 | error | **VALID** | Tests missing mandatory product price field validation. |
| FR07_TC009 | Domain Partition | Add item with negative price (-1000) | POST /api/cart | {"id":1,"name":"Ao thun", "price":-1000,"quantity":1} | 400 | error | **INVALID** | SUT accepts negative price without validation. |
| FR07_TC010 | Domain Partition | Add item with missing product id | POST /api/cart | {"name":"Ao thun", "price":100000,"quantity":1} | 400 | error | **VALID** | Tests missing product ID validation. |
| FR07_TC011 | Security | Fetch cart without Authorization token | GET /api/cart | *None* | 401 | Unauthorized | **VALID** | Tests authentication requirement on GET /api/cart. |
| FR07_TC012 | Security | Add item to cart without Authorization token | POST /api/cart | {"id":1,"name":"Ao thun", "price":100000,"quantity":1} | 401 | Unauthorized | **VALID** | Tests authentication requirement on POST /api/cart. |
| FR07_TC013 | Security | Fetch cart with invalid / expired JWT token | GET /api/cart | *None* | 403 | Forbidden | **VALID** | Tests invalid token handling. |
| FR07_TC014 | Security | Fetch cart with malformed JWT token string ("Bearer invalid.token") | GET /api/cart | *None* | 403 | Forbidden | **VALID** | Tests malformed token signature verification. |
| FR07_TC015 | Security | IDOR / Cart Tampering - Attempt to access another user's cart via custom header | GET /api/cart | *None* | 200 | user_own_cart_only | **VALID** | Verifies cart endpoint extracts user ID exclusively from verified JWT payload. |
| FR07_TC016 | Security | Price Tampering - Client sends modified price lower than product catalog price | POST /api/cart | {"id":1,"name":"Laptop", "price":1,"quantity":1} | 400 | Price mismatch | **INVALID** | SUT accepts client-supplied price instead of pulling from DB. Vulnerable to price tampering! |
| FR07_TC017 | Security | SQL Injection payload in item name field | POST /api/cart | {"id":1,"name":"' OR 1=1--", "price":100000,"quantity":1} | 200 | Added to cart | **VALID** | Tests input sanitization in cart item object. |
| FR07_TC018 | Security | XSS script payload in item name field | POST /api/cart | {"id":1,"name":"<script>alert('xss')</script>", "price":100000,"quantity":1} | 200 | Added to cart | **VALID** | Tests XSS payload handling stored in in-memory cart. |
| FR07_TC019 | State Transition | Fetch cart after adding 1 item - verify cart contains 1 item | GET /api/cart | *None* | 200 | [{"id":1}] | **VALID** | State transition test for adding item and verifying cart contents. |
| FR07_TC020 | State Transition | Add same product twice - verify cart aggregation or duplicate entry | POST /api/cart | {"id":1,"name":"Ao thun", "price":100000,"quantity":1} | 200 | Added to cart | **VALID** | Tests item duplicate handling or quantity aggregation in cart. |
| FR07_TC021 | Domain Partition | Add item with extremely large quantity (999999999) | POST /api/cart | {"id":1,"name":"Ao thun", "price":100000,"quantity":999999999} | 400 | Quantity exceeds limit | **VALID** | Tests maximum inventory/quantity limit. |
| FR07_TC022 | Domain Partition | Add item with empty JSON object `{}` payload | POST /api/cart | {} | 400 | error | **VALID** | Tests empty object payload validation. |
| FR07_TC023 | Domain Partition | Add item with null price | POST /api/cart | {"id":1,"name":"Ao thun", "price":null,"quantity":1} | 400 | error | **VALID** | Tests null value rejection for mandatory fields. |
| FR07_TC024 | Domain Partition | Add item with boolean id (id=true) | POST /api/cart | {"id":true,"name":"Ao thun", "price":100000,"quantity":1} | 400 | error | **VALID** | Tests data type validation on product ID. |
| FR07_TC025 | Schema Validation | Verify GET /api/cart returns JSON Array response type | GET /api/cart | *None* | 200 | json_array | **VALID** | Verifies response is JSON array schema. |
| FR07_TC026 | Schema Validation | Verify POST /api/cart returns `{"message": "Added to cart"}` | POST /api/cart | {"id":1,"name":"Ao thun", "price":100000,"quantity":1} | 200 | {"message":"Added to cart"} | **VALID** | Validates JSON object schema response for cart insertion. |
| FR07_TC027 | Domain Partition | Add item with extra unknown fields in JSON (overposting attack) | POST /api/cart | {"id":1,"name":"Ao thun", "price":100000,"quantity":1,"secret_discount":99} | 200 | Added to cart | **INCOMPLETE** | AI did not test whether unknown attributes were stripped. |
| FR07_TC028 | Domain Partition | Fetch cart with empty Bearer token ("Authorization: Bearer ") | GET /api/cart | *None* | 401 | Unauthorized | **VALID** | Tests empty bearer token handling. |
| FR07_TC029 | Domain Partition | Fetch cart with Basic Auth header instead of Bearer token | GET /api/cart | *None* | 401 | Unauthorized | **VALID** | Tests non-Bearer auth scheme handling. |
| FR07_TC030 | Domain Partition | Add item with null name field | POST /api/cart | {"id":1,"name":null, "price":100000,"quantity":1} | 400 | error | **VALID** | Tests null check for item name. |
| FR07_TC031 | State Transition | Cart isolation check - User A cannot see User B cart | GET /api/cart | *None* | 200 | userA_cart_only | **VALID** | Verifies multi-tenant session cart isolation between users. |
| FR07_TC032 | Domain Partition | Add 100 distinct items to cart (Cart capacity boundary) | POST /api/cart | {"id":100,"name":"Item 100", "price":1000,"quantity":1} | 200 | Added to cart | **VALID** | Tests cart upper item capacity handling. |
| FR07_TC033 | Schema Validation | Verify status 200 OK on GET /api/cart | GET /api/cart | *None* | 200 | OK | **VALID** | Verifies HTTP 200 response status. |
| FR07_TC034 | Schema Validation | Verify Content-Type application/json header on GET /api/cart | GET /api/cart | *None* | 200 | application/json | **VALID** | Verifies Content-Type header on cart endpoints. |
| FR07_TC035 | Domain Partition | Add item with zero price (free promo item) | POST /api/cart | {"id":1,"name":"Free Gift", "price":0,"quantity":1} | 200 | Added to cart | **VALID** | Tests zero price item addition. |
| FR07_TC036 | Human Extension | In-memory cart memory leak vulnerability check under high payload | POST /api/cart | {"id":1,"name":"Big Payload", "price":100000,"quantity":1,"data":"A".repeat(100000)} | 400 | error | **INVALID** | Human extension: In-memory `userCarts` array stores arbitrary client data without size restriction causing server RAM leak! |
| FR07_TC037 | Human Extension | Cart Persistence Failure Check - Server restart wipes in-memory userCarts | GET /api/cart | *None* | 200 | [] | **INVALID** | Human extension: Cart is stored in global JS object (`userCarts`) rather than database. All cart data lost on server reboot. |
| FR07_TC038 | Human Extension | Race Condition on concurrent POST /api/cart requests | POST /api/cart | {"id":1,"name":"Ao thun", "price":100000,"quantity":1} | 200 | Added to cart | **VALID** | Human extension: Tests atomic cart mutation under concurrent async requests. |
| FR07_TC039 | Human Extension | Quantity Overflow Attack (quantity = Number.MAX_SAFE_INTEGER + 1) | POST /api/cart | {"id":1,"name":"Ao thun", "price":100000,"quantity":9007199254740992} | 400 | error | **VALID** | Human extension: Tests JavaScript safe integer overflow boundary on quantity calculation. |
| FR07_TC040 | Human Extension | Price Tampering checkout propagation bug check | POST /api/cart | {"id":1,"name":"Ao thun", "price":0.01,"quantity":1} | 200 | Added to cart | **INVALID** | Human extension: Tampered item price in cart propagates directly to total_amount in checkout API. |

---

## 5. FR-12: Access Control (Web Admin) (Pool C — Web Admin)
*Tập tin nguồn CSV:* [test_cases/FR12_Access_Control.csv](test_cases/FR12_Access_Control.csv)

| Test ID | Nhóm kiểm thử | Mô tả kịch bản | Method & Endpoint | Request Body / Params | Expected Status | Expected Response | Audit Status | Lý do Audit (ISTQB / SUT Analysis) |
| :--- | :--- | :--- | :---: | :--- | :---: | :--- | :---: | :--- |
| FR12_TC001 | Security | Fetch admin users list with valid Admin JWT token | GET /api/admin/users | *None* | 200 | [{"id":1,"role":"admin"}] | **VALID** | Happy path for authorized admin access to user list. |
| FR12_TC002 | Security | Fetch admin users list without Authorization header (Unauthenticated) | GET /api/admin/users | *None* | 401 | Unauthorized | **VALID** | Tests unauthenticated block on admin user list endpoint. |
| FR12_TC003 | Security | Broken Access Control (SEC-01) - Fetch admin users with Normal User JWT token | GET /api/admin/users | *None* | 403 | Forbidden | **INVALID** | SUT defect: Server accepts normal user token and returns admin user list (Broken Role Access Control!). |
| FR12_TC004 | Security | Delete user via DELETE /api/admin/users/2 with valid Admin token | DELETE /api/admin/users/2 | *None* | 200 | User deleted | **VALID** | Happy path for admin user deletion. |
| FR12_TC005 | Security | Broken Access Control - Delete user via DELETE /api/admin/users/2 with Normal User token | DELETE /api/admin/users/2 | *None* | 403 | Forbidden | **INVALID** | SUT defect: Normal user token can successfully delete other users from DB! |
| FR12_TC006 | Security | Fetch all system orders via GET /api/admin/orders with Admin token | GET /api/admin/orders | *None* | 200 | [{"id":1}] | **VALID** | Happy path for admin viewing system orders. |
| FR12_TC007 | Security | Broken Access Control - Fetch all system orders with Normal User token | GET /api/admin/orders | *None* | 403 | Forbidden | **INVALID** | SUT defect: Normal user can view all orders across all users in system. |
| FR12_TC008 | Security | Update order status via PUT /api/admin/orders/1/status with Admin token | PUT /api/admin/orders/1/status | {"status":"confirmed"} | 200 | Order status updated | **VALID** | Happy path for admin order state transition update. |
| FR12_TC009 | Security | Broken Access Control - Update order status with Normal User token | PUT /api/admin/orders/1/status | {"status":"confirmed"} | 403 | Forbidden | **INVALID** | SUT defect: Normal user token allowed to alter order status in admin endpoint. |
| FR12_TC010 | Security | Create new coupon via POST /api/admin/coupons with Admin token | POST /api/admin/coupons | {"code":"TEST100","type":"percent","discount_value":10,"min_order_amount":100000,"expired_at":"2030-12-31"} | 200 | Coupon created | **VALID** | Happy path for coupon creation by admin. |
| FR12_TC011 | Security | Broken Access Control - Create coupon with Normal User token | POST /api/admin/coupons | {"code":"HACK100","type":"percent","discount_value":99,"min_order_amount":0,"expired_at":"2030-12-31"} | 403 | Forbidden | **INVALID** | SUT defect: Normal user can create 99% off coupons! |
| FR12_TC012 | Security | Delete coupon via DELETE /api/admin/coupons/1 with Admin token | DELETE /api/admin/coupons/1 | *None* | 200 | Coupon deleted | **VALID** | Happy path for admin coupon deletion. |
| FR12_TC013 | Security | Broken Access Control - Delete coupon with Normal User token | DELETE /api/admin/coupons/1 | *None* | 403 | Forbidden | **INVALID** | SUT defect: Normal user token allowed to delete system coupons. |
| FR12_TC014 | Security | Access admin endpoint with forged / tampered JWT signature | GET /api/admin/users | *None* | 403 | Forbidden | **VALID** | Tests JWT signature verification algorithm defense. |
| FR12_TC015 | Security | Access admin endpoint with expired JWT token | GET /api/admin/users | *None* | 403 | Forbidden | **VALID** | Tests expired JWT token rejection. |
| FR12_TC016 | Security | Access admin endpoint with JWT using algorithm 'none' attack (alg: none) | GET /api/admin/users | *None* | 403 | Forbidden | **VALID** | Tests JWT alg=none vulnerability attack defense. |
| FR12_TC017 | Security | Delete non-existent user ID via DELETE /api/admin/users/999999 with Admin token | DELETE /api/admin/users/999999 | *None* | 200 | User deleted | **VALID** | Tests non-existent entity deletion response. |
| FR12_TC018 | Security | Invalid State Transition - Update order from pending directly to delivered | PUT /api/admin/orders/1/status | {"status":"delivered"} | 400 | Invalid state transition | **VALID** | Tests order state machine transition rules. |
| FR12_TC019 | Security | Invalid State Transition - Update order from canceled to shipping | PUT /api/admin/orders/1/status | {"status":"shipping"} | 400 | Invalid state transition | **VALID** | Tests state machine restriction from canceled state. |
| FR12_TC020 | Security | Update order status with invalid status string (status: 'super_delivered') | PUT /api/admin/orders/1/status | {"status":"super_delivered"} | 400 | Invalid state transition | **VALID** | Tests invalid state string input rejection. |
| FR12_TC021 | Security | Update order status with missing status field in JSON body | PUT /api/admin/orders/1/status | {} | 400 | Invalid state transition | **VALID** | Tests missing status parameter validation. |
| FR12_TC022 | Security | Create coupon with negative discount_value (-50) | POST /api/admin/coupons | {"code":"NEG50","type":"percent","discount_value":-50,"min_order_amount":100000,"expired_at":"2030-12-31"} | 400 | error | **INVALID** | SUT accepts negative coupon discount value. |
| FR12_TC023 | Security | Create coupon with discount_value exceeding 100 for percent type (150%) | POST /api/admin/coupons | {"code":"OVER100","type":"percent","discount_value":150,"min_order_amount":100000,"expired_at":"2030-12-31"} | 400 | error | **INVALID** | SUT permits >100% percentage discount creation. |
| FR12_TC024 | Security | Create coupon with past expiration date ("2020-01-01") | POST /api/admin/coupons | {"code":"PAST","type":"percent","discount_value":10,"min_order_amount":100000,"expired_at":"2020-01-01"} | 400 | error | **INCOMPLETE** | AI did not test past date validation logic on creation. |
| FR12_TC025 | Security | SQL Injection payload in delete user ID parameter (id=1 OR 1=1) | DELETE /api/admin/users/1%20OR%201=1 | *None* | 400 | error | **VALID** | Tests SQL injection defense in route params. |
| FR12_TC026 | Schema Validation | Verify GET /api/admin/users response array schema | GET /api/admin/users | *None* | 200 | [{"id":1,"name":"string","email":"string","role":"string"}] | **VALID** | Validates JSON schema response shape for users list. |
| FR12_TC027 | Schema Validation | Verify GET /api/admin/orders response schema includes user_name | GET /api/admin/orders | *None* | 200 | [{"id":1,"user_name":"string"}] | **VALID** | Validates order JOIN output schema. |
| FR12_TC028 | Domain Partition | Create coupon with min_order_amount = 0 | POST /api/admin/coupons | {"code":"ZERO_MIN","type":"fixed","discount_value":10000,"min_order_amount":0,"expired_at":"2030-12-31"} | 200 | Coupon created | **VALID** | Tests zero minimum order threshold. |
| FR12_TC029 | Domain Partition | Create coupon with duplicate coupon code | POST /api/admin/coupons | {"code":"TET2025","type":"percent","discount_value":10,"min_order_amount":100000,"expired_at":"2030-12-31"} | 400 | error | **VALID** | Tests duplicate coupon code unique index constraint. |
| FR12_TC030 | Domain Partition | Delete coupon with non-numeric string ID (id=abc) | DELETE /api/admin/coupons/abc | *None* | 400 | error | **VALID** | Tests string parameter handling on coupon deletion. |
| FR12_TC031 | Domain Partition | Update status of non-existent order ID (id=99999) | PUT /api/admin/orders/99999/status | {"status":"confirmed"} | 404 | Order not found | **VALID** | Tests missing order ID handling on status update. |
| FR12_TC032 | Domain Partition | Access admin endpoint with Bearer token containing empty spaces | GET /api/admin/users | *None* | 401 | Unauthorized | **VALID** | Tests white space token header parsing. |
| FR12_TC033 | Schema Validation | Verify status code 200 OK for GET /api/admin/users with admin auth | GET /api/admin/users | *None* | 200 | OK | **VALID** | Validates HTTP 200 status code. |
| FR12_TC034 | Schema Validation | Verify Content-Type header application/json on admin routes | GET /api/admin/users | *None* | 200 | application/json | **VALID** | Validates response content type header. |
| FR12_TC035 | Domain Partition | Delete self admin account via DELETE /api/admin/users/{self_id} | DELETE /api/admin/users/1 | *None* | 400 | Cannot delete active self account | **INVALID** | SUT allows admin to delete their own account from active session. |
| FR12_TC036 | Human Extension | Privilege Escalation via PUT /api/users/me - User promotes own role to admin | PUT /api/users/me | {"name":"Hacker","shipping_address":"123","phone":"0900000000","role":"admin"} | 200 | Profile updated | **INVALID** | Human extension: Critical vulnerability! PUT /api/users/me permits normal user to supply role="admin" and gain full admin rights! |
| FR12_TC037 | Human Extension | Invalid Order State Transition Bug - Server allows transition from canceled to delivered (line 550 in server.js) | PUT /api/admin/orders/1/status | {"status":"delivered"} | 400 | Invalid transition | **INVALID** | Human extension: Defect in server.js line 550: `if (currentStatus === 'canceled' && status === 'delivered') isValidTransition = true;` allows canceled orders to be marked delivered! |
| FR12_TC038 | Human Extension | Access Control Bypass via Case-Sensitivity (/API/ADMIN/USERS vs /api/admin/users) | GET /API/ADMIN/USERS | *None* | 401 | Unauthorized | **VALID** | Human extension: Verifies case sensitivity in express route matching for admin access control. |
| FR12_TC039 | Human Extension | Admin Session Invalidation on Password Reset / Role Revocation | GET /api/admin/users | *None* | 403 | Forbidden | **INVALID** | Human extension: SUT lacks token blacklist; revoked/demoted admin tokens remain valid until expiration. |
| FR12_TC040 | Human Extension | Import Products CSV JSON Injection Attack (POST /api/admin/import-products) | POST /api/admin/import-products | {"products":[{"name":"<script>alert(1)</script>","price":-10,"description":"Bad","imageUrl":"","category_id":1}]} | 400 | error | **INVALID** | Human extension: Import products endpoint allows bulk insertion of negative price and unescaped XSS strings. |

---
