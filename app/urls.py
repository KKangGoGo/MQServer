from django.urls import path

from . import views

app_name = 'ksb_api'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('siamese', views.request_siamese)
]
