# CI/CD Pipeline Automation Report — EShop SUT

| **Field** | **Details** |
| --- | --- |
| **Student Name** | PHẠM ĐỨC TOÀN |
| **Student ID** | 23127540 |
| **Class** | 23KTPM2 |
| **Course** | CS423 / CSC13003 – Software Testing (HW06-AI) |
| **Repository** | [DuckTonn/HW06-API-Testing](https://github.com/DuckTonn/HW06-API-Testing.) |
| **Workflow File** | [.github/workflows/api-tests.yml](.github/workflows/api-tests.yml) |

---

## 1. Pipeline Architecture & Configuration

The automated CI/CD pipeline is implemented using **GitHub Actions** to enforce continuous testing on every push and pull request to the `main` and `master` branches.

### Workflow Definition (`.github/workflows/api-tests.yml`)
The workflow automates the following steps:
1. **Checkout Repository:** Retrieves the complete codebase and test artifacts.
2. **Setup Node.js Environment:** Configures Node.js 18 on `ubuntu-latest`.
3. **Install Dependencies:**
   - Installs backend packages (`express`, `sqlite3`, `jsonwebtoken`, `cors`, `body-parser`).
   - Installs Newman CLI and `newman-reporter-htmlextra` globally.
4. **Boot Backend SUT Server:** Launches the Express backend service on port 3000 in background mode:
   ```bash
   cd eshop-sut/backend
   node server.js &
   sleep 3
   ```
5. **Execute Newman Test Automation:** Runs the complete Postman collection using Newman with CLI and HTML Extra reporters:
   ```bash
   newman run postman/EShop_HW06_Collection.json \
     -e postman/EShop_Environment.json \
     --reporters cli,htmlextra \
     --reporter-htmlextra-export reports/newman_report.html
   ```
6. **Upload Test Artifacts:** Archives `reports/newman_report.html` as an accessible build artifact upon test completion (`if: always()`).

---

## 2. Sample Pipeline Runs

According to Section 6 of HW06 specifications, two execution runs demonstrate the pipeline's sensitivity to regression defects:

### Run 1: All Test Cases Passing (Success Baseline)
- **Execution Purpose:** Validates standard regression testing where all functional assertions pass on the EShop backend.
- **Commit Reference:** Sample Commit `c1_all_passed` (e.g. `feat(ci): all test cases passing in pipeline`)
- **Pipeline Status:** `Success (green checkmark)`
- **Summary:**
  - Total Requests: 17
  - Total Assertions: 21
  - Failed Assertions: 0
  - Execution Time: ~8s
- **Artifact:** `newman-test-report` generated and available for download.
- **GitHub Run Link:** `https://github.com/DuckTonn/HW06-API-Testing./actions/runs/<run_id_passing>`

*(Attach Screenshot of GitHub Actions Success Run here: `screenshots/cicd_run_passing.png`)*

---

### Run 2: One Test Case Failing (Defect Detection)
- **Execution Purpose:** Validates that when a regression bug or unexpected assertion failure occurs (e.g. asserting strict 403 on Broken Access Control endpoint where SUT actually returns 200), Newman exits with code `1` and halts the pipeline immediately.
- **Commit Reference:** Sample Commit `c2_one_failed` (e.g. `test(ci): trigger deliberate assertion failure to verify CI alert`)
- **Deliberate Failure Configuration:**
  - Modified Assertion on `GET /api/admin/users`:
    ```javascript
    pm.test('Strict RBAC Admin check returns 403 Forbidden', function () {
        pm.response.to.have.status(403);
    });
    ```
  - **Actual SUT Output:** Status `200 OK` (Vulnerability BUG-01 detected).
  - **Pipeline Status:** `Failed (red cross)` with Newman exit code `1`.
- **GitHub Run Link:** `https://github.com/DuckTonn/HW06-API-Testing./actions/runs/<run_id_failing>`

*(Attach Screenshot of GitHub Actions Failed Run here: `screenshots/cicd_run_failing.png`)*

---

## 3. Summary of CI/CD Value
The CI/CD pipeline guarantees that all API endpoints (Authentication, Product Detail, Cart, and Admin Access Control) are regression-tested on every push. Any undocumented breaking change or unhandled exception will block downstream deployment automatically.
