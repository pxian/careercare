from django.db import models
from test_cand.models import TestCand
from django.contrib.auth.models import User


class SSearch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    category = models.CharField(max_length=100, null=True)
    service_type = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=500, null=True, blank=True)
    total_search = models.CharField(max_length=500, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user.id)


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    cand = models.ForeignKey(TestCand, on_delete=models.CASCADE, default=1)
    messages = models.TextField(null=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user.id)
