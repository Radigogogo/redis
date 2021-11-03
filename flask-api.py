from flask import Flask
from redis import Redis  # 增加這行

import configs


app = Flask(__name__)
@app.route('/',methods=['GET'])
def home():
    return "<h1>hello python</h1>"

#app.config.from_object(configs.DevelopmentConfig)

# 連接本地的 redis server，埠號 6379，連接 0 號資料庫
r = Redis(host='localhost', port=6379, db=0)

# 設定資料 key => test, value => 0
r.set('test', 0)


app.run()