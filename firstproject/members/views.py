from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django import forms
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Reservation
from .models import Reservation, Location


# HOME
def home(request):
    return render(request, "members/home.html")


# SIGNUP
def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect("signup")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("signup")

        User.objects.create_user(username=username, email=email, password=password1)

        messages.success(request, "Account created successfully!")
        return redirect("login")

    return render(request, "members/signup.html")


# LOGIN FORM
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


def login_view(request):
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"]
            )

            if user:
                login(request, user)
                return redirect("reservation")
            else:
                messages.error(request, "Invalid login")

    return render(request, "members/login.html", {"form": form})


# RESERVATION → CREATE + GO TO MESSAGE
def reservation_view(request):
    if request.method == "POST":
        reservation = Reservation.objects.create(
            user_name=request.POST.get("user_name"),
            date=request.POST.get("date"),
            price=request.POST.get("price"),
            status=request.POST.get("status")
        )

        # IMPORTANT: go to message page WITH ID
        return redirect("message", pk=reservation.id)

    reservations = Reservation.objects.all()

    return render(request, "members/reservation.html", {
        "reservations": reservations
    })



# MESSAGE PAGE
def message_view(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)

    return render(request, "members/message.html", {
        "reservation": reservation
    })


# MAP PAGE
def map_view(request):
    return render(request, 'members/map.html')
