import os
import time
import base64
import requests
import json

from celery import Celery

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379'),
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379')

celery = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)


@celery.task(name='tasks.testpost')
def test_post():
    res = requests.post('http://3.35.24.108/test/post', files=images).json()
    return res


@celery.task(name='tasks.siamese')
def get_siamese_result(data):
    try:
        time.sleep(2)
        res = requests.post('http://52.79.226.64//siamese', data=json.dumps(data)).json()
        return res
    except Exception as e:
        return 'Connection Exception'
