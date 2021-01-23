from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class JobAd(models.Model):
    company_name = models.CharField(max_length=100, null=True)
    position_title = models.CharField(max_length=100, null=True)
    employment_type = models.CharField(max_length=100, null=True)
    position_level = models.CharField(max_length=100, null=True)
    job_specialization = models.CharField(max_length=100, null=True)
    job_description = models.TextField(null=True)
    job_requirements = models.TextField(null=True)
    location = models.TextField(null=True)
    salary = models.CharField(max_length=100, null=True, blank=True)
    # closing_date = models.DateField(
    #     ("Date"), auto_now=False, auto_now_add=False, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.position_title

class Freelance(models.Model):
    company_name = models.CharField(max_length=100, null=True)
    job_title = models.CharField(max_length=100, null=True)
    category = models.CharField(max_length=100, default='',blank ='True')
    job_type = models.CharField(max_length=100,default='',blank ='True')
    job_description = models.CharField(max_length=500,default='',blank ='True')
    city = models.CharField(max_length=100,default='',blank ='True')
    working_hour = models.CharField(max_length=100,default='',blank ='True')
    pay = models.CharField(max_length=100,default='',blank ='True')
    industry = models.CharField(max_length=100,default='',blank ='True')
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.job_title

class AppliedJob(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    jobad = models.ForeignKey(JobAd, on_delete=models.CASCADE, default=1,related_name="job_applied")
    status = models.CharField(max_length=100, null=True,default ="Application Processing")
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)

class AppliedFree(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    freelance = models.ForeignKey(Freelance, on_delete=models.CASCADE, default=1)
    status = models.CharField(max_length=100, null=True,default ="Application Processing")
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)

class ServiceRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=100, null=True)
    date = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    time = models.TimeField(auto_now=False, auto_now_add=False,null=True,blank=True)
    address =models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)
    title =models.CharField(max_length=100, null=True)
    timestamp = models.DateTimeField(auto_now=True)
    price = models.IntegerField(blank='True',default=0)

    def __str__(self):
        return str(self.user)

class ViewedJob(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    jobad = models.ForeignKey(JobAd, on_delete=models.CASCADE, default=1)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)

class ViewedFree(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    freelance = models.ForeignKey(Freelance, on_delete=models.CASCADE, default=1)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)