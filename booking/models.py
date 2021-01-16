from django.apps import apps
from django.db import models
from service.models import Service
from django.contrib.auth.models import User


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, default=1)
    booked_date = models.DateField(
        ("Date"), auto_now=False, auto_now_add=False)
    booked_time = models.TimeField(
        ("Time"), auto_now=False, auto_now_add=False)
    address = models.CharField(max_length=100, blank=True, null=True)
    additional_info = models.CharField(max_length=100, blank=True, null=True)
    job_status = models.CharField(max_length=100, null=True)
    reasons = models.CharField(max_length=100, blank=True, null=True)
    hidden = models.CharField(max_length=100, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.service.id)
