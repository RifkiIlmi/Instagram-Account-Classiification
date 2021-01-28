from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.contrib import messages

from .models import Data

# Create your views here.
def index(request):
    data = Data.objects.all()

    context = {
        'data':data,
        'name' : 'Data',
        'title': 'Data - Instagram Market Classification'
    }
    return render(request,'data/index.html',context)