import time
import requests
import logging
from celery import Celery

# broker和backend参数指定了Redis的连接URL
app = Celery('tasks', broker='redis://lqjhome.cn:9379/0', backend='redis://lqjhome.cn:9379/0')

@app.task
def add(x, y):
    return x + y

@app.task
def sleep():
    time.sleep(5)
    return True

@app.task
def add_sleep(x, y):
    sleep()
    return x + y

@app.task(bind=True, max_retries=3)
def fetch_ip(self):
    try:
        url = "https://api.ipify231.org"
        response = requests.get(url)
        return response.text
    except Exception as exc:
        logging.error('Failed to fetch URL: %s, error: %s', url, exc)
        self.retry(exc=exc, countdown=10)

# celery -A tasks worker --loglevel=info -P eventlet