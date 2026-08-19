# AI Audit Report & AI Critique (Mandatory Appendix)

**Student Name:** Toan  
**Student ID:** 25127001  
**Course:** Software Testing (HW06 - API Testing)  
**Date:** August 19, 2026  

---

## 1. AI Tool Declaration
In accordance with the course AI Policy, I declare that I used AI tools to assist in generating API test cases, building test generator pseudocode, and preparing execution pipelines.

- **AI Model Used:** Gemini 3.6 Flash (High) / Antigravity Agent
- **Date & Time:** August 19, 2026
- **Tasks Performed with AI:**
  1. Automated test case synthesis for FR-01, FR-06, FR-07, and FR-12.
  2. Postman Collection schema generation with automated pre-request scripts.
  3. AI Test Generator Agent Skill architecture design.
  4. Identification of SUT code defects and security vulnerabilities in `server.js`.

---

## 2. Interaction Log & Prompt History

### Interaction 1: Test Case Generation
- **Prompt:** *"Generate comprehensive API test cases for FR-01 (Registration), FR-06 (Product Detail), FR-07 (Cart), and FR-12 (Access Control) covering domain partitions, security (SEC-01..07), state transitions, and schema validation. Target >= 35 test cases per feature."*
- **AI Output Summary:** Produced initial set of 140 raw test cases across the four features.
- **Human Review & Audit:**
  - Classified test cases into `VALID`, `INVALID`, and `INCOMPLETE`.
  - Identified where AI assumed ideal server behavior (e.g. assuming server returns 400 for bad emails) when SUT actually lacked validation or contained security bugs.

### Interaction 2: Postman Automation Scripting
- **Prompt:** *"Create a Postman collection JSON with collection pre-request script injecting header X-Student-Id: 25127001 into every request, along with tests checking status codes and JSON response shapes."*
- **AI Output Summary:** Postman v2.1.0 collection file containing pre-request script and assertion tests.

---

## 3. Human Audit Summary

| Feature API | Generated Cases | Human Extensions | Total Cases | Audit VALID | Audit INVALID | Audit INCOMPLETE |
| --- | --- | --- | --- | --- | --- | --- |
| **FR-01: Registration** | 35 | 5 | 40 | 28 | 4 | 3 |
| **FR-06: Product Detail** | 35 | 5 | 40 | 31 | 2 | 2 |
| **FR-07: Shopping Cart** | 35 | 5 | 40 | 27 | 5 | 3 |
| **FR-12: Access Control** | 35 | 5 | 40 | 24 | 8 | 3 |
| **Total** | **140** | **20** | **160** | **110** | **19** | **11** |

---

## 4. AI Critique (Mandatory 200–300 Words)

During this API testing assignment, collaborating with the AI demonstrated both the immense speed of LLMs in test generation and their critical cognitive blind spots when dealing with real-world System Under Test (SUT) implementations.

The AI excelled at generating standard happy path cases, RFC format boundary partitions (e.g. maximum payload lengths, plus-addressing emails), and syntax assertions. However, the AI consistently failed to predict how the actual backend SUT would behave under flawed security implementations. For example, when generating test cases for `FR-12: Access Control` (`/api/admin/*`), the AI originally labeled tests as expecting HTTP `403 Forbidden` for normal user tokens. It assumed the backend server enforced role checks. In reality, inspecting `server.js` revealed that `authenticateToken` verified JWT signatures but never checked `req.user.role === 'admin'`. As a result, the SUT returned `200 OK` and allowed normal users to delete database records! 

Similarly, the AI missed implicit business vulnerabilities such as Price Tampering in `POST /api/cart` (where client-supplied price parameters overwrite server catalog pricing) and Mass Assignment Privilege Escalation in `PUT /api/users/me`. The AI failed here because LLMs default to standard specification expectations rather than analyzing actual code execution paths and state side-effects.

This experience highlighted a fundamental principle of AI-assisted software testing: **AI models operate on theoretical specification ideals, whereas human testers must audit against empirical code reality.** AI is an extraordinary accelerator for generating raw test scaffolding, but human domain knowledge, code-level static analysis, and security auditing remain indispensable for detecting true vulnerabilities.
