from flask import Flask, render_template, jsonify
import time
import os
import json
from scraper import get_all_fund_flow_data

app = Flask(__name__)

# 缓存数据和上次更新时间
data_cache = None
last_update = 0
CACHE_TIME = 300  # 缓存时间5分钟

def get_data():
    """获取数据，使用缓存减少请求次数"""
    global data_cache, last_update
    current_time = time.time()
    
    # 如果缓存过期或不存在，则重新获取数据
    if data_cache is None or (current_time - last_update) > CACHE_TIME:
        data_cache = get_all_fund_flow_data()
        last_update = current_time
        
        # 保存到文件，用于调试和备份
        with open('data_cache.json', 'w', encoding='utf-8') as f:
            json.dump(data_cache, f, ensure_ascii=False, indent=2)
    
    return data_cache

@app.route('/')
def index():
    """首页"""
    data = get_data()
    return render_template('index.html', data=data)

@app.route('/api/data')
def api_data():
    """API接口，返回JSON数据"""
    data = get_data()
    return jsonify(data)

@app.route('/refresh')
def refresh():
    """强制刷新数据"""
    global data_cache, last_update
    data_cache = None
    data = get_data()
    return jsonify({'status': 'success', 'message': '数据已刷新'})

# 为生产环境添加配置
if __name__ == '__main__':
    # 确保templates目录存在
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    # 启动前先获取一次数据
    get_data()
    
    # 开发环境使用
    app.run(debug=True, host='0.0.0.0', port=5000)
else:
    # 生产环境使用
    # 启动前先获取一次数据
    get_data() 