from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from .forms import ReservationForm
from .models import Menu, BatteryOption, Location


# ---------------- BASIC TEST ----------------
def hello_world(request):
    return HttpResponse("Hello World")


class HelloEthiopia(View):
    def get(self, request):
        return HttpResponse("Hello Ethiopia")


# ---------------- HOME PAGE ----------------
def home(request):
    return render(request, 'firstapp/home.html')


# ---------------- RESERVATION ----------------
def reservation_view(request):
    form = ReservationForm()

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Reservation created successfully!")
            return redirect('home')

    return render(request, 'index.html', {'form': form})


# ---------------- MENU ----------------
def battery_menu(request):
    menu_data = Menu.objects.all()
    return render(request, 'battery_menu.html', {'battery_menu': menu_data})


# ---------------- MENU ITEM ----------------
def display_battery_menu_item(request, pk=None):
    if pk:
        battery_menu_item = BatteryOption.objects.get(pk=pk)
    else:
        battery_menu_item = None

    return render(request, 'battery_menu_item.html', {
        'battery_menu_item': battery_menu_item
    })


# ---------------- SIGNUP ----------------
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():   # FIXED HERE
            form.save()
            messages.success(request, "Account created! Please log in.")
            return redirect('login')

    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form})


# ---------------- MAP ----------------
def map_view(request):
    location = Location.objects.first()

    if location:
        data = {
            "name": location.name,
            "latitude": location.latitude,
            "longitude": location.longitude
        }
    else:
        data = {
            "name": "No location",
            "latitude": 0.33444,
            "longitude": 32.601386
        }

    return render(request, "members/map.html", {"location": data})