from django.urls import path

from .views import index, analyze, summary

urlpatterns = [
    path('', index, name='klasifikasiIndex'),
    path('analyze/', analyze, name='analyze'),
    path('summary/', summary, name = "summary"),
]