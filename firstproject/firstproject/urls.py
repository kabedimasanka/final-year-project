from django.contrib import admin
from django.urls import path, include
from members import views as member_views
from members import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('api/', include('api.urls')),

    path('logout/', LogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),

    # Home page
    path('', member_views.home, name='home'),

    # Members app
    path('members/', include('members.urls')),

    # App prefix version (what you want)
    path('app/', include('members.urls')),
]
