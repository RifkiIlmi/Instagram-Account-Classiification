from django.urls import path

from .views import index,process

urlpatterns = [
    path('', index, name='preprocessingIndex'),
    path('process/', process, name='process'),
]