from django.shortcuts import render

def index(request):
    return render(request, 'protinvis_app/index.html')