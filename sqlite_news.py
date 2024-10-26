import sqlite3
import json
from googletrans import Translator  # 导入翻译库

# 初始化翻译器
translator = Translator()

# 连接 SQLite 数据库（如果不存在会自动创建）
conn = sqlite3.connect('/home/data/win11_data/sqlite/news.db')
cursor = conn.cursor()

cursor.execute('drop table news')
# 提交创建表操作
conn.commit()

# 创建 news 表，添加翻译字段
cursor.execute('''
CREATE TABLE IF NOT EXISTS news (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT UNIQUE,
    translated_title TEXT,  -- 翻译后的标题
    description TEXT,
    translated_description TEXT,  -- 翻译后的描述
    source TEXT,
    published_at TEXT,  -- 保存日期、时间和时区
    category TEXT,
    author TEXT,
    country TEXT,
    url TEXT,
    image TEXT,
    language TEXT
)
''')

# 提交创建表操作
conn.commit()

# 示例 JSON 数据（包含数组的data字段）
# json_data = '''
# {
#     "pagination": {
#         "limit": 100,
#         "offset": 0,
#         "count": 100,
#         "total": 1311
#     },
#     "data": [
#         {
#             "author": "Dolat Capital",
#             "title": "SRF Q2 Results Review - Recovery Delayed As Uncertainties Persist: Dolat Capital",
#             "description": "SRF Q2 Results Review - Recovery Delayed As Uncertainties Persist: Dolat Capital",
#             "url": "https://www.ndtvprofit.com/research-reports/srf-q2-results-review-recovery-delayed-as-uncertainties-persist-dolat-capital",
#             "source": "Bloomberg | Latest And Live Business",
#             "image": null,
#             "category": "business",
#             "language": "en",
#             "country": "us",
#             "published_at": "2024-10-24T02:02:48+00:00"
#         },
#         {
#             "author": null,
#             "title": "Warning: NBTX is at high risk of performing badly",
#             "description": "Warning: NBTX is at high risk of performing badly",
#             "url": "https://seekingalpha.com/warnings/4197996-warning-nbtx-is-high-risk-of-performing-badly?utm_source=feed_news_all&utm_medium=referral&feed_item_type=news",
#             "source": "Seeking Alpha",
#             "image": null,
#             "category": "business",
#             "language": "en",
#             "country": "us",
#             "published_at": "2024-10-24T02:13:41+00:00"
#         }
#     ]
# }
# '''

import http.client, urllib.parse

net_conn = http.client.HTTPConnection('api.mediastack.com')

params = urllib.parse.urlencode({
    'access_key': 'ecc24351cf7da9ac4825577ea48b5710',
    'countries': 'cn,us',
    'language': 'zh',
    'limit': 100,
    'sort': 'published_desc',
    'categories': 'business,science,technology',
    'sources' : '-SeekingAlpha',
    'date': '2024-10-24',
    'offset': 0
    })

net_conn.request('GET', '/v1/news?{}'.format(params))

res = net_conn.getresponse()
data = res.read()

json_str = data.decode('utf-8')

# 解析 JSON 数据
data = json.loads(json_str)

# 定义函数检查并添加句号
def ensure_period(text):
    if text and not text.endswith(('.', '!', '?')):
        return text + '.'
    return text

# 遍历 data 数组中的每个新闻项目
for news_item in data['data']:
    # 获取并检查 title 和 description
    title = ensure_period(news_item.get('title', ''))
    description = ensure_period(news_item.get('description', ''))

    # 翻译 title 和 description 为中文
    translated_title = translator.translate(title, src='en', dest='zh-cn').text
    translated_description = translator.translate(description, src='en', dest='zh-cn').text

    # 直接保存 published_at 字段的完整字符串，包括时间和时区
    published_at_str = news_item.get('published_at')

    # 插入每个新闻项到 news 表中，包括翻译后的标题和描述
    cursor.execute('''
    INSERT OR IGNORE INTO news (translated_title, translated_description, author, title, description, url, source, image, category, language, country, published_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        translated_title,  # 翻译后的标题
        translated_description,  # 翻译后的描述
        news_item.get('author'),
        title,  # 检查后的标题
        description,  # 检查后的描述
        news_item.get('url'),
        news_item.get('source'),
        news_item.get('image'),  # None 可以直接插入
        news_item.get('category'),
        news_item.get('language'),
        news_item.get('country'),
        published_at_str  # 保留完整的日期、时间和时区字符串
    ))
    print("processed")

# 提交所有插入操作
conn.commit()

# 关闭游标和连接
cursor.close()
conn.close()

print("所有新闻数据已成功插入 SQLite 数据库，翻译后的标题和描述也已存储！")
