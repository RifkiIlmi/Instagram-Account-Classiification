from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.contrib import messages

# Create your views here.
def index(request):
    context = {
        'name' : 'Home',
        'title': 'Home - Instagram Market Classification'
    }
    return render(request,'home/index.html',context)