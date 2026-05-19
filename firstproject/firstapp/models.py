from django.db import models
from django.utils import timezone

# Battery model
class Battery(models.Model):
    name = models.CharField(max_length=100, default="Battery Unit")
    phone = models.IntegerField()

    def __str__(self):
        return self.name


# Reservation model
class Reservation(models.Model):
    user_name = models.CharField(max_length=100)
    date = models.DateField(default=timezone.now)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, default="reserved")
    code = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.user_name} - {self.date}"


# Battery type
class BatteryOption(models.Model):
    name = models.CharField(max_length=100)
    voltage = models.FloatField()
    capacity = models.IntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name


# Station model
class BatteryStation(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name


# ✅ FIXED BatterySwap model
class BatterySwap(models.Model):
    user_name = models.CharField(max_length=100)   # ✅ FIX: no ForeignKey
    code = models.CharField(max_length=10)
    status = models.CharField(max_length=20, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_name} - {self.code}"