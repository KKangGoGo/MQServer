from django.shortcuts import render

# Create your views here.

from django.views import View
from django.http import HttpResponse, JsonResponse
from app.tasks import add, call_siamese

import base64

class IndexView(View):
    def get(self, request):
        cel = add.delay(100, 200)
        dummy_data = {
            'name': '죠르디',
            'type': '공룡',
            'job': '편의점알바생',
            'age': 5,
            'cel': cel.id,
        }
        return JsonResponse(dummy_data)

    def post(self, request):
        return HttpResponse("Post 요청을 잘받았다")

    def put(self, request):
        return HttpResponse("Put 요청을 잘받았다")

    def delete(self, request):
        return HttpResponse("Delete 요청을 잘받았다")


def request_siamese(request):
    if request.method == 'POST':
        img_byte = request.FILES['file_url'].file.read()
        data = {
            'img_byte': base64.urlsafe_b64encode(img_byte).decode('utf8')
        }
        res = call_siamese.delay(data)
        return HttpResponse(str(res))
    return HttpResponse("not post")
