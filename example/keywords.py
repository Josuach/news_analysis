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

# news_desc = "\n".join(news_descs)
# print(f"message length: {len(news_desc)}")
# print(news_desc)

filtered_keywords = []
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer

nlp = spacy.load("en_core_web_sm")

# text = ["I love learning Python for natural language processing. It is a great language for data analysis."]
text = news_descs

vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(text)
# indices = X[0].argsort()[::-1]  # 获取 TF-IDF 权重从高到低的索引

for x in X:
    indices = x.indices
    features = vectorizer.get_feature_names_out()

    keywords = [features[i] for i in indices[:3]]  # 获取前 5 个关键词
    print(keywords)
    filtered_keywords.extend(keywords)



# Deprecated functionality.
# from gensim import keywords

# text = "I love learning Python for natural language processing. It is a great language for data analysis."

# key_words = keywords(text, words=5).split('\n')  # 提取前 5 个关键词
# print(key_words)

# from summa import keywords

# text = "I love learning Python for natural language processing. It is a great language for data analysis."

# key_words = keywords.keywords(text)  # 提取关键词
# print(key_words)


remove_list = ["says", "gets", "reportedly", "best", "better",
               "study", "make", "finds", "reveals", "new", "researchers", "year", "shows", "report", "analysis", "predicts",
               "announces"]
filtered_keywords = [v for v in filtered_keywords if v not in remove_list]

import matplotlib.pyplot as plt
from wordcloud import WordCloud

text = " ".join(filtered_keywords)
wordcloud = WordCloud(width=1200, height=400,
                      background_color='white',
                      max_words=200).generate(text)

# # Save the word cloud to a file
wordcloud.to_file('/home/data/win11_data/technology_news.png')  # Specify the filename and format

