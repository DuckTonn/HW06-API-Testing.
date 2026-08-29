import os
import re
import base64
import markdown
from playwright.sync_api import sync_playwright

css = """
@page {
    size: A4;
    margin: 15mm 12mm 15mm 12mm;
}
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    font-size: 12px;
    line-height: 1.55;
    color: #24292e;
    margin: 0;
    padding: 0;
}
h1, h2, h3, h4, h5, h6 {
    margin-top: 18px;
    margin-bottom: 8px;
    font-weight: 600;
    line-height: 1.25;
    color: #1a1e22;
    page-break-after: avoid;
}
h1 { font-size: 20px; border-bottom: 2px solid #eaecef; padding-bottom: 6px; }
h2 { font-size: 15px; border-bottom: 1px solid #eaecef; padding-bottom: 4px; }
h3 { font-size: 13px; }
p, ul, ol, blockquote { margin-top: 0; margin-bottom: 10px; }
table {
    border-collapse: collapse;
    width: 100%;
    margin-bottom: 14px;
    font-size: 11px;
    page-break-inside: auto;
}
tr {
    page-break-inside: avoid;
    page-break-after: auto;
}
table th, table td {
    padding: 5px 8px;
    border: 1px solid #dfe2e5;
    word-break: break-word;
}
table th {
    background-color: #f6f8fa;
    font-weight: 600;
}
table tr:nth-child(2n) {
    background-color: #fbfcfd;
}
code {
    font-family: Consolas, 'Liberation Mono', Menlo, Courier, monospace;
    font-size: 11px;
    padding: 2px 4px;
    background-color: #f6f8fa;
    border-radius: 3px;
    border: 1px solid #e1e4e8;
}
pre {
    background-color: #f6f8fa;
    border-radius: 4px;
    padding: 10px;
    overflow: hidden;
    white-space: pre-wrap;
    word-wrap: break-word;
    border: 1px solid #e1e4e8;
    margin-bottom: 14px;
    page-break-inside: avoid;
}
pre code {
    padding: 0;
    background-color: transparent;
    border: none;
    font-size: 10.5px;
}
blockquote {
    padding: 6px 12px;
    color: #444d56;
    border-left: 4px solid #0366d6;
    background-color: #f1f8ff;
    border-radius: 0 4px 4px 0;
    margin-bottom: 12px;
}
img {
    max-width: 95%;
    height: auto;
    display: block;
    margin: 10px auto;
    border: 1px solid #dfe2e5;
    border-radius: 4px;
    page-break-inside: avoid;
}
hr {
    height: 1px;
    background-color: #e1e4e8;
    border: none;
    margin: 16px 0;
}
"""

docs = [
    ('Main_Report.md', 'Main_Report.pdf'),
    ('Bug_Report.md', 'Bug_Report.pdf'),
    ('CICD_Report.md', 'CICD_Report.pdf'),
    ('AI_Audit_Report.md', 'AI_Audit_Report.pdf'),
    ('ai_critique.md', 'AI_Critique.pdf'),
    ('README.md', 'README.pdf')
]

def embed_images(text, base_dir="."):
    def img_sub(m):
        alt = m.group(1)
        src = m.group(2)
        src_path = os.path.join(base_dir, src)
        if os.path.exists(src_path):
            ext = os.path.splitext(src_path)[1].lower().replace('.', '')
            if ext == 'jpg': ext = 'jpeg'
            with open(src_path, 'rb') as img_f:
                b64 = base64.b64encode(img_f.read()).decode('utf-8')
            return f'<img alt="{alt}" src="data:image/{ext};base64,{b64}" />'
        return m.group(0)
    return re.sub(r'!\[(.*?)\]\((.*?)\)', img_sub, text)

print("Starting PDF export...")
with sync_playwright() as p:
    browser = p.chromium.launch()
    for md_file, pdf_file in docs:
        if not os.path.exists(md_file):
            print(f"[-] Missing {md_file}")
            continue
        with open(md_file, 'r', encoding='utf-8') as f:
            md_text = f.read()
        
        md_text = embed_images(md_text)
        html_body = markdown.markdown(md_text, extensions=['tables', 'fenced_code', 'toc'])
        full_html = f"<!DOCTYPE html><html><head><meta charset='utf-8'><style>{css}</style></head><body>{html_body}</body></html>"
        
        page = browser.new_page()
        page.set_content(full_html, wait_until='load')
        page.pdf(path=pdf_file, format='A4', print_background=True, margin={'top': '15mm', 'bottom': '15mm', 'left': '12mm', 'right': '12mm'})
        page.close()
        print(f"[+] Generated: {pdf_file} ({os.path.getsize(pdf_file):,} bytes)")
    browser.close()
print("All PDFs successfully created!")
