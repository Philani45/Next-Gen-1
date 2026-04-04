from django.shortcuts import render

def index(request):
    return render(request, 'home/index.html')

def register(request):
    return render(request, 'home/register.html')

def schedule(request):
    return render(request, 'home/schedule.html')

def location(request):
    return render(request, 'home/location.html')

def route(request):
    return render(request, 'home/route.html')

def departure(request):
    return render(request, 'home/departure.html')

def notifications(request):
    return render(request, 'home/notifications.html')

def settings(request):
    return render(request, 'home/settings.html')

def datastorage(request):
    return render(request, 'home/datastorage.html')

def login(request):
    return render(request, 'home/login.html')