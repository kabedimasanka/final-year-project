from django.urls import path
from .views import battery_swap

urlpatterns = [
    path('battery-swap/', battery_swap),
]