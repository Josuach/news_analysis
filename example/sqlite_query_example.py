import sqlite3

news_descs = []

# 连接到 SQLite 数据库（如果数据库不存在，则会创建一个新的数据库文件）
conn = sqlite3.connect('/home/data/win11_data/sqlite/news_technology.db')

# 创建一个游标对象
cursor = conn.cursor()

# 执行 SELECT 查询
cursor.execute("select title from news_technology where date_int=20241025")  # 替换为你要查询的表名

# 获取所有结果
rows = cursor.fetchall()

# 打印每行的各列的值
# print("Query Results:")
for row in rows:
    # # row 是一个元组，包含了该行的所有列
    # for index, value in enumerate(row):
    #     print(f"Column {index}: {value}")
    # print()  # 打印空行以分隔不同的记录
    for value in row:
        # print(value)
        news_descs.append(value)

# 关闭游标和连接
cursor.close()
conn.close()

news_desc = "\n".join(news_descs)
print(f"message length: {len(news_desc)}")
print(news_desc)
# command = '''
# Following is the titles of some technology news. 
# Please output a summary for following content by topic. 
# Mark keywords in summary.\n
# '''
command = '''
Following content is titles of technology news. 
For every title of technology news, get 2 to 3 keywords from title. \n
'''
# command = "Following is the titles of some technology news. Please output 20 to 30 keywords for following content.\n"
message = command + news_desc


import requests
import json

# 设置请求的 URL
url = "http://192.168.1.50:8000/v1/chat/completions"

# 设置请求头
headers = {
    "Content-Type": "application/json"
}

# 设置请求数据
data = {
    "model": "meta-llama/Llama-3.2-1B-Instruct",
    "messages": [
        {"role": "user", "content": message}
    ]
}

# 发送 POST 请求
response = requests.post(url, headers=headers, data=json.dumps(data))

json = response.json()
# 输出响应内容
# print(response.status_code)  # 打印状态码
# print(response.json())       # 打印响应的 JSON 内容
# print(response.json()["choices"][0]["message"]["content"])
res = response.json()["choices"][0]["message"]["content"]

import markdown
from weasyprint import HTML

def markdown_to_pdf(md_content, output_file):
    # 将 Markdown 转换为 HTML
    html_content = markdown.markdown(md_content)

    # 渲染为 PDF 并保存
    HTML(string=html_content).write_pdf(output_file)


# 将 Markdown 转换为 PDF 并保存为 example.pdf
markdown_to_pdf(res, '/home/data/win11_data/keywords.pdf')