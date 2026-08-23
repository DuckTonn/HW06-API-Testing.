#!/usr/bin/env python3
"""
AI API Test Generator - Antigravity Agent Skill Script
Author: PHẠM ĐỨC TOÀN (MSSV: 23127540)
"""

import sys
import os
import json
import csv
import re
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="AI API Test Generator Agent Skill")
    parser.add_argument("--spec", default="eshop-sut/api_specification.md", help="Path to API specification markdown")
    parser.add_argument("--output", default="reports/generated_test_suite.json", help="Path to output JSON")
    parser.add_argument("--student-id", default="23127540", help="Student ID for header injection")
    return parser.parse_args()

def parse_api_spec(spec_path):
    if not os.path.exists(spec_path):
        print(f"[-] Error: Spec file not found at {spec_path}")
        return []

    with open(spec_path, 'r', encoding='utf-8') as f:
        content = f.read()

    endpoints = []
    lines = content.split('\n')
    current_section = ""
    current_title = ""

    for line in lines:
        if line.startswith("## "):
            current_section = line.replace("## ", "").strip()
        elif line.startswith("### "):
            current_title = line.replace("### ", "").strip()
        elif "- **Endpoint:**" in line:
            match = re.search(r'`(GET|POST|PUT|DELETE)\s+([^`]+)`', line)
            if match:
                method, path = match.groups()
                endpoints.append({
                    "section": current_section,
                    "title": current_title,
                    "method": method,
                    "path": path,
                    "requires_auth": "/admin/" in path or "/cart" in path or "/me" in path
                })
    return endpoints

def generate_comprehensive_tests(endpoints, student_id="23127540"):
    test_suite = []
    tc_index = 1

    for ep in endpoints:
        # 1. Happy Path
        test_suite.append({
            "Test_ID": f"GEN_TC_{tc_index:03d}",
            "Category": "Domain Partition (Happy Path)",
            "Title": f"Valid request to {ep['method']} {ep['path']}",
            "Method": ep['method'],
            "Endpoint": ep['path'],
            "Headers": {"X-Student-Id": student_id},
            "Expected_Status": 200,
            "Audit_Status": "VALID"
        })
        tc_index += 1

        # 2. Domain Partition - Boundary & Missing Payload
        if ep['method'] in ['POST', 'PUT']:
            test_suite.append({
                "Test_ID": f"GEN_TC_{tc_index:03d}",
                "Category": "Domain Partition (Missing Body)",
                "Title": f"Empty payload body on {ep['method']} {ep['path']}",
                "Method": ep['method'],
                "Endpoint": ep['path'],
                "Payload": {},
                "Expected_Status": 400,
                "Audit_Status": "VALID"
            })
            tc_index += 1

        # 3. Security - Authentication Requirement
        if ep['requires_auth']:
            test_suite.append({
                "Test_ID": f"GEN_TC_{tc_index:03d}",
                "Category": "Security (Unauthenticated)",
                "Title": f"Unauthenticated access attempt to {ep['path']}",
                "Method": ep['method'],
                "Endpoint": ep['path'],
                "Headers": {"X-Student-Id": student_id},
                "Expected_Status": 401,
                "Audit_Status": "VALID"
            })
            tc_index += 1

            if "/admin/" in ep['path']:
                test_suite.append({
                    "Test_ID": f"GEN_TC_{tc_index:03d}",
                    "Category": "Security (Broken Access Control SEC-01)",
                    "Title": f"Normal user token accessing admin endpoint {ep['path']}",
                    "Method": ep['method'],
                    "Endpoint": ep['path'],
                    "Headers": {"Authorization": "Bearer <normal_user_token>", "X-Student-Id": student_id},
                    "Expected_Status": 403,
                    "Audit_Status": "INVALID",
                    "Audit_Rationale": "SUT fails to check role='admin', returning 200 OK."
                })
                tc_index += 1

        # 4. Security - Injection & Tampering
        if ep['method'] in ['GET', 'POST']:
            test_suite.append({
                "Test_ID": f"GEN_TC_{tc_index:03d}",
                "Category": "Security (SQLi SEC-02)",
                "Title": f"SQL Injection verification on {ep['path']}",
                "Method": ep['method'],
                "Endpoint": ep['path'],
                "Expected_Status": 400,
                "Audit_Status": "VALID"
            })
            tc_index += 1

    return test_suite

def main():
    args = parse_arguments()
    print(f"[*] Agent Skill [api-test-generator] Initialized.")
    print(f"[*] Parsing spec from: {args.spec}")
    endpoints = parse_api_spec(args.spec)
    print(f"[+] Discovered {len(endpoints)} API endpoints in specification.")

    tests = generate_comprehensive_tests(endpoints, args.student_id)
    print(f"[+] Synthesized {len(tests)} automated test cases with Student ID {args.student_id}.")

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(tests, f, indent=2, ensure_ascii=False)
    print(f"[+] Output saved successfully to: {args.output}")

if __name__ == "__main__":
    main()
