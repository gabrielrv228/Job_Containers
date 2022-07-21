import time

import redis
from flask import Flask
import logging, sys, json_logging
from prometheus_flask_exporter import PrometheusMetrics


import os

# Set environment variables
REDIS_HOST = os.environ['REDIS_HOST']
REDIS_PORT = os.environ['REDIS_PORT']
REDIS_PASSWORD = os.environ['REDIS_PASSWORD']


app = Flask(__name__)
json_logging.init_flask(enable_json=True)
json_logging.init_request_instrument(app)

# init the logger as usual
logger = logging.getLogger("logger")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))

cache = redis.Redis(host=REDIS_HOST, port=int(REDIS_PORT), password=REDIS_PASSWORD)

metrics = PrometheusMetrics(app)

# static information as metric
metrics.info('app_info', 'Application info', version='1.0.3')


def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                logger.error("Can't connect to redis")
                logger.exception(exc)
                raise exc
            retries -= 1
            time.sleep(0.5)


@app.route('/')
def hello():
    count = get_hit_count()
    message = 'Hello Keepcoding! I have been seen {} times.\n'.format(count)
    return message

@app.route('/health/live')
@metrics.do_not_track()
def health_live():
    return "Ok"

@app.route('/health/ready')
@metrics.do_not_track()
def health_ready():
    return "Ok"
