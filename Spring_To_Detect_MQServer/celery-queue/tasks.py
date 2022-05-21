import os
import time
import requests
import json

from celery import Celery

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379'),
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379')

celery = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)
# celery.conf.update(task_serializer="pickle", accept_content=["pickle", "json"])


# Redis의 요청을 하나씩 처
@celery.task(name='tasks.detect')
def get_detect_result(data):
    try:
        time.sleep(2)
        res = requests.post('http://host.docker.internal:5999/data', data=json.dumps(data)).json()
        return res
    except Exception as e:
        return 'Connection Exception'
