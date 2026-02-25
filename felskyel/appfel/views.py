from django.http import HttpResponse

from django.shortcuts import render

# Create your views here.

def prueba(request):
    return HttpResponse("Prueba pantalla")

def index(request):
    return render (request, 'index.html')
