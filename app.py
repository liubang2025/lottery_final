import os
import sqlite3
import random
from flask import Flask, render_template

# 导入你其他的自定义模块
from database import init_db
from scraper import fetch_latest
from predictor import get_ai_prediction
from config import get_detail

app = Flask(__name__)

@app.route('/')
def index():
    # 1. 自动初始化数据库（如果不存在则创建）
    try:
        init_db()
    except Exception as e:
        print(f"数据库初始化失败: {e}")

    # 2. 获取最新数据 (加入防御性编程)
    data = None
    try:
        data = fetch_latest()
    except Exception as e:
        print(f"爬虫运行出错: {e}")

    # 3. 如果抓取失败(data为空)，提供一套2026年的默认模拟数据，防止网页崩溃
    if not data:
        data = {
            "date": "等待数据更新",
            "nums": [1, 13, 25, 37, 49, 10], # 模拟平码
            "sp": 8                          # 模拟特码
        }

    # 4. 获取 AI 预测结果
    try:
        pred = get_ai_prediction()
    except Exception as e:
        print(f"AI预测模块出错: {e}")
        pred = {"main": [10, 20, 30, 40, 48, 49], "special": 1}

    # 5. 结合 config.py 里的逻辑，为号码匹配生肖和五行
    latest_info = []
    for n in data['nums']:
        latest_info.append({"n": n, "d": get_detail(n)})
    
    sp_info = {"n": data['sp'], "d": get_detail(data['sp'])}

    # 6. 渲染到网页
    return render_template(
        'index.html', 
        date=data['date'], 
        latest=latest_info, 
        sp=sp_info, 
        pred=pred
    )

if __name__ == "__main__":
    # 适配 Render 的环境端口
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
