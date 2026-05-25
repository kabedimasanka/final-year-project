from django.urls import path
from . import views
from .views import reservation_view
from django.urls import path, include


urlpatterns = [
    path('map/', views.map_view, name='university_map'),
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('admin-login/', views.admin_login_view, name='admin_login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home, name='home'),
    path('reservation/', views.reservation_view, name='reservation'),
    path('dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path("message/<int:pk>/", views.message_view, name="message"),
]
