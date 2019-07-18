import os
import time
import logging

from flask import Flask
from flask import Config
from flask_redis import FlaskRedis

REDIS_URL = 'redis://:{password}@{host}:{port}/0'.format(
     password=os.environ.get('REDIS_PASSWORD', ''),
     host=os.environ.get('REDIS_HOST', '127.0.0.1'),
     port='6379',
)

flask_app = Flask(__name__)
flask_app.config['REDIS_URL'] = REDIS_URL

redis = FlaskRedis()
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
