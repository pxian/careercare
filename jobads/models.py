from django.apps import apps
from django.db import models
from test_cand.models import TestCand
from django.contrib.auth.models import User


class JobAd(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    position_title = models.CharField(max_length=100, null=True)
    employment_type = models.CharField(max_length=100, null=True)
    position_level = models.CharField(max_length=100, null=True)
    job_specialization = models.CharField(max_length=100, null=True)
    job_description = models.TextField(null=True)
    job_requirements = models.TextField(null=True)
    location = models.TextField(null=True)
    min_salary = models.CharField(max_length=100, null=True, blank=True)
    max_salary = models.CharField(max_length=100, null=True, blank=True)
    closing_date = models.DateField(
        ("Date"), auto_now=False, auto_now_add=False, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.position_title


class Unprocessed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    jobad = models.ForeignKey(JobAd, on_delete=models.CASCADE, default=1)
    cand = models.ForeignKey(TestCand, on_delete=models.CASCADE, default=1)
    status = models.CharField(max_length=100, null=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)


class Shortlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    jobad = models.ForeignKey(JobAd, on_delete=models.CASCADE, default=1)
    cand = models.ForeignKey(TestCand, on_delete=models.CASCADE, default=1)
    hidden = models.CharField(max_length=100, null=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)


class Interview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    jobad = models.ForeignKey(JobAd, on_delete=models.CASCADE, default=1)
    cand = models.ForeignKey(TestCand, on_delete=models.CASCADE, default=1)
    hidden = models.CharField(max_length=100, null=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)


class NotSuitable(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    jobad = models.ForeignKey(JobAd, on_delete=models.CASCADE, default=1)
    cand = models.ForeignKey(TestCand, on_delete=models.CASCADE, default=1)
    hidden = models.CharField(max_length=100, null=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)


class Invitation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    jobad = models.ForeignKey(JobAd, on_delete=models.CASCADE, default=1)
    cand = models.ForeignKey(TestCand, on_delete=models.CASCADE, default=1)
    booked_date = models.DateField(
        ("Date"), auto_now=False, auto_now_add=False)
    booked_time = models.TimeField(
        ("Time"), auto_now=False, auto_now_add=False)
    messages = models.TextField(null=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)

class joblist(models.Model):
    job_name = models.CharField(max_length=100, null=True)


class test_employee(models.Model):
    name = models.CharField(max_length=100, null=True)
    openess = models.IntegerField()
    conscientiousness = models.IntegerField()
    extraversion = models.IntegerField()
    agreeableness = models.IntegerField()
    neuroticism = models.IntegerField()
    job_id = models.ForeignKey(joblist, on_delete=models.CASCADE, default=1)
    JobAd_id = models.ForeignKey(JobAd, on_delete=models.CASCADE, default=1)
    chart = models.CharField(max_length=100, null=True)
