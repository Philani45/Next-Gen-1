from datetime import timedelta
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserLocation
from .forms import LocationForm
from .utils import geocode_address
from django.contrib.auth.decorators import login_required
from .models import Building, Schedule, ClassSchedule
import json
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect
from .models import Schedule

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
    schedules = Schedule.objects.filter(user=request.user).order_by("day", "start_time")
    buildings = Building.objects.all()

    return render(request, "home/schedule.html", {
        "schedules": schedules,
        "buildings": buildings
    })

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

        return redirect("schedule")  # reload page

    return redirect("schedule")


def location(request):
    return starting_location(request)

def route(request):
    user_location = UserLocation.objects.get(user=request.user)

    building_id = request.GET.get("building")
    if not building_id:
        return HttpResponse("Error: No building selected.")

    try:
        building = Building.objects.get(id=building_id)
    except Building.DoesNotExist:
        return HttpResponse("Error: Building not found.")

    return render(request, "home/route.html", {
        "user_location": user_location,
        "building": building
    })

def route_view(request):
    building_id = request.GET.get("building")

    if not building_id:
        return HttpResponse("Error: No building selected.")

    building = Building.objects.get(id=building_id)

    # Get user's saved starting location (UserLocation)
    start_location = UserLocation.objects.filter(user=request.user).first()

    context = {
        "building": building,
        "start_location": start_location,
    }

    return render(request, "route.html", context)


def departure(request):
    # 1. Get building ID passed from auto-route
    building_id = request.GET.get("building")

    if not building_id:
        return HttpResponse("Error: No building selected.")

    building = Building.objects.get(id=building_id)

    # 2. Get user's starting location
    start_location = UserLocation.objects.filter(user=request.user).first()

    # 3. Get the user's next class
    next_class = ClassSchedule.objects.filter(
        user=request.user,
        start_time__gte=timezone.now()
    ).order_by('start_time').first()

    if not next_class:
        return render(request, "no_upcoming_class.html")

    # 4. Travel time (placeholder — replace with Google Maps API later)
    travel_time_minutes = 12

    # 5. Buffer time (could be user setting later)
    buffer_minutes = 5

    # 6. Arrival time = class start time
    arrival_time = next_class.start_time

    # 7. Recommended departure = arrival - travel - buffer
    recommended_departure = arrival_time - timedelta(
        minutes=travel_time_minutes + buffer_minutes
    )

    # 8. Send everything to the template
    context = {
        "next_class": next_class,
        "building": building,
        "start_location": start_location,
        "travel_time_minutes": travel_time_minutes,
        "buffer_minutes": buffer_minutes,
        "arrival_time": arrival_time,
        "recommended_departure": recommended_departure,
    }

    return render(request, "home/departure.html", context)

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

def auto_route(request):
    next_class = ClassSchedule.objects.filter(
        user=request.user,
        start_time__gte=timezone.now()
    ).order_by('start_time').first()

    if not next_class:
        return render(request, "no_upcoming_class.html")

    building_id = next_class.building.id

    # Redirect to the Recommended Departure Time page
    return redirect(f"/departure?building={building_id}")


def delete_schedule(request, id):
    schedule = get_object_or_404(Schedule, id=id)
    schedule.delete()
    return redirect('schedule') 

def edit_schedule(request, id):
    schedule = get_object_or_404(Schedule, id=id)

    if request.method == "POST":
        schedule.course_name = request.POST.get("course")
        schedule.day = request.POST.get("day")
        schedule.start_time = request.POST.get("start")
        schedule.end_time = request.POST.get("end")
        schedule.building_id = request.POST.get("building")
        schedule.save()
        return redirect('schedule')

    buildings = Building.objects.all()

    return render(request, "schedule.html", {
        "schedule": schedule,
        "buildings": buildings
    })
