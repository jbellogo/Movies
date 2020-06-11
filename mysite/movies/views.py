from django.shortcuts import render

#temporary module
from django.http import HttpResponse
# Create your views here.

# here goes everything you want to display, except html
# each page is a function

def home(request):
    # Instead of this, render
    #return HttpResponse("Hi Im Juan")
    return render(request, "home.html")

def about(request):
    return render(request, 'about.html')
    return HttpResponse("additional page, might delete")
