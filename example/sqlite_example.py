import sqlite3

# 连接到数据库（如果不存在则创建）
conn = sqlite3.connect('/home/data/win11_data/sqlite/example.db')
cursor = conn.cursor()

# 创建表
cursor.execute('''CREATE TABLE IF NOT EXISTS users
                  (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)''')

# 插入数据
cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ('Alice', 25))
cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ('Bob', 30))

# 提交更改
conn.commit()

# 查询数据
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()

# 打印查询结果
for row in rows:
    print(row)

# 更新数据
cursor.execute("UPDATE users SET age = ? WHERE name = ?", (26, 'Alice'))
conn.commit()

# 删除数据
# cursor.execute("DELETE FROM users WHERE name = ?", ('Bob',))
# conn.commit()

# 关闭连接
cursor.close()
conn.close()
