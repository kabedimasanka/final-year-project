from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from firstapp.models import Reservation   # 👈 IMPORTANT

# ---------------- SIGN UP FORM ----------------
class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


# ---------------- RESERVATION FORM ----------------
class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['user_name', 'date', 'price', 'status']

