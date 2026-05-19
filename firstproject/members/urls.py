from django.urls import path
from . import views
from .views import reservation_view
from django.urls import path, include


urlpatterns = [
    path('map/', views.map_view, name='university_map'),
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('home/', views.home, name='home'),
    path('reservation/', views.reservation_view, name='reservation'),
    path("message/<int:pk>/", views.message_view, name="message"),
]