import markdown
from weasyprint import HTML

def markdown_to_pdf(md_content, output_file):
    # 将 Markdown 转换为 HTML
    html_content = markdown.markdown(md_content)

    # 渲染为 PDF 并保存
    HTML(string=html_content).write_pdf(output_file)

# 示例 Markdown 内容
md_content = """
# 示例标题

这是一个示例段落。下面是一个列表：

- 项目1
- 项目2
- 项目3
"""

# 将 Markdown 转换为 PDF 并保存为 example.pdf
markdown_to_pdf(md_content, '/home/data/win11_data/example.pdf')
