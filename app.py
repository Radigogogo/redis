from flask import Flask
from redis import Redis  # 增加這行

import configs


app = Flask(__name__)
#app.config.from_object(configs.DevelopmentConfig)

# 連接本地的 redis server，埠號 6379，連接 0 號資料庫
r = Redis(host='localhost', port=6379, db=0)

# 設定資料 key => test, value => 0
r.set('test', 0)


@app.route('/')
def index():
    # key 為 test 的資料 +1
    r.incr('test')
    # 取得 test 的資料
    test = r.get('test')
    return test


if __name__ == '__main__':
    app.run()