from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='pembobotanIndex'),
    path('bobot/', bobot, name='bobot'),
    path('bigram/', bigram, name='bigram'),
]