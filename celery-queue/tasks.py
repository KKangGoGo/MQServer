import os
import time
import base64
import requests

from celery import Celery

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379'),
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379')

celery = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)
celery.conf.update(task_serializer="pickle", accept_content=["pickle", "json"])


@celery.task(name='tasks.add')
def add(x: int, y: int) -> int:
    time.sleep(5)
    return x + y

@celery.task(name='tasks.check', retry_backoff=True, retry_kwargs={'max_retries': 5})
def check():
    time.sleep(5)
    res = requests.get('http://host.docker.internal:5888/check', verify=False)
    return res.status_code

@celery.task(name='tasks.siamese')
def get_siamese_result(data):
    time.sleep(5)
    img_byte = base64.b64decode(data['img_byte'])
    images = {'file_url': img_byte}
    res = requests.post('http://127.0.0.1:5888/siamese', files=images).json()
    return res