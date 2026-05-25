from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django import forms
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Count, Q, Sum
from django.db.models.functions import TruncDate
from django.utils import timezone
from datetime import timedelta
from .models import Reservation, Location


FIXED_RESERVATION_PRICE = 5000
ADMIN_DASHBOARD_USERNAMES = {"emmanuella"}


def should_use_admin_dashboard(user):
    if not user.is_authenticated:
        return False
    return user.is_staff or user.username.lower() in ADMIN_DASHBOARD_USERNAMES


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

    if should_use_admin_dashboard(request.user):
        return redirect("/members/dashboard/")

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
                if should_use_admin_dashboard(user):
                    return redirect("/members/dashboard/")
                return redirect("/members/reservation/")
            else:
                messages.error(request, "Invalid login")

    return render(request, "members/login.html", {"form": form})


def admin_login_view(request):
    form = LoginForm()

    if should_use_admin_dashboard(request.user):
        return redirect("/members/dashboard/")

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"]
            )

            if user and should_use_admin_dashboard(user):
                login(request, user)
                return redirect("/members/dashboard/")

            messages.error(request, "Invalid admin login")

    return render(request, "members/login.html", {
        "form": form,
        "login_title": "Admin Login",
        "login_intro": "Sign in to open the admin dashboard.",
    })


def logout_view(request):
    logout(request)
    return redirect("/app/login/")


# RESERVATION → CREATE + GO TO MESSAGE
def reservation_view(request):
    if should_use_admin_dashboard(request.user):
        return redirect("/members/dashboard/")

    if request.method == "POST":
        reservation = Reservation.objects.create(
            user_name=request.POST.get("user_name"),
            date=request.POST.get("date"),
            price=FIXED_RESERVATION_PRICE,
            status=request.POST.get("status", "reserved")
        )

        # IMPORTANT: go to message page WITH ID
        return redirect("message", pk=reservation.id)

    reservations = Reservation.objects.all()

    return render(request, "members/reservation.html", {
        "reservations": reservations,
        "fixed_price": FIXED_RESERVATION_PRICE,
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


@user_passes_test(should_use_admin_dashboard, login_url='admin_login')
def admin_dashboard_view(request):
    today = timezone.localdate()
    week_start = today - timedelta(days=today.weekday())
    next_week_start = week_start + timedelta(days=7)
    last_7_start = today - timedelta(days=6)

    search_query = request.GET.get("q", "").strip()
    status_filter = request.GET.get("status", "").strip()
    validity_filter = request.GET.get("validity", "").strip()

    reservations = Reservation.objects.all()

    if search_query:
        reservations = reservations.filter(
            Q(user_name__icontains=search_query) |
            Q(code__icontains=search_query)
        )

    if status_filter:
        reservations = reservations.filter(status=status_filter)

    if validity_filter == "active":
        reservations = reservations.exclude(status="cancelled").filter(date__gte=today)
    elif validity_filter == "expired":
        reservations = reservations.filter(date__lt=today)
    elif validity_filter == "cancelled":
        reservations = reservations.filter(status="cancelled")

    reservations = reservations.order_by("-created_at", "-id")

    all_reservations = Reservation.objects.all()

    total_reservations = all_reservations.count()
    total_revenue = all_reservations.aggregate(total=Sum("price"))["total"] or 0
    purchases_this_week = all_reservations.filter(
        created_at__date__gte=week_start,
        created_at__date__lt=next_week_start,
    ).count()
    revenue_this_week = all_reservations.filter(
        created_at__date__gte=week_start,
        created_at__date__lt=next_week_start,
    ).aggregate(total=Sum("price"))["total"] or 0
    valid_count = all_reservations.exclude(status="cancelled").filter(date__gte=today).count()
    expired_count = all_reservations.filter(date__lt=today).count()
    cancelled_count = all_reservations.filter(status="cancelled").count()
    pending_count = all_reservations.filter(status="pending").count()
    today_count = all_reservations.exclude(status="cancelled").filter(date=today).count()
    upcoming_count = all_reservations.exclude(status="cancelled").filter(date__gt=today).count()
    expiring_soon_count = all_reservations.exclude(status="cancelled").filter(
        date__gte=today,
        date__lte=today + timedelta(days=1),
    ).count()

    status_rows = list(
        Reservation.objects.values("status")
        .annotate(total=Count("id"))
        .order_by("status")
    )

    daily_purchase_rows = list(
        Reservation.objects.filter(created_at__date__gte=last_7_start)
        .annotate(day=TruncDate("created_at"))
        .values("day")
        .annotate(total=Count("id"), revenue=Sum("price"))
        .order_by("day")
    )
    daily_purchase_map = {row["day"]: row for row in daily_purchase_rows}
    daily_labels = []
    daily_values = []
    daily_revenue_values = []

    for day_offset in range(7):
        day = last_7_start + timedelta(days=day_offset)
        row = daily_purchase_map.get(day)
        daily_labels.append(day.strftime("%b %d"))
        daily_values.append(row["total"] if row else 0)
        daily_revenue_values.append(row["revenue"] if row else 0)

    recent_reservations = all_reservations.order_by("-created_at", "-id")[:6]
    upcoming_reservations = all_reservations.exclude(status="cancelled").filter(
        date__gte=today
    ).order_by("date", "id")[:6]

    context = {
        "reservations": reservations,
        "today": today,
        "search_query": search_query,
        "status_filter": status_filter,
        "validity_filter": validity_filter,
        "total_reservations": total_reservations,
        "total_revenue": total_revenue,
        "purchases_this_week": purchases_this_week,
        "revenue_this_week": revenue_this_week,
        "valid_count": valid_count,
        "expired_count": expired_count,
        "cancelled_count": cancelled_count,
        "pending_count": pending_count,
        "today_count": today_count,
        "upcoming_count": upcoming_count,
        "expiring_soon_count": expiring_soon_count,
        "status_labels": [row["status"].title() for row in status_rows],
        "status_values": [row["total"] for row in status_rows],
        "daily_labels": daily_labels,
        "daily_values": daily_values,
        "daily_revenue_values": daily_revenue_values,
        "validity_labels": ["Active", "Expired", "Cancelled"],
        "validity_values": [valid_count, expired_count, cancelled_count],
        "recent_reservations": recent_reservations,
        "upcoming_reservations": upcoming_reservations,
    }
    return render(request, "members/admin_dashboard.html", context)
