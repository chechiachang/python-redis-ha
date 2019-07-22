import os
import time
import logging

from flask import Flask
from flask import Config
from flask_redis import FlaskRedis

REDIS_SENTINEL_MASTER = 'mymaster'
REDIS_SENTINEL_URL = [('localhost', '26379')]
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD', '')

flask_app = Flask(__name__)
flask_app.config['REDIS_SENTINEL_URL'] = REDIS_SENTINEL_URL
flask_app.config['REDIS_SENTINEL_MASTER'] = REDIS_SENTINEL_MASTER

redis = FlaskRedis(password=REDIS_PASSWORD)
redis.init_app(flask_app)
flask_app.config["DEBUG"] = True

pipeline = redis.pipeline()
while True:
    pipeline.set('test', time.time() % 60 , ex=5)
    pipeline.get('test')
    try:
        result = pipeline.execute()
        print("Testing redis", result)
    except:
        print("error")
        time.sleep(1)
    else:
        time.sleep(1)
