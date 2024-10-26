import sqlite3
from googletrans import Translator  # 导入翻译库
import http.client, urllib.parse
import json
import os
import time

# 分别获取business、science、technology的数据存入不同数据库中，提供不同的配置(access_key和date在程序中给出)
# 注意到美国和巴黎有6小时时差，因此考虑晚上跑一次，早上跑一次，同时做数据去重（按照标题）
# 完成数据搜集后，出3张报表，提供关注的信息

# 初始化翻译器
translator = Translator()

access_key = "ecc24351cf7da9ac4825577ea48b5710"
date = "2024-10-25"

# 定义函数检查并添加句号
def ensure_period(text):
    if text and not text.endswith(('.', '!', '?')):
        return text + '.'
    return text

def create_table_if_not_exist(conn, cursor, db_name):
    # 创建 news 表，添加翻译字段
    cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS {db_name} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT UNIQUE,
        translated_title TEXT,  -- 翻译后的标题
        description TEXT,
        translated_description TEXT,  -- 翻译后的描述
        source TEXT,
        published_at TEXT,  -- 保存日期、时间和时区
        author TEXT,
        country TEXT,
        url TEXT,
        image TEXT,
        language TEXT
    )
    ''')

    # 提交创建表操作
    conn.commit()

def fecth_data(config):
    net_conn = http.client.HTTPConnection('api.mediastack.com')

    params = urllib.parse.urlencode({
        'access_key': access_key,
        'countries': config['countries'],
        'language': config['language'],
        'limit': config['limit'],
        'sort': config['sort'],
        'sources' : config['sources'],
        'date': date,
        'offset': config['offset'],
        "categories": config["categories"]
        })

    net_conn.request('GET', '/v1/news?{}'.format(params))

    res = net_conn.getresponse()
    data = res.read()

    json_str = data.decode('utf-8')

    return json_str

def store_data(conn, cursor, db_name, data):
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
        cursor.execute(f'''
        INSERT OR IGNORE INTO {db_name} (translated_title, translated_description, author, title, description, url, source, image, language, country, published_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            translated_title,  # 翻译后的标题
            translated_description,  # 翻译后的描述
            news_item.get('author'),
            title,  # 检查后的标题
            description,  # 检查后的描述
            news_item.get('url'),
            news_item.get('source'),
            news_item.get('image'),  # None 可以直接插入
            news_item.get('language'),
            news_item.get('country'),
            published_at_str  # 保留完整的日期、时间和时区字符串
        ))
        print("processed")

    # 提交所有插入操作
    conn.commit()
    
    
def fetch_data_and_store(config_file_path):
    config = {}
    with open(config_file_path, 'r', encoding='utf-8') as file:
        config = json.load(file)
    
    # 连接 SQLite 数据库（如果不存在会自动创建）
    conn = sqlite3.connect(f"/home/data/win11_data/sqlite/{config['db_name']}.db")
    cursor = conn.cursor()

    # cursor.execute(f"drop table IF EXISTS {config['db_name']}")
    # conn.commit()

    create_table_if_not_exist(conn, cursor, config['db_name'])

    json_str = fecth_data(config)
    # 解析 JSON 数据
    data = json.loads(json_str)

    store_data(conn, cursor, config['db_name'], data)

    # 关闭游标和连接
    cursor.close()
    conn.close()

    print("所有新闻数据已成功插入 SQLite 数据库，翻译后的标题和描述也已存储！")


if __name__ == '__main__':
    total_start_time = time.time()
    
    configs = [file for file in os.listdir("news/config")]
    for config in configs:
        start_time = time.time()
        print(f"processing config: {config}")
        
        fetch_data_and_store("news/config/" + config)

        end_time = time.time()
        elapsed_time = end_time - start_time
        print("finished")
        print(f"timecost: {elapsed_time:.2f}秒")

    
    total_end_time = time.time()
    elapsed_time = total_end_time - total_start_time
    print(f"total timecost: {elapsed_time:.2f}秒")
