#!/usr/bin/env python3
"""
AI API Test Generator - Executable Python Script for HW06
Generates test cases from EShop API Specification.
"""

import sys
import os
import json
import csv
import re

def parse_api_spec(spec_path):
    if not os.path.exists(spec_path):
        print(f"Error: Specification file not found at {spec_path}")
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

def generate_test_cases(endpoints):
    test_suite = []
    tc_index = 1
    
    for ep in endpoints:
        # Happy Path
        test_suite.append({
            "Test_ID": f"GEN_TC_{tc_index:03d}",
            "Category": "Domain Partition",
            "Title": f"Valid request to {ep['method']} {ep['path']}",
            "Method": ep['method'],
            "Endpoint": ep['path'],
            "Expected_Status": 200,
            "Audit_Status": "VALID"
        })
        tc_index += 1
        
        # Invalid Input / Missing Payload
        if ep['method'] in ['POST', 'PUT']:
            test_suite.append({
                "Test_ID": f"GEN_TC_{tc_index:03d}",
                "Category": "Domain Partition",
                "Title": f"Empty payload body on {ep['method']} {ep['path']}",
                "Method": ep['method'],
                "Endpoint": ep['path'],
                "Expected_Status": 400,
                "Audit_Status": "VALID"
            })
            tc_index += 1
            
        # Security Auth Check
        if ep['requires_auth']:
            test_suite.append({
                "Test_ID": f"GEN_TC_{tc_index:03d}",
                "Category": "Security",
                "Title": f"Unauthenticated access to {ep['path']}",
                "Method": ep['method'],
                "Endpoint": ep['path'],
                "Expected_Status": 401,
                "Audit_Status": "VALID"
            })
            tc_index += 1
            
            if "/admin/" in ep['path']:
                test_suite.append({
                    "Test_ID": f"GEN_TC_{tc_index:03d}",
                    "Category": "Security (SEC-01)",
                    "Title": f"Normal user token access to admin route {ep['path']}",
                    "Method": ep['method'],
                    "Endpoint": ep['path'],
                    "Expected_Status": 403,
                    "Audit_Status": "INVALID"
                })
                tc_index += 1
                
        # SQL Injection Check
        test_suite.append({
            "Test_ID": f"GEN_TC_{tc_index:03d}",
            "Category": "Security (SEC-02)",
            "Title": f"SQL Injection attempt on {ep['path']}",
            "Method": ep['method'],
            "Endpoint": ep['path'],
            "Expected_Status": 400,
            "Audit_Status": "VALID"
        })
        tc_index += 1
        
    return test_suite

def main():
    spec_file = sys.argv[1] if len(sys.argv) > 1 else "eshop-sut/api_specification.md"
    print(f"[+] Loading API Specification from: {spec_file}")
    endpoints = parse_api_spec(spec_file)
    print(f"[+] Found {len(endpoints)} API endpoints in spec.")
    
    test_cases = generate_test_cases(endpoints)
    print(f"[+] Successfully generated {len(test_cases)} automated API test cases!")
    
    output_json = "reports/generated_test_suite.json"
    os.makedirs("reports", exist_ok=True)
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(test_cases, f, indent=2, ensure_ascii=False)
    print(f"[+] Exported generated test cases to: {output_json}")

if __name__ == "__main__":
    main()
