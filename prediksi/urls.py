from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='prediksiIndex'),
    path('predict/', predict, name='predict'),
]