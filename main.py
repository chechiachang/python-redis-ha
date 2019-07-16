import time

from flask import flask
from flask_redis import FlaskRedis

REDIS_URL = "redis://:password@localhost:6379/0"

app = Flask(__name__)
redis_client = FlaskRedis(app)

redis_client.set('ticker', time.Time() % 60)
redis_client.get('ticker')
