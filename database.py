import sqlite3
import os

# 适配 Render 的持久化路径
DB_DIR = '/opt/render/project/src/data' if os.environ.get('RENDER') else 'data'
DB_PATH = os.path.join(DB_DIR, 'lottery.db')

def init_db():
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("CREATE TABLE IF NOT EXISTS history (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, nums TEXT, sp INTEGER)")
    conn.close()

def get_history():
    conn = sqlite3.connect(DB_PATH)
    res = conn.execute("SELECT * FROM history ORDER BY id DESC LIMIT 10").fetchall()
    conn.close()
    return res
