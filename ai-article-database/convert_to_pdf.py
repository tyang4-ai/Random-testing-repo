"""
Markdown to HTML converter - creates a print-ready HTML file
The HTML file can be opened in a browser and printed to PDF
"""
import markdown
import os

# Read the markdown file
md_path = "/home/user/Random-testing-repo/ai-article-database/部署说明.md"
html_path = "/home/user/Random-testing-repo/ai-article-database/部署说明.html"

with open(md_path, 'r', encoding='utf-8') as f:
    md_content = f.read()

# Convert markdown to HTML
html_content = markdown.markdown(
    md_content,
    extensions=['tables', 'fenced_code', 'toc']
)

# Create full HTML with CSS styling for printing
full_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>环保文献智能数据库 - 部署说明</title>
    <style>
        @media print {{
            body {{ font-size: 11pt; }}
            pre {{ white-space: pre-wrap; word-wrap: break-word; }}
            h1 {{ page-break-before: auto; }}
            h2 {{ page-break-before: auto; page-break-after: avoid; }}
            h3 {{ page-break-after: avoid; }}
            pre, table {{ page-break-inside: avoid; }}
        }}

        * {{
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "Helvetica Neue", Helvetica, Arial, sans-serif;
            font-size: 14px;
            line-height: 1.7;
            color: #333;
            max-width: 900px;
            margin: 0 auto;
            padding: 40px 20px;
            background: #fff;
        }}

        h1 {{
            color: #1a5f2a;
            font-size: 28px;
            font-weight: 600;
            border-bottom: 3px solid #1a5f2a;
            padding-bottom: 12px;
            margin-top: 30px;
            margin-bottom: 20px;
        }}

        h2 {{
            color: #2d8a3e;
            font-size: 22px;
            font-weight: 600;
            border-bottom: 2px solid #e8f5e9;
            padding-bottom: 10px;
            margin-top: 35px;
            margin-bottom: 15px;
        }}

        h3 {{
            color: #1a5f2a;
            font-size: 18px;
            font-weight: 600;
            margin-top: 25px;
            margin-bottom: 12px;
        }}

        h4 {{
            color: #555;
            font-size: 16px;
            font-weight: 600;
            margin-top: 20px;
            margin-bottom: 10px;
        }}

        p {{
            margin: 12px 0;
        }}

        code {{
            background-color: #f5f5f5;
            padding: 3px 8px;
            border-radius: 4px;
            font-family: "SF Mono", "Consolas", "Monaco", "Menlo", monospace;
            font-size: 13px;
            color: #c7254e;
        }}

        pre {{
            background-color: #f8f8f8;
            border: 1px solid #e0e0e0;
            border-radius: 6px;
            padding: 16px;
            overflow-x: auto;
            font-size: 13px;
            line-height: 1.5;
            margin: 15px 0;
        }}

        pre code {{
            background-color: transparent;
            padding: 0;
            color: #333;
            font-size: 13px;
        }}

        blockquote {{
            border-left: 4px solid #2d8a3e;
            margin: 20px 0;
            padding: 12px 20px;
            background-color: #f9fdf9;
            color: #555;
            border-radius: 0 6px 6px 0;
        }}

        blockquote p {{
            margin: 0;
        }}

        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
            font-size: 14px;
        }}

        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}

        th {{
            background-color: #e8f5e9;
            color: #1a5f2a;
            font-weight: 600;
        }}

        tr:nth-child(even) {{
            background-color: #fafafa;
        }}

        tr:hover {{
            background-color: #f5f5f5;
        }}

        a {{
            color: #2d8a3e;
            text-decoration: none;
        }}

        a:hover {{
            text-decoration: underline;
        }}

        ul, ol {{
            margin: 12px 0;
            padding-left: 30px;
        }}

        li {{
            margin: 8px 0;
        }}

        hr {{
            border: none;
            border-top: 1px solid #e0e0e0;
            margin: 30px 0;
        }}

        strong {{
            color: #1a5f2a;
            font-weight: 600;
        }}

        /* Table of contents styling */
        .toc {{
            background: #f9f9f9;
            border: 1px solid #e0e0e0;
            border-radius: 6px;
            padding: 20px;
            margin: 20px 0;
        }}

        .toc ul {{
            list-style: none;
            padding-left: 0;
        }}

        .toc li {{
            margin: 5px 0;
        }}

        .toc a {{
            color: #333;
        }}

        /* Print button (hidden when printing) */
        .print-button {{
            position: fixed;
            top: 20px;
            right: 20px;
            background: #2d8a3e;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 500;
            box-shadow: 0 2px 8px rgba(0,0,0,0.15);
        }}

        .print-button:hover {{
            background: #1a5f2a;
        }}

        @media print {{
            .print-button {{
                display: none;
            }}
        }}
    </style>
</head>
<body>
    <button class="print-button" onclick="window.print()">🖨️ 打印/保存为PDF</button>
    {html_content}

    <script>
        // Auto-scroll to top when printing
        window.onbeforeprint = function() {{
            window.scrollTo(0, 0);
        }};
    </script>
</body>
</html>
"""

# Save HTML file
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(full_html)

print(f"HTML 文件已生成: {html_path}")
print("")
print("=" * 60)
print("如何生成 PDF:")
print("=" * 60)
print("1. 用浏览器打开生成的 HTML 文件")
print("2. 点击右上角的 '打印/保存为PDF' 按钮")
print("3. 在打印对话框中选择 '另存为PDF' 或 'Save as PDF'")
print("4. 保存文件")
print("")
print(f"HTML 文件位置: {html_path}")
