from django.shortcuts import render

# Create your views here.

def index(request):
    name = request.GET.get("name") or "world!"
    return HttpResponse("Hello, "+name)