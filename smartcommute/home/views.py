from datetime import timedelta
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import (
    UserLocation,
    Building,
    Schedule,
    ClassSchedule
)

from .forms import LocationForm
from .utils import geocode_address


# ------------------------------
# BASIC PAGES
# ------------------------------

def index(request):
    return render(request, 'home/index.html')


# ------------------------------
# AUTHENTICATION
# ------------------------------

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("register")

        User.objects.create_user(username=username, password=password)
        messages.success(request, "Account created! Please log in.")
        return redirect("login")

    return render(request, "home/register.html")


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect("home")
        else:
            return render(request, "home/login.html", {
                "error": "Invalid username or password"
            })

    return render(request, "home/login.html")


# ------------------------------
# SCHEDULE
# ------------------------------

@login_required
def schedule(request):
    schedules = Schedule.objects.filter(user=request.user).order_by("day", "start_time")
    buildings = Building.objects.all()

    return render(request, "home/schedule.html", {
        "schedules": schedules,
        "buildings": buildings
    })


@login_required
def add_schedule(request):
    if request.method == "POST":
        course_name = request.POST.get("course")
        building_id = request.POST.get("building")
        days = request.POST.getlist("days")
        start_time = request.POST.get("start")
        end_time = request.POST.get("end")

        building = Building.objects.get(id=building_id)

        for day in days:
            Schedule.objects.create(
                user=request.user,
                course_name=course_name,
                building=building,
                day=day,
                start_time=start_time,
                end_time=end_time
            )

    return redirect("schedule")


@login_required
def delete_schedule(request, id):
    schedule = get_object_or_404(Schedule, id=id)
    schedule.delete()
    return redirect('schedule')


@login_required
def edit_schedule(request, id):
    schedule_obj = get_object_or_404(Schedule, id=id)

    if request.method == "POST":
        schedule_obj.course_name = request.POST.get("course")
        schedule_obj.day = request.POST.get("day")
        schedule_obj.start_time = request.POST.get("start")
        schedule_obj.end_time = request.POST.get("end")
        schedule_obj.building_id = request.POST.get("building")
        schedule_obj.save()
        return redirect('schedule')

    buildings = Building.objects.all()

    return render(request, "home/edit_schedule.html", {
        "schedule": schedule_obj,
        "buildings": buildings
    })


# ------------------------------
# LOCATION
# ------------------------------

@login_required
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


@login_required
def save_location(request):
    if request.method == "POST":
        lat = request.POST.get("latitude")
        lng = request.POST.get("longitude")

        UserLocation.objects.update_or_create(
            user=request.user,
            defaults={
                "latitude": lat,
                "longitude": lng,
                "address": "Live Location"
            }
        )

        return JsonResponse({"status": "saved"})


# ------------------------------
# ROUTING
# ------------------------------

@login_required
def route_old(request):
    """Auto-route to next class."""
    next_class = ClassSchedule.objects.filter(
        user=request.user,
        start_time__gte=timezone.now()
    ).order_by('start_time').first()

    if not next_class:
        return render(request, "no_upcoming_class.html")

    building_id = next_class.building.id
    return redirect(f"/departure?building={building_id}")


@login_required
def route(request):
    """Main route page using coordinates."""
    building_id = request.GET.get("building")
    if not building_id:
        return HttpResponse("Error: No building selected.")

    building = Building.objects.get(id=building_id)

    user_location = UserLocation.objects.filter(user=request.user).first()
    if not user_location:
        return HttpResponse("Error: No saved location found.")

    
    return render(request, "home/route.html", {
        "start_lat": user_location.latitude,
        "start_lng": user_location.longitude,
        "end_lat": building.latitude,
        "end_lng": building.longitude,
    })


# ------------------------------
# DEPARTURE TIME
# ------------------------------

@login_required
def departure(request):
    building_id = request.GET.get("building")

    if not building_id:
        return HttpResponse("Error: No building selected.")

    building = Building.objects.get(id=building_id)
    start_location = UserLocation.objects.filter(user=request.user).first()

    next_class = ClassSchedule.objects.filter(
        user=request.user,
        start_time__gte=timezone.now()
    ).order_by('start_time').first()

    if not next_class:
        return render(request, "no_upcoming_class.html")

    travel_time_minutes = 12
    buffer_minutes = 5

    arrival_time = next_class.start_time
    recommended_departure = arrival_time - timedelta(
        minutes=travel_time_minutes + buffer_minutes
    )

    return render(request, "home/departure.html", {
        "next_class": next_class,
        "building": building,
        "start_location": start_location,
        "travel_time_minutes": travel_time_minutes,
        "buffer_minutes": buffer_minutes,
        "arrival_time": arrival_time,
        "recommended_departure": recommended_departure,
    })


# ------------------------------
# MISC PAGES
# ------------------------------

def notifications(request):
    return render(request, 'home/notifications.html')

def settings(request):
    return render(request, 'home/settings.html')

def datastorage(request):
    return render(request, 'home/datastorage.html')
