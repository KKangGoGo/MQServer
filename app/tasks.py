from __future__ import absolute_import, unicode_literals

from celery import shared_task
import requests
import base64

# from kombu import serialization
#
# serialization.register(
#             'mistral_serialization',
#             encoder=serializers.KombuSerializer.serialize,
#             decoder=serializers.KombuSerializer.deserialize,
#             content_type='application/octet-stream'
#         )

@shared_task
def add(x, y):
    return x + y

@shared_task
def call():
    res = requests.get('zhttp://host.docker.internal:5888/check', verify=False)
    return res.status_code

@shared_task(serializer='json')
def call_siamese(data):
    # img_byte = base64.b64decode(data['img_byte'])
    images = {'file_url': data['img_byte']}
    res = requests.post('http://host.docker.internal:5888/siamese', files=images).json()
    return res.status_code