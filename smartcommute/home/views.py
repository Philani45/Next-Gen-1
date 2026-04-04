from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserLocation
from .forms import LocationForm
from .utils import geocode_address
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'home/index.html')

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # Check password match
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        # Check if username exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("register")

        # Create user in database
        User.objects.create_user(username=username, password=password)

        messages.success(request, "Account created! Please log in.")
        return redirect("login")

    return render(request, "home/register.html")



def schedule(request):
    return render(request, 'home/schedule.html')

def location(request):
    return starting_location(request)

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

def starting_location(request):
    user = request.user

    try:
        location = UserLocation.objects.get(user=user)
    except UserLocation.DoesNotExist:
        location = None

    if request.method == "POST":
        form = LocationForm(request.POST, instance=location)

        if form.is_valid():
            loc = form.save(commit=False)
            loc.user = user

            # Convert address → coordinates
            lat, lng = geocode_address(loc.address)
            loc.latitude = lat
            loc.longitude = lng

            loc.save()
            return redirect("route")

    else:
        form = LocationForm(instance=location)

    return render(request, "home/location.html", {
        "form": form,
        "saved_location": location.address if location else None
    })