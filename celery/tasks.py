import time
from celery import Celery
app = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')
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


# celery -A tasks worker --loglevel=info -P eventlet