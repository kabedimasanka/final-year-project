import random
from django.db import models


class Reservation(models.Model):

    STATUS_CHOICES = [
        ("reserved", "Reserved"),
        ("pending", "Pending"),
        ("cancelled", "Cancelled"),
    ]

    user_name = models.CharField(max_length=100)
    date = models.DateField()
    price = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    code = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = str(random.randint(100000, 999999))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user_name


class Location(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name
