# Bug Report — EShop System Under Test (SUT)

**Tester:** Toan (Student ID: 25127001)  
**SUT Repository:** [eshop-sut](file:///e:/Nam3-HKIII/KiemThuPhanMem/HW06/eshop-sut)  
**Date:** August 19, 2026  

---

## Executive Summary
During the execution of automated API tests across Pool A (FR-01, FR-06), Pool B (FR-07), and Pool C (FR-12), **5 critical security vulnerabilities and logical defects** were detected in `eshop-sut/backend/server.js`.

---

## Bug Details

### 1. BUG-01: Broken Access Control (SEC-01) on Web Admin Endpoints
- **Severity:** CRITICAL
- **Category:** Security / Authorization
- **Affected Endpoints:**
  - `GET /api/admin/users`
  - `DELETE /api/admin/users/:id`
  - `GET /api/admin/orders`
  - `PUT /api/admin/orders/:id/status`
  - `POST /api/admin/coupons`
  - `DELETE /api/admin/coupons/:id`
- **Location in Code:** [server.js](file:///e:/Nam3-HKIII/KiemThuPhanMem/HW06/eshop-sut/backend/server.js#L494-L525)
- **Description:** The `authenticateToken` middleware verifies the JWT token signature, but admin routes fail to inspect whether `req.user.role === 'admin'`. As a result, any registered normal user token can access all administrative functions, including reading user data, deleting arbitrary users, modifying order statuses, and creating/deleting discount coupons.
- **Steps to Reproduce:**
  1. Register a standard user via `POST /api/register`.
  2. Login via `POST /api/login` and receive standard JWT token.
  3. Send request `GET /api/admin/users` with header `Authorization: Bearer <userToken>`.
- **Observed Result:** Status `200 OK` returned with full list of all system users and roles.
- **Expected Result:** Status `403 Forbidden` error indicating user lacks administrative privileges.

---

### 2. BUG-02: Privilege Escalation via Profile Update (SEC-04)
- **Severity:** CRITICAL
- **Category:** Mass Assignment / Role Escalation
- **Affected Endpoint:** `PUT /api/users/me`
- **Location in Code:** [server.js](file:///e:/Nam3-HKIII/KiemThuPhanMem/HW06/eshop-sut/backend/server.js#L124-L127)
- **Description:** Line 124 checks `if (role) { query += ", role = ?"; params.push(role); }`. The backend allows the client to pass a `role` field in the request body of `PUT /api/users/me`, updating `users.role` directly in SQLite.
- **Steps to Reproduce:**
  1. Login as standard user (`role = 'user'`).
  2. Send request `PUT /api/users/me` with body `{"name": "Attacker", "role": "admin"}`.
  3. Re-login or fetch user profile.
- **Observed Result:** User role in SQLite database is updated to `admin`.
- **Expected Result:** Server should ignore or strip `role` field in profile updates and return 400/403.

---

### 3. BUG-03: SQL Injection Vulnerability in Product Search (SEC-02)
- **Severity:** HIGH
- **Category:** Security / SQL Injection
- **Affected Endpoint:** `GET /api/products?search=...`
- **Location in Code:** [server.js](file:///e:/Nam3-HKIII/KiemThuPhanMem/HW06/eshop-sut/backend/server.js#L144)
- **Description:** Line 144 constructs raw SQL via string template literal: `const query = 'SELECT * FROM products WHERE name LIKE \'%${searchQuery}%\'';`. User input `searchQuery` is unescaped and unparameterized.
- **Steps to Reproduce:**
  1. Send request `GET /api/products?search=' OR '1'='1`
- **Observed Result:** Raw SQL string execution. On syntax error, server leaks full SQL schema back in HTML error response (`<h1>Database Error</h1>`).
- **Expected Result:** Query must use parameterized binding (`WHERE name LIKE ?`).

---

### 4. BUG-04: Lack of Password Complexity and Email Input Validation (FR-01)
- **Severity:** MEDIUM
- **Category:** Input Validation
- **Affected Endpoint:** `POST /api/register`
- **Location in Code:** [server.js](file:///e:/Nam3-HKIII/KiemThuPhanMem/HW06/eshop-sut/backend/server.js#L20-L30)
- **Description:** `POST /api/register` inserts `name, email, password` directly into database without verifying email RFC format or enforcing minimum password length/complexity.
- **Steps to Reproduce:**
  1. Send `POST /api/register` with body `{"name": "User", "email": "invalidemail", "password": "1"}`.
- **Observed Result:** Status `200 OK` with "User registered successfully".
- **Expected Result:** Status `400 Bad Request` with validation error message.

---

### 5. BUG-05: Insecure Order State Transition (Canceled -> Delivered) (FR-10)
- **Severity:** HIGH
- **Category:** Business Logic / State Machine Violation
- **Affected Endpoint:** `PUT /api/admin/orders/:id/status`
- **Location in Code:** [server.js](file:///e:/Nam3-HKIII/KiemThuPhanMem/HW06/eshop-sut/backend/server.js#L550-L551)
- **Description:** Line 550 explicitly sets `if (currentStatus === "canceled" && status === "delivered") isValidTransition = true;`. This allows canceled orders to be marked delivered, violating the order state machine transition rules.
- **Steps to Reproduce:**
  1. Select an order currently in `canceled` state.
  2. Send `PUT /api/admin/orders/:id/status` with body `{"status": "delivered"}`.
- **Observed Result:** Status `200 OK`, order status changed to `delivered`.
- **Expected Result:** Status `400 Bad Request` with error message `"Invalid state transition from canceled to delivered"`.
